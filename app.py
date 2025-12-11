"""
AI山田v6.0 - Streamlit アプリケーション
質問ベース診断システム統合版
"""
import streamlit as st
from pathlib import Path
import os

# モジュールインポート
from core.coaching_engine import YamadaCoachingEngine
from diagnosis.enneagram_estimator import EnneagramEstimator
from diagnosis.fourstance_estimator import FourStanceEstimator
from utils.data_loader import DataLoader
import config

# ページ設定
st.set_page_config(
    page_title="AI山田v6.0 - テニス&メンタルコーチング",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .diagnosis-box {
        background-color: #f0f8ff;
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .stChatMessage {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    /* チャット入力欄のスタイル */
    .stChatInputContainer {
        border-top: 2px solid #FF6B6B;
        padding-top: 1rem;
    }
    /* モバイル対応: ボタンの文字を確実に表示 */
    button {
        font-size: 16px !important;
        font-weight: 600 !important;
        min-height: 44px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    /* サイドバーのテキストをモバイルでも読みやすく */
    .sidebar .sidebar-content {
        font-size: 14px !important;
    }
    /* モバイルでのマークダウン表示を改善 */
    .stMarkdown {
        font-size: 14px !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """セッション状態の初期化"""
    if "initialized" not in st.session_state:
        # データローダー
        data_loader = DataLoader(config.DATA_DIR)
        
        # データ読み込み
        instructions = data_loader.load_instructions()
        enneagram_data = data_loader.load_enneagram_data()
        fourstance_data = data_loader.load_fourstance_data()
        
        # 診断エンジン初期化
        enneagram_estimator = EnneagramEstimator(
            questions=enneagram_data['questions'],
            patterns=enneagram_data['patterns']
        )
        
        fourstance_estimator = FourStanceEstimator(
            questions_content=fourstance_data['questions'],
            database_content=fourstance_data['database'],
            question_list=fourstance_data['question_list']
        )
        
        # コーチングエンジン初期化
        api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
        
        if not api_key:
            st.error("⚠️ OpenAI APIキーが設定されていません。サイドバーで設定してください。")
            st.stop()
        
        coaching_engine = YamadaCoachingEngine(
            openai_api_key=api_key,
            instructions=instructions,
            enneagram_estimator=enneagram_estimator,
            fourstance_estimator=fourstance_estimator,
            model=config.OPENAI_MODEL
        )
        
        # セッション状態に保存
        st.session_state.coaching_engine = coaching_engine
        st.session_state.messages = []
        st.session_state.initialized = True

def render_sidebar():
    """サイドバー描画"""
    with st.sidebar:
        st.markdown("### 🎾 AI山田v6.0")
        st.markdown("---")
        
        # APIキー設定(secretsにない場合)
        if "OPENAI_API_KEY" not in st.secrets:
            api_key = st.text_input(
                "OpenAI APIキー",
                type="password",
                help="OpenAI APIキーを入力してください"
            )
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
        
        st.markdown("---")
        
        # 診断状況表示
        if "coaching_engine" in st.session_state:
            engine = st.session_state.coaching_engine
            status = engine.get_diagnosis_status()
            
            st.markdown("### 📊 診断状況")
            
            # エニアグラム
            enneagram = status['enneagram']
            st.markdown("#### 🧠 エニアグラム")
            st.progress(enneagram['confidence'] / 100)
            st.caption(f"信頼度: {enneagram['confidence']}%")
            if enneagram['estimated_type']:
                st.success(f"推定タイプ: {enneagram['estimated_type']}")
            
            st.markdown("---")
            
            # 4スタンス
            fourstance = status['fourstance']
            st.markdown("#### 🎯 4スタンス")
            st.progress(fourstance['confidence'] / 100)
            st.caption(f"信頼度: {fourstance['confidence']}%")
            if fourstance['estimated_type']:
                st.success(f"推定タイプ: {fourstance['estimated_type']}")
            
            st.markdown("---")
            
            # 状態情報
            st.markdown("#### 💭 状態")
            st.info(f"感情レベル: {status['emotion_level']}")
            st.info(f"フェーズ: {status['current_phase']}")
        
        st.markdown("---")
        
        # リセットボタン
        if st.button("🔄 セッションリセット", use_container_width=True):
            if "coaching_engine" in st.session_state:
                st.session_state.coaching_engine.reset()
                st.session_state.messages = []
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📖 使い方")
        st.markdown("""
        1. チャットで自由に相談
        2. AIが自然な会話で診断
        3. あなたに最適化されたアドバイスを提供
        
        **特徴:**
        - 山田式性格診断(90問)
        - 山田式タイプ分け(112問)
        - 統合アドバイス生成
        """)
        
        st.markdown("---")
        st.caption("© 2025 AI山田v6.0")

def render_main():
    """メイン画面描画"""
    # ヘッダー
    st.markdown('<div class="main-title">🎾 AI山田v6.0</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">テニス&メンタルコーチング - 質問ベース診断システム</div>',
        unsafe_allow_html=True
    )
    
    # チャット履歴表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # チャット入力
    if prompt := st.chat_input("何でも相談してください!"):
        # ユーザーメッセージ表示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI応答生成
        with st.chat_message("assistant"):
            with st.spinner("考え中..."):
                engine = st.session_state.coaching_engine
                response = engine.chat(prompt)
                st.markdown(response)
        
        # アシスタントメッセージ保存
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 再描画
        st.rerun()

def main():
    """メイン関数"""
    # 初期化
    initialize_session_state()
    
    # サイドバー
    render_sidebar()
    
    # メイン画面
    render_main()

if __name__ == "__main__":
    main()
