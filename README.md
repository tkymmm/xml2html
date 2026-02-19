# XML to HTML変換ツール

XMLファイルをXSLTスタイルシートを使用してHTMLに変換するツールです。

## 機能

- 単一XMLファイルのHTML変換
- ZIPアーカイブ内のXMLファイル一括変換
- GUIビューアによるブラウザ表示
- oshiraseクラスの折り返し対応

## ファイル構成

```
xml2html/
├── xml2html.py              # コマンドライン変換ツール
├── xml2htmlviewer.py        # GUIビューア
├── xml2html_common.py       # 共通モジュール
├── config.py                # 設定ファイル
└── README.md               # このファイル
```

## 使用方法

### コマンドラインツール

```bash
# 単一XMLファイルを変換
python xml2html.py input.xml

# ZIPファイル内のXMLを一括変換
python xml2html.py archive.zip

# 複数ファイルを一度に処理
python xml2html.py file1.xml file2.xml archive.zip
```

### GUIビューア

```bash
# XMLファイルをブラウザで表示
python xml2htmlviewer.py input.xml

# ZIPファイル内のXMLを選択して表示
python xml2htmlviewer.py archive.zip
```

## 設定

`config.py`で以下の設定が可能です：

- エンコーディング
- サポートするファイル拡張子
- GUIウィンドウ設定
- ロギングレベル

## 依存ライブラリ

- lxml
- tkinter (GUIビューアのみ)

## インストール

```bash
pip install lxml
```

## 変換処理の仕組み

1. XMLファイルから`xml-stylesheet`処理命令を解析
2. XSLTスタイルシートを検索・読み込み
3. lxmlを使用してXMLをHTMLに変換
4. oshiraseクラスのpreタグをdivタグに変換
5. 折り返し用CSSをheadタグ内に挿入
6. HTMLファイルとして出力

## ライセンス

このツールは公文書のHTML変換を目的として開発されました。
