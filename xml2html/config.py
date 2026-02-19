"""
XML2HTML変換ツールの設定
"""
from pathlib import Path
from typing import Dict, Any


class Config:
    """アプリケーション設定"""
    
    DEFAULT_ENCODING = "utf-8"
    SUPPORTED_XML_EXTENSIONS = {".xml"}
    SUPPORTED_ARCHIVE_EXTENSIONS = {".zip"}
    
    GUI_SETTINGS = {
        "window_title": "XML 選択",
        "window_geometry": "450x350",
        "listbox_width": 60,
        "listbox_height": 15,
        "font_size": 12,
        "topmost": True
    }
    
    LOGGING_LEVEL = "INFO"
    
    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """全設定を辞書で返す"""
        return {
            "encoding": cls.DEFAULT_ENCODING,
            "xml_extensions": cls.SUPPORTED_XML_EXTENSIONS,
            "archive_extensions": cls.SUPPORTED_ARCHIVE_EXTENSIONS,
            "gui": cls.GUI_SETTINGS,
            "logging": cls.LOGGING_LEVEL
        }
