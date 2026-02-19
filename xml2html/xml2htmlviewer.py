"""
XML to HTML変換GUIビューア
"""
import logging
import sys
import tempfile
import webbrowser
import zipfile
from pathlib import Path
from typing import List, Optional

import tkinter as tk
from tkinter import messagebox, font

from xml2html_common import XSLTProcessor, TempFileManager, setup_logging
from config import Config


class XMLViewer:
    """XMLファイルビューアクラス"""
    
    def __init__(self):
        setup_logging(Config.LOGGING_LEVEL)
        self.logger = logging.getLogger(__name__)
        self.processor = XSLTProcessor()
        self.temp_manager = TempFileManager()
    
    def view_xml(self, xml_path: Path) -> bool:
        """XMLをHTMLに変換しブラウザで表示"""
        try:
            self.logger.info(f"XML表示中: {xml_path.name}")
            
            html = self.processor.transform_xml(xml_path)
            if not html:
                return False
            
            tmp_path = Path(tempfile.gettempdir()) / f"{xml_path.stem}_view.html"
            tmp_path.write_text(html, encoding=Config.DEFAULT_ENCODING)
            
            webbrowser.open(str(tmp_path))
            self.logger.info(f"ブラウザで開きました: {xml_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"表示エラー: {xml_path} - {e}")
            return False
    
    def show_file_selector(self, xml_files: List[Path], temp_dir: Path) -> Optional[Path]:
        """ファイル選択GUIを表示"""
        if not xml_files:
            messagebox.showinfo("情報", "ZIP内にXMLファイルがありません")
            return None
        
        root = tk.Tk()
        root.title(Config.GUI_SETTINGS["window_title"])
        root.geometry(Config.GUI_SETTINGS["window_geometry"])
        root.attributes("-topmost", Config.GUI_SETTINGS["topmost"])
        
        # ESCキーで閉じる
        root.bind("<Escape>", lambda e: root.destroy())
        
        # フォント設定
        list_font = font.Font(size=Config.GUI_SETTINGS["font_size"])
        
        # スクロールバー付きリストボックス
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            frame,
            selectmode=tk.SINGLE,
            width=Config.GUI_SETTINGS["listbox_width"],
            height=Config.GUI_SETTINGS["listbox_height"],
            font=list_font,
            yscrollcommand=scrollbar.set
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # 表示名（ZIP内の相対パス）
        display_names = [str(f.relative_to(temp_dir)) for f in xml_files]
        for name in display_names:
            listbox.insert(tk.END, name)
        
        selected_file = None
        
        def on_double_click(event):
            nonlocal selected_file
            sel = listbox.curselection()
            if sel:
                selected_file = xml_files[sel[0]]
                root.destroy()
        
        listbox.bind("<Double-Button-1>", on_double_click)
        root.mainloop()
        
        return selected_file
    
    def view_archive(self, zip_path: Path) -> bool:
        """ZIPファイル内のXMLを選択して表示"""
        try:
            self.logger.info(f"ZIP展開中: {zip_path.name}")
            
            temp_dir = self.temp_manager.create_temp_dir()
            
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(temp_dir)
            
            xml_files = list(temp_dir.rglob("*.xml"))
            selected = self.show_file_selector(xml_files, temp_dir)
            
            if selected:
                return self.view_xml(selected)
            return False
            
        except Exception as e:
            self.logger.error(f"ZIP表示エラー: {zip_path} - {e}")
            return False
    
    def process_files(self, file_paths: List[str]) -> None:
        """複数ファイルを処理"""
        for path_str in file_paths:
            path = Path(path_str)
            
            if not path.exists():
                self.logger.error(f"ファイルが存在しません: {path}")
                continue
            
            if path.is_file() and path.suffix.lower() in Config.SUPPORTED_XML_EXTENSIONS:
                self.view_xml(path)
            elif path.is_file() and path.suffix.lower() in Config.SUPPORTED_ARCHIVE_EXTENSIONS:
                self.view_archive(path)
            else:
                self.logger.warning(f"サポート外のファイル: {path}")
    
    def cleanup(self):
        """リソースをクリーンアップ"""
        self.temp_manager.cleanup()


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python xml2htmlviewer.py <XMLファイル|ZIPファイル> [...]")
        sys.exit(1)
    
    viewer = XMLViewer()
    try:
        viewer.process_files(sys.argv[1:])
    finally:
        viewer.cleanup()


if __name__ == "__main__":
    main()