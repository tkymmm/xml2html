from lxml import etree
from pathlib import Path
import sys
import re
import zipfile
import tempfile
import shutil

def find_xsl_from_xml(xml_path: Path) -> Path | None:
    text = xml_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'href="([^"]+\.xsl)"', text)
    if m:
        xsl_path = xml_path.parent / m.group(1)
        if xsl_path.exists():
            return xsl_path
    return None

def transform(xml_path: Path, output_dir: Path):
    print(f"[INFO] XML 変換中: {xml_path.name}")

    xsl_path = find_xsl_from_xml(xml_path)
    if not xsl_path:
        print(f"[WARN] XSL が見つかりません: {xml_path.name}")
        return

    xml_tree = etree.parse(str(xml_path))
    xsl_tree = etree.parse(str(xsl_path))
    transform = etree.XSLT(xsl_tree)
    result = transform(xml_tree)

    # HTML 文字列化
    html = str(result)

    # ★ <pre> → <div>
    html = html.replace('<pre class="oshirase">', '<div class="oshirase">')
    html = html.replace('</pre>', '</div>')

    # ★ oshirase 専用の折り返し CSS を強制注入
    fix_css = """
<style>
.oshirase {
    white-space: normal !important;
    word-break: break-all !important;
}
</style>
"""
    html = html.replace("</head>", fix_css + "</head>")

    out_path = output_dir / (xml_path.stem + ".html")
    out_path.write_text(html, encoding="utf-8")

    print(f"[OK] {xml_path.name} → {out_path.name}")

def process_zip(zip_path: Path):
    print(f"[INFO] ZIP 展開中: {zip_path.name}")

    # 一時フォルダに展開
    temp_dir = Path(tempfile.mkdtemp())

    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)

    # 展開先の XML をすべて変換
    for xml in temp_dir.rglob("*.xml"):
        transform(xml, zip_path.parent)

    # 一時フォルダ削除
    shutil.rmtree(temp_dir)
    print(f"[INFO] ZIP 処理完了: {zip_path.name}")

def main():
    for arg in sys.argv[1:]:
        p = Path(arg)

        if p.is_file() and p.suffix.lower() == ".xml":
            transform(p, p.parent)

        elif p.is_file() and p.suffix.lower() == ".zip":
            process_zip(p)

if __name__ == "__main__":
    main()