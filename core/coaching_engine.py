"""
AI山田v6.0 コーチングエンジン
AI山田v5.2.1の全機能 + エニアグラム + 4スタンス診断を統合
"""
from typing import Dict, List, Optional
import os
from openai import OpenAI

class YamadaCoachingEngine:
    """AI山田 コーチングエンジン"""
    
    def __init__(
        self,
        openai_api_key: str,
        instructions: str,
        enneagram_estimator,
        fourstance_estimator,
        model: str = "gpt-4o-mini"
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
        self.instructions = instructions
        
        # 診断エンジン
        self.enneagram = enneagram_estimator
        self.fourstance = fourstance_estimator
        
        # 会話履歴
        self.messages = []
        
        # 状態管理
        self.emotion_level = "ポジティブ"  # ポジティブ/葛藤/深刻
        self.gennari_count = 0  # げんなりカウンター
        self.current_phase = "greeting"  # greeting/meta_outcome/grow/diagnosis/advice
        
    def generate_system_prompt(self) -> str:
        """
        動的システムプロンプト生成
        診断結果を反映した統合プロンプトを作成
        """
        base_prompt = self.instructions
        
        # エニアグラム診断結果を追加
        enneagram_info = ""
        if self.enneagram.estimated_type:
            enneagram_summary = self.enneagram.get_diagnosis_summary()
            enneagram_info = f"""
## エニアグラム診断結果(推定)
- タイプ: {enneagram_summary['estimated_type']}
- 信頼度: {enneagram_summary['confidence']}%
- 特徴: {enneagram_summary['message'][:100]}...

**コーチング方針**: このタイプの特性を考慮し、相手の本質的な動機に響くアドバイスを提供してください。
"""
        
        # 4スタンス診断結果を追加
        fourstance_info = ""
        if self.fourstance.estimated_type:
            fourstance_summary = self.fourstance.get_diagnosis_summary()
            type_info = fourstance_summary['type_info']
            fourstance_info = f"""
## 4スタンス診断結果(推定)
- タイプ: {type_info['type']}
- 信頼度: {fourstance_summary['confidence']}%
- 特徴: {type_info['characteristics']}
- 参考プロ: {', '.join(type_info['pro_players'])}
- アドバイス: {type_info['advice']}

**コーチング方針**: この身体タイプに最適化されたテニス技術アドバイスを提供してください。
"""
        
        # 統合プロンプト
        integrated_prompt = f"""{base_prompt}

---
# 診断システム統合情報

{enneagram_info}

{fourstance_info}

---
# 重要な指示

1. **診断はバックエンド分析ツール**: ユーザーに診断結果を直接伝えず、コーチングに自然に活かす
2. **会話に溶け込ませる**: 質問ベースの診断は、自然な会話の中で2-3問ずつ混ぜる
3. **統合アドバイス**: エニアグラム×4スタンス×感情レベル×テニスメソッドを組み合わせる
4. **15パターン対応**: 本質到達判定、経路A/B配分など、確認済みパターンを適用
5. **げんなりサイン検出**: ユーザーの疲労を感知したら、すぐにペースダウン

現在の感情レベル: {self.emotion_level}
現在のフェーズ: {self.current_phase}
"""
        
        return integrated_prompt
    
    def chat(self, user_message: str) -> str:
        """
        メインチャット処理
        
        Args:
            user_message: ユーザーメッセージ
            
        Returns:
            AI山田の応答
        """
        # げんなりサイン検出
        self._detect_gennari(user_message)
        
        # 感情レベル判定
        self._detect_emotion_level(user_message)
        
        # 診断質問の処理(バックグラウンド)
        self._process_diagnosis(user_message)
        
        # システムプロンプト生成
        system_prompt = self.generate_system_prompt()
        
        # メッセージ履歴に追加
        self.messages.append({"role": "user", "content": user_message})
        
        # OpenAI API呼び出し
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *self.messages
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def _detect_emotion_level(self, message: str):
        """感情レベル検出"""
        text = message.lower()
        
        # 深刻モードキーワード
        serious_keywords = ["辞めたい", "もう無理", "できない", "絶望", "最悪"]
        if any(word in text for word in serious_keywords):
            self.emotion_level = "深刻"
            return
        
        # 葛藤モードキーワード
        conflict_keywords = ["でも", "だけど", "難しい", "うまくいかない", "悩んでいる"]
        if any(word in text for word in conflict_keywords):
            self.emotion_level = "葛藤"
            return
        
        # デフォルトはポジティブ
        self.emotion_level = "ポジティブ"
    
    def _detect_gennari(self, message: str):
        """げんなりサイン検出"""
        gennari_keywords = ["疲れた", "もういい", "わからない", "別に", "はい"]
        
        if any(word in message.lower() for word in gennari_keywords):
            self.gennari_count += 1
        else:
            self.gennari_count = max(0, self.gennari_count - 1)
    
    def _process_diagnosis(self, user_message: str):
        """診断処理(バックグラウンド)"""
        # エニアグラム診断
        if self.enneagram.confidence < 0.70:
            next_q = self.enneagram.get_next_question(user_message)
            if next_q:
                # 質問を会話に溶け込ませる(実際の質問はシステムプロンプトで指示)
                self.enneagram.process_answer(next_q, user_message, user_message)
        
        # 4スタンス診断
        if self.fourstance.confidence < 0.75:
            next_q = self.fourstance.get_next_question(user_message)
            if next_q:
                self.fourstance.process_answer(next_q, user_message, user_message)
    
    def get_diagnosis_status(self) -> Dict:
        """診断状況を取得"""
        return {
            "enneagram": self.enneagram.get_diagnosis_summary(),
            "fourstance": self.fourstance.get_diagnosis_summary(),
            "emotion_level": self.emotion_level,
            "gennari_count": self.gennari_count,
            "current_phase": self.current_phase
        }
    
    def reset(self):
        """セッションリセット"""
        self.messages = []
        self.emotion_level = "ポジティブ"
        self.gennari_count = 0
        self.current_phase = "greeting"
