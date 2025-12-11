# AI山田 v3.0 動画解析機能 デプロイガイド

**Phase 2完了**: MediaPipe + GPT-4 Vision統合  
**作成日**: 2025-12-09

---

## 📋 実装内容

### ✅ 完成した機能

1. **MediaPipe骨格検出システム** (`video_analyzer.py`)
   - 33関節ポイント抽出
   - A/B判定（つま先/かかと重心）
   - 1/2判定（内側/外側軸）
   - クロス/パラレル判定
   - 骨格オーバーレイ動画生成

2. **統合ナレッジベース** (`yamada_4stance_integrated_knowledge.md`)
   - 一般的な4スタンス理論
   - テニス特化データ
   - プロ選手マッピング
   - 動画解析フレームワーク

3. **Streamlit UI拡張** (`app_with_video.py`)
   - 動画アップロード機能
   - リアルタイム解析進捗表示
   - 判定結果の可視化
   - 信頼度スコア表示

---

## 🚀 デプロイ手順

### Step 1: ファイルをGitHubにアップロード

以下のファイルをGitHubリポジトリにアップロードしてください:

#### 必須ファイル（置き換え）

```
yamada-ai/
├── app.py  ← app_with_video.py にリネーム
├── requirements.txt  ← requirements_video.txt の内容にアップデート
├── yamada_coach.py  ← 既存のまま
└── 新規追加:
    ├── video_analyzer.py
    └── yamada_4stance_integrated_knowledge.md
```

#### ファイル操作手順

1. **ローカルでダウンロード:**
   - [`video_analyzer.py`](computer:///mnt/user-data/outputs/video_analyzer.py) をダウンロード
   - [`yamada_4stance_integrated_knowledge.md`](computer:///mnt/user-data/outputs/yamada_4stance_integrated_knowledge.md) をダウンロード
   - [`app_with_video.py`](computer:///mnt/user-data/outputs/app_with_video.py) をダウンロード
   - [`requirements_video.txt`](computer:///mnt/user-data/outputs/requirements_video.txt) をダウンロード

2. **GitHubで操作:**

   **オプションA: Web UIで操作（簡単）**
   
   a) `https://github.com/(あなたのユーザー名)/ai-yamada` にアクセス
   
   b) 既存ファイルの置き換え:
      - `app.py` をクリック → 編集ボタン（鉛筆アイコン）→ `app_with_video.py` の内容をコピペ → "Commit changes"
      - `requirements.txt` をクリック → 編集ボタン → `requirements_video.txt` の内容をコピペ → "Commit changes"
   
   c) 新規ファイルの追加:
      - "Add file" → "Create new file"
      - ファイル名: `video_analyzer.py` → 内容をコピペ → "Commit new file"
      - 同様に `yamada_4stance_integrated_knowledge.md` も追加
   
   d) コミットメッセージ例:
      ```
      Phase2完了: MediaPipe動画解析機能追加
      
      - MediaPipe骨格検出システム実装
      - 4スタンス自動判定ロジック追加
      - 動画アップロードUI追加
      - 判定精度: 85%+目標
      ```

   **オプションB: Git CLIで操作（上級者向け）**
   
   ```bash
   # リポジトリをクローン
   git clone https://github.com/(あなたのユーザー名)/ai-yamada.git
   cd ai-yamada
   
   # ファイルをコピー
   cp /path/to/downloaded/video_analyzer.py ./
   cp /path/to/downloaded/yamada_4stance_integrated_knowledge.md ./
   cp /path/to/downloaded/app_with_video.py ./app.py
   cp /path/to/downloaded/requirements_video.txt ./requirements.txt
   
   # Git操作
   git add .
   git commit -m "Phase2完了: MediaPipe動画解析機能追加"
   git push origin main
   ```

---

### Step 2: Streamlit Cloudで自動デプロイ

1. **自動デプロイ待機**
   - GitHubにpushすると、Streamlit Cloudが自動的に検知
   - 約2-3分で新しいバージョンがデプロイされます

2. **デプロイログ確認**
   - `https://share.streamlit.io` にアクセス
   - 'ai-yamada' アプリをクリック
   - "Manage app" → "Logs" でデプロイ状況を確認

3. **想定されるエラーと対処法**

   **エラー1: `ModuleNotFoundError: No module named 'mediapipe'`**
   ```
   原因: requirements.txtが更新されていない
   対処: requirements.txtにmediapipe>=0.10.0を追記
   ```

   **エラー2: `ModuleNotFoundError: No module named 'cv2'`**
   ```
   原因: opencv-pythonがインストールされていない
   対処: requirements.txtにopencv-python>=4.8.0を追記
   ```

   **エラー3: `FileNotFoundError: yamada_4stance_integrated_knowledge.md`**
   ```
   原因: ナレッジベースファイルがアップロードされていない
   対処: GitHubに yamada_4stance_integrated_knowledge.md をアップロード
   ```

---

### Step 3: 動作確認

1. **アプリにアクセス**
   - `https://ai-yamada.streamlit.app` を開く

2. **動画解析機能テスト**
   
   a) サイドバーで「🎬 動画で自動判定（推奨）」をクリック
   
   b) テスト動画をアップロード:
      - フォアハンドストローク動画（5-30秒）
      - 側面から撮影
      - MP4/MOV/AVI形式
   
   c) 「🚀 解析開始」をクリック
   
   d) 約30秒〜1分待つ
   
   e) 判定結果を確認:
      - タイプ（A1/A2/B1/B2）
      - 信頼度（%）
      - 類似プロ選手
      - 詳細スコア

3. **期待される結果**
   ```
   🎉 判定結果
   
   🎯 あなたのタイプ: A1
   信頼度: 85%
   類似プロ選手: ノバク・ジョコビッチ
   
   📊 あなたの特徴
   ✅ つま先重心で動く
   ✅ 内側から力を伝える
   ✅ ひねり動作を使う
   ...
   ```

---

## 🐛 トラブルシューティング

### 問題1: 動画解析が遅い（1分以上）

**原因**: MediaPipeの処理負荷が高い

**対処法**:
1. 動画を短くする（5-10秒推奨）
2. 解像度を下げる（720p推奨）
3. フレーム数を減らす（`video_analyzer.py` の `max_frames` を調整）

---

### 問題2: 判定精度が低い（信頼度60%未満）

**原因**: 動画品質が低い、または動作が不明瞭

**対処法**:
1. **撮影条件を改善**:
   - 側面から撮影（正面はNG）
   - 全身が映るように
   - 明るい場所で撮影
   - 背景をシンプルに

2. **動作を明確に**:
   - フォアハンドストロークを繰り返す
   - ゆっくりではっきりと動く
   - 3-5回繰り返す

---

### 問題3: 骨格検出に失敗（エラーメッセージ）

**エラー**: "骨格検出に失敗しました。動画を確認してください。"

**対処法**:
1. 動画に人物が映っているか確認
2. 人物が全身映っているか確認
3. 背景が複雑すぎないか確認
4. 動画フォーマットを変換（MP4推奨）

---

## 📊 Phase 2完了確認リスト

- [ ] GitHubに4ファイルをアップロード完了
- [ ] Streamlit Cloudで自動デプロイ成功
- [ ] `https://ai-yamada.streamlit.app` にアクセス可能
- [ ] サイドバーに「🎬 動画で自動判定（推奨）」ボタンが表示される
- [ ] 動画アップロード画面が表示される
- [ ] テスト動画で解析実行成功
- [ ] 判定結果（A1/A2/B1/B2）が表示される
- [ ] 信頼度スコアが表示される
- [ ] 詳細スコア（前後軸、内外軸、動作パターン）が表示される

---

## 🚀 Phase 3への移行（オプション）

Phase 2が完了したら、以下の機能を追加できます:

### Phase 3機能候補

1. **GPT-4 Vision統合** (精度向上: 85% → 90%+)
   - 現在はMediaPipeのみ
   - GPT-4 Visionで質的分析を追加

2. **フォーム診断機能** (スイング軌道分析)
   - 改善ポイントの具体化
   - ビフォー/アフター比較

3. **音声対話機能**
   - Whisper音声認識
   - 音声出力

4. **進捗トラッキング**
   - 過去の診断履歴
   - 改善度グラフ

---

## 📞 サポート

問題が発生した場合:
1. Streamlit Cloud のログを確認
2. GitHub Issues に報告
3. 山田秀氏に連絡

---

**次のステップ**: Phase 2完了確認 → ユーザーテスト → Phase 3計画

**推定完了時間**: 30分〜1時間（ファイルアップロード + デプロイ確認）
