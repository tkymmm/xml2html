"""
XML to HTML変換の共通モジュール
"""
import logging
import re
import tempfile
from pathlib import Path
from typing import Optional
from lxml import etree


class XSLTProcessor:
    """XSLT変換を管理するクラス"""
    
    OSHIRASE_CSS = """
<style>
.oshirase {
    white-space: normal !important;
    word-break: break-all !important;
}
</style>
"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def find_xsl_from_xml(self, xml_path: Path) -> Optional[Path]:
        """XMLファイルからXSLTスタイルシートパスを検索"""
        try:
            text = xml_path.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r'href="([^"]+\.xsl)"', text)
            if match:
                xsl_path = xml_path.parent / match.group(1)
                if xsl_path.exists():
                    return xsl_path
        except Exception as e:
            self.logger.error(f"XSL検索エラー: {xml_path} - {e}")
        return None
    
    def transform_xml(self, xml_path: Path) -> Optional[str]:
        """XMLをHTMLに変換"""
        try:
            xsl_path = self.find_xsl_from_xml(xml_path)
            if not xsl_path:
                raise FileNotFoundError(f"XSLファイルが見つかりません: {xml_path}")
            
            xml_tree = etree.parse(str(xml_path))
            xsl_tree = etree.parse(str(xsl_path))
            transformer = etree.XSLT(xsl_tree)
            result = transformer(xml_tree)
            
            html = str(result)
            html = self._post_process_html(html)
            return html
            
        except Exception as e:
            self.logger.error(f"XML変換エラー: {xml_path} - {e}")
            return None
    
    def _post_process_html(self, html: str) -> str:
        """HTMLの後処理"""
        html = html.replace('<pre class="oshirase">', '<div class="oshirase">')
        html = html.replace('</pre>', '</div>')
        html = html.replace("</head>", self.OSHIRASE_CSS + "</head>")
        return html


class TempFileManager:
    """一時ファイルを管理するクラス"""
    
    def __init__(self):
        self.temp_dirs = []
    
    def create_temp_dir(self) -> Path:
        temp_dir = Path(tempfile.mkdtemp())
        self.temp_dirs.append(temp_dir)
        return temp_dir
    
    def cleanup(self):
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
        self.temp_dirs.clear()


def setup_logging(level: str = "INFO"):
    """ロギング設定"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
