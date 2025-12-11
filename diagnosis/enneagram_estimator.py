"""
エニアグラム診断エンジン: 90問ステルス推定(70%精度)
"""
from typing import Dict, List, Optional, Tuple
import random

class EnneagramEstimator:
    """エニアグラム タイプ推定器"""
    
    def __init__(self, questions: List[Dict], patterns: Dict):
        self.questions = questions
        self.patterns = patterns
        self.conversation_history = []
        self.scores = {i: 0 for i in range(1, 10)}  # タイプ1-9
        self.asked_questions = set()
        self.confidence = 0.0
        self.estimated_type = None
    
    def get_next_question(self, context: str = "") -> Optional[str]:
        """
        会話文脈から次の質問を選択(ステルス推定)
        
        Args:
            context: 現在の会話文脈
            
        Returns:
            次の質問文 or None(推定完了時)
        """
        # 推定完了判定(信頼度70%以上 or 30問到達)
        if self.confidence >= 0.70 or len(self.asked_questions) >= 30:
            return None
        
        # 未使用の質問からランダムに選択
        available = [q for q in self.questions if q['number'] not in self.asked_questions]
        
        if not available:
            return None
        
        # 文脈に応じた質問選択(簡易版: ランダム)
        question = random.choice(available)
        self.asked_questions.add(question['number'])
        
        return question['text']
    
    def process_answer(self, question: str, answer: str, user_message: str) -> Dict:
        """
        回答を処理してスコア更新
        
        Args:
            question: 質問文
            answer: ユーザーの回答
            user_message: ユーザーの元メッセージ
            
        Returns:
            更新後の診断状態
        """
        self.conversation_history.append({
            "question": question,
            "answer": answer,
            "message": user_message
        })
        
        # スコア更新(簡易版: キーワードベース)
        self._update_scores(answer, user_message)
        
        # 推定タイプ計算
        self._calculate_estimation()
        
        return {
            "estimated_type": self.estimated_type,
            "confidence": self.confidence,
            "scores": self.scores.copy(),
            "questions_asked": len(self.asked_questions),
            "total_questions": len(self.questions)
        }
    
    def _update_scores(self, answer: str, message: str):
        """回答からスコアを更新"""
        text = (answer + " " + message).lower()
        
        # タイプ別キーワード(簡易版)
        keywords = {
            1: ["完璧", "正しい", "ルール", "間違い", "べき"],
            2: ["人", "助ける", "支える", "必要", "喜ぶ"],
            3: ["成功", "達成", "目標", "認められ", "結果"],
            4: ["自分らしさ", "特別", "個性", "感情", "理解"],
            5: ["知識", "分析", "理解", "考える", "観察"],
            6: ["安全", "不安", "信頼", "準備", "心配"],
            7: ["楽しい", "新しい", "可能性", "ワクワク", "自由"],
            8: ["強さ", "コントロール", "リーダー", "正義", "戦う"],
            9: ["平和", "調和", "落ち着き", "穏やか", "バランス"]
        }
        
        for type_num, words in keywords.items():
            for word in words:
                if word in text:
                    self.scores[type_num] += 1
    
    def _calculate_estimation(self):
        """現在のスコアから推定タイプと信頼度を計算"""
        if not self.scores:
            return
        
        # トップタイプを取得
        sorted_types = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        top_type, top_score = sorted_types[0]
        second_score = sorted_types[1][1] if len(sorted_types) > 1 else 0
        
        # 信頼度計算: (トップスコア - 2位スコア) / 質問数
        if len(self.asked_questions) > 0:
            score_diff = top_score - second_score
            self.confidence = min(score_diff / len(self.asked_questions), 1.0)
        
        self.estimated_type = top_type if self.confidence >= 0.3 else None
    
    def get_type_message(self, type_num: Optional[int] = None) -> str:
        """タイプ別メッセージを取得"""
        target_type = type_num or self.estimated_type
        
        if target_type is None or target_type not in self.patterns:
            return "まだタイプを推定できていません。もう少し会話を続けましょう。"
        
        return self.patterns[target_type]
    
    def get_diagnosis_summary(self) -> Dict:
        """診断結果サマリーを取得"""
        return {
            "estimated_type": self.estimated_type,
            "confidence": round(self.confidence * 100, 1),
            "questions_asked": len(self.asked_questions),
            "top3_types": sorted(
                self.scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3],
            "message": self.get_type_message()
        }
