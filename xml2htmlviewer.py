import sys
import re
import zipfile
import tempfile
import shutil
import webbrowser
from pathlib import Path
from lxml import etree
import tkinter as tk
from tkinter import messagebox, font

def find_xsl_from_xml(xml_path: Path) -> Path | None:
    """xml-stylesheet の href を取得して XSL のパスを返す"""
    text = xml_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'href="([^"]+\.xsl)"', text)
    if m:
        xsl_path = xml_path.parent / m.group(1)
        if xsl_path.exists():
            return xsl_path
    return None

def apply_xslt(xml_path: Path) -> str:
    """XML + XSL → HTML（文字列）"""
    xsl_path = find_xsl_from_xml(xml_path)
    if not xsl_path:
        raise FileNotFoundError(f"XSL が見つかりません: {xml_path}")

    xml_tree = etree.parse(str(xml_path))
    xsl_tree = etree.parse(str(xsl_path))
    transform = etree.XSLT(xsl_tree)
    result = transform(xml_tree)

    html = str(result)

    # ★ oshirase の <pre> → <div>
    html = html.replace('<pre class="oshirase">', '<div class="oshirase">')
    html = html.replace('</pre>', '</div>')

    # ★ 折り返し強制 CSS を注入
    fix_css = """
<style>
.oshirase {
    white-space: normal !important;
    word-break: break-all !important;
}
</style>
"""
    html = html.replace("</head>", fix_css + "</head>")

    return html

def view_xml(xml_path: Path):
    """XML を HTML に変換し、temp に保存してブラウザで開く"""
    html = apply_xslt(xml_path)

    tmp = Path(tempfile.gettempdir()) / f"{xml_path.stem}_view.html"
    tmp.write_text(html, encoding="utf-8")

    webbrowser.open(str(tmp))

def view_zip(zip_path: Path):
    """ZIP 内の XML を展開し、リストボックスで選択して表示（ダブルクリック + ESC + スクロールバー + 大きめフォント）"""
    temp_dir = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)

    xml_files = list(temp_dir.rglob("*.xml"))
    if not xml_files:
        messagebox.showinfo("情報", f"ZIP 内に XML がありません:\n{zip_path.name}")
        shutil.rmtree(temp_dir)
        return

    # Tkinter ウィンドウ
    root = tk.Tk()
    root.title("XML 選択")
    root.geometry("450x350")
    root.attributes("-topmost", True)

    # ESC で閉じる
    root.bind("<Escape>", lambda e: root.destroy())

    # 大きめフォント
    list_font = font.Font(size=12)

    # フレーム（スクロールバーとリストボックスをまとめる）
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # スクロールバー
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # リストボックス（フォント指定 + スクロールバー連動）
    listbox = tk.Listbox(
        frame,
        selectmode=tk.SINGLE,
        width=60,
        height=15,
        font=list_font,
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=listbox.yview)

    # 表示名（ZIP 内の相対パス）
    display_names = [str(x.relative_to(temp_dir)) for x in xml_files]
    for name in display_names:
        listbox.insert(tk.END, name)

    # ダブルクリックで開く
    def on_double_click(event):
        sel = listbox.curselection()
        if sel:
            index = sel[0]
            root.destroy()
            view_xml(xml_files[index])

    listbox.bind("<Double-Button-1>", on_double_click)

    root.mainloop()

    # temp は削除しない（ブラウザが参照するため）
    # → OS が後で自動クリーンアップする

def main():
    for arg in sys.argv[1:]:
        p = Path(arg)

        if p.is_file() and p.suffix.lower() == ".xml":
            view_xml(p)

        elif p.is_file() and p.suffix.lower() == ".zip":
            view_zip(p)

if __name__ == "__main__":
    main()