# XML 公文書ツールセット

XML/XSL 形式の公文書を扱うためのツールです。  
以下の 2 つのアプリケーションがあります。

- **xml2html.exe**  
  XML または ZIP を HTML に変換するツール  
- **xml2htmlviewer.exe**  
  XML または ZIP をブラウザで閲覧するビューア

どちらもドラッグ＆ドロップで動作します。

---

## xml2html（変換ツール）

### 機能
- XML を HTML に変換
- ZIP を展開し、内部の XML を一括変換
- XML 内の `xml-stylesheet` から XSL を自動検出
- 出力 HTML は入力ファイルと同じフォルダに生成

### 使い方
1. `xml2html.exe` に XML または ZIP をドラッグ＆ドロップします  
2. 同じフォルダに HTML が生成されます

---

## xml2htmlviewer（ビューア）

### 機能
- XML を変換してブラウザで表示
- HTML はOSの一時フォルダに作成
- ZIP 内に複数 XML がある場合は選択ダイアログを表示
- ダブルクリックで開く簡易ビューア
- ESC キーでダイアログを閉じる

### 使い方
1. `xml2htmlviewer.exe` に XML または ZIP をドラッグ＆ドロップします  
2. 既定ブラウザで整形された HTML が表示されます  
3. ZIP の場合、XML を選択するダイアログが表示されます

---

## 対応形式
- XML（XSLT1.0）
- ZIP（内部に XML/XSL を含むもの）

---

## 動作環境
- Windows 10 / 11  
- Python 3.14 で開発し、PyInstaller により単一 exe 化

---

## ライセンス
自由に利用・改変できます。
