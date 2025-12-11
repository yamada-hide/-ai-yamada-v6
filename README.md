# AI山田v6.0 - 質問ベース診断システム

## 📌 プロジェクト概要
AI山田v5.2.1をベースに、4スタンス診断とエニアグラム診断を統合した次世代AIコーチングシステム

## 🎯 主要機能
### コア機能(v5.2.1継承)
- Meta Outcome: 5-6問で本質到達
- GROW深掘り: 50問システム
- 感情レベル3段階判定
- げんなりサイン検出
- パターン移動(15種類)
- 35種テニスメソッド

### 新機能
- **4スタンス診断**: 112問ステルス推定(75-85%精度)
- **エニアグラム診断**: 90問ステルス推定(70%精度)
- **統合アドバイス**: 診断結果×感情×メソッド

## 📁 ディレクトリ構造
```
ai_yamada_v6_final/
├── app.py                    # メインアプリ
├── requirements.txt          # 依存関係
├── config.py                 # 設定
├── core/
│   ├── coaching_engine.py   # コーチングエンジン
│   └── conversation_controller.py
├── diagnosis/
│   ├── enneagram_estimator.py
│   └── fourstance_estimator.py
├── data/
│   └── (各種MDファイル)
└── utils/
    └── data_loader.py
```

## 🚀 デプロイ
Streamlit Cloud: https://ai-yamada.streamlit.app

## 📝 開発履歴
- v6.0 (2025-12-11): 質問ベース診断統合
- v5.2.1: ChatGPT移植版
- v3.0: 動画解析版(アーカイブ)
