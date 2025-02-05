# Desktop Name Display

Windows用の仮想デスクトップ名表示アプリケーション。常に最前面に表示される小さなウィンドウに、現在の仮想デスクトップ名を表示します。

## 特徴

- 常に最前面に表示される小さなウィンドウ
- 仮想デスクトップの名前を大きな文字で表示
- デスクトップ名に応じて背景色と文字色が自動的に変更
- ドラッグ可能なウィンドウ位置
- 右クリックメニューによる終了機能

## 必要要件

- Windows 10/11
- Python 3.11以上
- 仮想デスクトップ機能の有効化

## インストール

### インストーラーを使用する場合

1. [Releases](../../releases)から最新のインストーラー(`DeskName_Setup.exe`)をダウンロード
2. インストーラーを実行
3. スタートメニューまたはデスクトップのショートカットから起動

### ソースコードから実行する場合

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/deskname.git
cd deskname

# 依存関係のインストール
pip install .

# 開発用依存関係のインストール(オプション)
pip install ".[dev]"

# アプリケーションの実行
python -m deskname.app
```

## 開発

### テストの実行

```bash
pytest
```

### 実行ファイルのビルド

```bash
# PyInstallerのインストール
pip install pyinstaller

# 実行ファイルの作成
pyinstaller --name deskname --onefile --noconsole --icon=NONE deskname/app.py
```

### インストーラーの作成

1. [Inno Setup](https://jrsoftware.org/isdl.php)をインストール
2. `deskname.iss`スクリプトをコンパイル

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照してください。
