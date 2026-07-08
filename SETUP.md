# AEGIS Boat Race Prediction Web - セットアップガイド

## 📋 要件

### 必須
- Docker & Docker Compose（推奨）
- または Python 3.9+ & Node.js 16+
- Claude API キー（Anthropic）

### オプション
- Git（クローン用）

---

## 🚀 クイックスタート（Docker推奨）

### 1. リポジトリをクローン

```bash
git clone https://github.com/Sakura5195/aegis-boat-prediction-web.git
cd aegis-boat-prediction-web
```

### 2. 環境変数を設定

```bash
cp .env.example .env
```

`.env` を編集して Claude API キーを設定：

```env
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FLASK_ENV=development
REACT_APP_API_URL=http://localhost:5000
```

### 3. Docker で起動

```bash
docker-compose up
```

初回は依存パッケージのインストールに時間がかかります（5～10分）。

### 4. ブラウザで確認

- **フロントエンド**: http://localhost:3000
- **バックエンド**: http://localhost:5000
- **ヘルスチェック**: http://localhost:5000/health

---

## 🔧 ローカル開発セットアップ

### バックエンド

```bash
# ディレクトリ移動
cd backend

# 仮想環境を作成（オプション）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt

# Flask アプリを起動
export FLASK_APP=app.py
flask run  # http://localhost:5000
```

### フロントエンド

```bash
# ディレクトリ移動
cd frontend

# 依存パッケージをインストール
npm install

# React 開発サーバーを起動
npm start  # http://localhost:3000
```

---

## 📚 使い方

### 1. 画像をアップロード

ボートレース出走表の画像をアップロードします。

### 2. データ確認

LLM が自動読み取りした出走情報を確認・修正します。

### 3. 予想実行

「予想する」ボタンを押すと：
- STEP2: AEGIS エンジンが統計計算を実行
- STEP3: LLM が結果を見やすいテキストに変換

### 4. 結果表示

```
【環境】逃げ（gap=1.2 / conf=0.87）

【3連単買い目】10点
① 1-2-3  8.5%  ◎
② 1-2-4  6.2%  ◎
...

【期待度】高
推奨: 3連単で勝負を推奨
```

---

## 🐛 トラブルシューティング

### Docker がうまく起動しない

```bash
# ログを確認
docker-compose logs -f

# キャッシュをクリアして再ビルド
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Claude API エラー

```
"Error: Invalid API key"
```

→ `.env` ファイルで `CLAUDE_API_KEY` を確認

### ポートが既に使用されている

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS / Linux
lsof -i :5000
kill -9 <PID>
```

---

## 📦 API エンドポイント

| メソッド | エンドポイント | 説明 |
|---------|------------|------|
| GET | `/health` | ヘルスチェック |
| POST | `/api/predict/step1` | 画像→JSON 構造化 |
| POST | `/api/predict/step2` | JSON→計算実行 |
| POST | `/api/predict/step3` | 結果→テキスト変換 |
| POST | `/api/predict/full` | ワンステップ実行 |

---

## 📝 開発ガイド

### プロジェクト構成

```
.
├── backend/
│   ├── app.py              # Flask メインアプリ
│   ├── config.py           # 設定ファイル
│   ├── services/
│   │   ├── step1_llm.py    # STEP1
│   │   ├── step2_engine.py # STEP2
│   │   └── step3_llm.py    # STEP3
│   └── engine/
│       └── aegis_engine_v51.py
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React コンポーネント
│   │   ├── pages/          # ページコンポーネント
│   │   └── App.jsx
│   └── package.json
│
├── docs/                   # ドキュメント
├── docker-compose.yml
└── .env.example
```

### テストの実行

```bash
# バックエンド
cd backend
pytest

# フロントエンド
cd frontend
npm test
```

---

## 🚢 本番デプロイ

### Heroku への デプロイ例

```bash
heroku create aegis-boat-prediction
git push heroku main
heroku config:set CLAUDE_API_KEY=sk-ant-...
```

### その他のプラットフォーム

- AWS Lambda + API Gateway
- Google Cloud Run
- Azure Container Instances

---

## 📞 サポート

問題が発生した場合は、GitHub Issues で報告してください：
https://github.com/Sakura5195/aegis-boat-prediction-web/issues

---

## 📄 ライセンス

MIT License
