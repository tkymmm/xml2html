"""
XML to HTML変換コマンドラインツール
"""
import logging
import sys
import zipfile
from pathlib import Path
from typing import List

from xml2html_common import XSLTProcessor, TempFileManager, setup_logging
from config import Config


class XMLToHTMLConverter:
    """XML to HTML変換メインクラス"""
    
    def __init__(self):
        setup_logging(Config.LOGGING_LEVEL)
        self.logger = logging.getLogger(__name__)
        self.processor = XSLTProcessor()
        self.temp_manager = TempFileManager()
    
    def convert_file(self, xml_path: Path, output_dir: Path) -> bool:
        """単一XMLファイルを変換"""
        try:
            self.logger.info(f"XML変換中: {xml_path.name}")
            
            html = self.processor.transform_xml(xml_path)
            if not html:
                return False
            
            out_path = output_dir / (xml_path.stem + ".html")
            out_path.write_text(html, encoding=Config.DEFAULT_ENCODING)
            
            self.logger.info(f"変換完了: {xml_path.name} → {out_path.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"変換エラー: {xml_path} - {e}")
            return False
    
    def process_archive(self, zip_path: Path) -> bool:
        """ZIPファイル内のXMLを変換"""
        try:
            self.logger.info(f"ZIP展開中: {zip_path.name}")
            
            temp_dir = self.temp_manager.create_temp_dir()
            
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(temp_dir)
            
            success_count = 0
            for xml_file in temp_dir.rglob("*.xml"):
                if self.convert_file(xml_file, zip_path.parent):
                    success_count += 1
            
            self.logger.info(f"ZIP処理完了: {zip_path.name} ({success_count}ファイル)")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"ZIP処理エラー: {zip_path} - {e}")
            return False
    
    def process_files(self, file_paths: List[str]) -> None:
        """複数ファイルを処理"""
        for path_str in file_paths:
            path = Path(path_str)
            
            if not path.exists():
                self.logger.error(f"ファイルが存在しません: {path}")
                continue
            
            if path.is_file() and path.suffix.lower() in Config.SUPPORTED_XML_EXTENSIONS:
                self.convert_file(path, path.parent)
            elif path.is_file() and path.suffix.lower() in Config.SUPPORTED_ARCHIVE_EXTENSIONS:
                self.process_archive(path)
            else:
                self.logger.warning(f"サポート外のファイル: {path}")
    
    def cleanup(self):
        """リソースをクリーンアップ"""
        self.temp_manager.cleanup()


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python xml2html.py <XMLファイル|ZIPファイル> [...]")
        sys.exit(1)
    
    converter = XMLToHTMLConverter()
    try:
        converter.process_files(sys.argv[1:])
    finally:
        converter.cleanup()


if __name__ == "__main__":
    main()