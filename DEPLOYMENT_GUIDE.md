# AI山田v6.0 デプロイガイド

## 🚀 Streamlit Cloudへのデプロイ手順

### 1. GitHubリポジトリ準備

```bash
# リポジトリ作成
git init
git add .
git commit -m "Initial commit: AI山田v6.0"

# GitHubにpush
git remote add origin https://github.com/YOUR_USERNAME/ai-yamada-v6.git
git push -u origin main
```

### 2. Streamlit Cloudでデプロイ

1. https://share.streamlit.io/ にアクセス
2. 「New app」をクリック
3. GitHubリポジトリを選択
4. ブランチ: `main`
5. メインファイル: `app.py`
6. 「Advanced settings」→「Secrets」にAPIキーを設定:

```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"
```

7. 「Deploy!」をクリック

### 3. デプロイ完了

デプロイURL: https://ai-yamada.streamlit.app

---

## 🔧 ローカル実行

```bash
# 依存関係インストール
pip install -r requirements.txt

# APIキー設定
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.tomlを編集してAPIキーを入力

# アプリ起動
streamlit run app.py
```

---

## 📁 ファイル構成

```
ai_yamada_v6_final/
├── app.py                          # メインアプリ
├── config.py                       # 設定
├── requirements.txt                # 依存関係
├── README.md                       # プロジェクト概要
├── DEPLOYMENT_GUIDE.md             # このファイル
├── .streamlit/
│   ├── config.toml                 # Streamlit設定
│   └── secrets.toml.example        # APIキーサンプル
├── core/
│   ├── __init__.py
│   └── coaching_engine.py          # コーチングエンジン
├── diagnosis/
│   ├── __init__.py
│   ├── enneagram_estimator.py     # エニアグラム診断
│   └── fourstance_estimator.py    # 4スタンス診断
├── data/
│   ├── AI山田_v5.2.1_Instructions.md
│   ├── YAMADA_AI_COMPLETE_PACKAGE.md
│   ├── yamada_4stance_conversational_questions_v1.6.md
│   └── (その他データファイル)
└── utils/
    ├── __init__.py
    └── data_loader.py              # データローダー
```

---

## ⚙️ 環境変数

### Streamlit Cloud
Secrets機能で設定:
- `OPENAI_API_KEY`: OpenAI APIキー

### ローカル
`.streamlit/secrets.toml`で設定:
```toml
OPENAI_API_KEY = "sk-..."
```

---

## 🔒 セキュリティ

- **APIキーは絶対にGitにコミットしない**
- `.gitignore`に`.streamlit/secrets.toml`を追加済み
- Streamlit CloudのSecretsで安全に管理

---

## 📊 動作確認

1. アプリ起動
2. チャットで「サーブがうまくいかない」と入力
3. AI山田が自然な会話で質問開始
4. サイドバーで診断進捗を確認
5. 信頼度が上がるにつれて、最適化されたアドバイスが提供される

---

## 🐛 トラブルシューティング

### エラー: "OpenAI APIキーが設定されていません"
→ Streamlit CloudのSecretsまたは`.streamlit/secrets.toml`でAPIキーを設定

### エラー: "データファイルが見つかりません"
→ `data/`ディレクトリに必要なMDファイルがあるか確認

### 診断が進まない
→ サイドバーで診断状況を確認。質問数が足りない場合は会話を続ける

---

## 📞 サポート

問題が解決しない場合は、以下を確認:
1. ログ確認: Streamlit Cloudの「Manage app」→「Logs」
2. データファイルの存在確認
3. APIキーの有効性確認

---

## 🎉 完成!

AI山田v6.0のデプロイが完了しました!
世界最高品質のAIコーチングシステムをお楽しみください。
