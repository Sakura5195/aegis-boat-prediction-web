# AEGIS Boat Race Prediction Web App
# AEGIS ボートレース予想 Web アプリケーション

AEGIS V5.1エンジンを使用したボートレース（競艇）の予想システムです。  
画像アップロードまたは手動入力から自動的にデータを構造化し、AI予想エンジンで3連単・3連複の買い目を生成します。

---

## 🎯 機能

- **画像アップロード** → 出走表・展示情報を自動読み取り（OCR + LLM）
- **データ構造化** → JSON 形式に自動変換（STEP1）
- **AI 予想エンジン** → AEGIS V5.1で統計計算（STEP2）
- **結果表示** → 3連単10点 + 3連複（統合）+ 期待度判定（STEP3）

---

## 📦 プロジェクト構成

```
aegis-boat-prediction-web/
├── backend/               # Flask バックエンド
│   ├── app.py            # メインアプリケーション
│   ├── config.py         # 設定ファイル
│   ├── requirements.txt   # Python 依存関係
│   ├── services/
│   │   ├── step1_llm.py  # STEP1: 画像→JSON
│   │   ├── step2_engine.py  # STEP2: エンジン実行
│   │   └── step3_llm.py  # STEP3: 出力整形
│   ├── engine/
│   │   └── aegis_engine_v51.py  # AEGIS V5.1 計算エンジン
│   └── prompts/
│       ├── step1.txt
│       ├── step3_santan.txt
│       └── step3_sanrenpuku.txt
│
├── frontend/              # React フロントエンド
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── App.jsx
│   └── package.json
│
├── docs/                  # ドキュメント
│   ├── AEGIS_仕様書.md
│   ├── AEGIS_入力.md
│   ├── AEGIS_予想.md
│   └── API_仕様.md
│
├── docker-compose.yml     # Docker 設定
└── .env.example          # 環境変数テンプレート
```

---

## 🚀 クイックスタート

### 前提条件
- Docker & Docker Compose
- または Python 3.9+ & Node.js 16+

### 方法1: Docker（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/Sakura5195/aegis-boat-prediction-web.git
cd aegis-boat-prediction-web

# 環境変数を設定
cp .env.example .env
# .env を編集して Claude API キーを設定

# Docker で起動
docker-compose up
```

ブラウザで http://localhost:3000 を開く

### 方法2: ローカル開発

**バックエンド:**
```bash
cd backend
pip install -r requirements.txt
export FLASK_APP=app.py
flask run  # http://localhost:5000
```

**フロントエンド:**
```bash
cd frontend
npm install
npm start  # http://localhost:3000
```

---

## 📚 ドキュメント

- **[AEGIS 仕様書](./docs/AEGIS_仕様書.md)** - エンジン全体の定義
- **[入力プロンプト（STEP1）](./docs/AEGIS_入力.md)** - 画像→JSON 変換
- **[出力プロンプト（STEP3）](./docs/AEGIS_予想.md)** - 予想結果表示
- **[API 仕様書](./docs/API_仕様.md)** - REST API 定義

---

## 🔑 環境変数

`.env` ファイルを作成して以下を設定：

```env
# Claude API
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Flask
FLASK_ENV=development
FLASK_DEBUG=True

# React
REACT_APP_API_URL=http://localhost:5000
```

---

## 🏗️ 開発フロー

1. **画像アップロード**  
   `POST /api/predict/upload` - 出走表画像をアップロード

2. **データ確認**  
   LLM (Claude) が画像を読み取り → JSON に変換  
   ユーザーが確認・修正

3. **予想実行**  
   `POST /api/predict/calculate` - AEGIS エンジン実行

4. **結果表示**  
   3連単10点 + 3連複 + 期待度判定を表示

---

## 🧪 テスト

```bash
# バックエンド
cd backend
pytest

# フロントエンド
cd frontend
npm test
```

---

## 📝 ライセンス

MIT License

---

## 🤝 貢献

プルリクエストを歓迎します！

---

## 📧 お問い合わせ

issues でバグ報告・機能提案をお願いします。
