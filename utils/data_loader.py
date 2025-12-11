"""
データローダー: MDファイルから診断データを読み込む
"""
from pathlib import Path
from typing import Dict, List, Optional
import re

class DataLoader:
    """AI山田v6.0用データローダー"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self._cache = {}
    
    def load_instructions(self) -> str:
        """AI山田v5.2.1 Instructionsを読み込み"""
        path = self.data_dir / "AI山田_v5.2.1_Instructions.md"
        return self._load_file(path)
    
    def load_enneagram_data(self) -> Dict:
        """エニアグラムデータを読み込み"""
        path = self.data_dir / "YAMADA_AI_COMPLETE_PACKAGE.md"
        content = self._load_file(path)
        
        return {
            "full_content": content,
            "questions": self._extract_enneagram_questions(content),
            "patterns": self._extract_enneagram_patterns(content)
        }
    
    def load_fourstance_data(self) -> Dict:
        """4スタンスデータを読み込み"""
        # v1.6が最新版
        questions_path = self.data_dir / "yamada_4stance_conversational_questions_v1.6.md"
        database_path = self.data_dir / "yamada_4stance_serve_database_v1.0.md"
        
        questions_content = self._load_file(questions_path)
        database_content = self._load_file(database_path)
        
        return {
            "questions": questions_content,
            "database": database_content,
            "question_list": self._extract_fourstance_questions(questions_content)
        }
    
    def load_tennis_methods(self) -> str:
        """35種テニスメソッドを読み込み"""
        # 完全再現パッケージから取得
        path = self.data_dir / "完全再現パッケージ.md"
        return self._load_file(path)
    
    def _load_file(self, path: Path) -> str:
        """ファイル読み込み(キャッシュ付き)"""
        if path in self._cache:
            return self._cache[path]
        
        if not path.exists():
            raise FileNotFoundError(f"データファイルが見つかりません: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._cache[path] = content
        return content
    
    def _extract_enneagram_questions(self, content: str) -> List[Dict]:
        """エニアグラム90問を抽出"""
        questions = []
        # パターン: Q数字. 質問文
        pattern = r'Q(\d+)\.\s*(.+?)(?=\n(?:Q\d+\.|#|$))'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            q_num = int(match.group(1))
            q_text = match.group(2).strip()
            questions.append({
                "number": q_num,
                "text": q_text
            })
        
        return questions[:90]  # 最大90問
    
    def _extract_enneagram_patterns(self, content: str) -> Dict:
        """エニアグラム81パターンメッセージを抽出"""
        patterns = {}
        # タイプごとのメッセージを抽出
        type_pattern = r'##\s*タイプ(\d+).*?\n(.+?)(?=##\s*タイプ\d+|$)'
        matches = re.finditer(type_pattern, content, re.DOTALL)
        
        for match in matches:
            type_num = int(match.group(1))
            message = match.group(2).strip()
            patterns[type_num] = message
        
        return patterns
    
    def _extract_fourstance_questions(self, content: str) -> List[Dict]:
        """4スタンス112問を抽出"""
        questions = []
        # パターン: Q数字. 質問文
        pattern = r'Q(\d+)\.\s*(.+?)(?:\n|$)'
        matches = re.finditer(pattern, content, re.MULTILINE)
        
        for match in matches:
            q_num = int(match.group(1))
            q_text = match.group(2).strip()
            
            # カテゴリ判定(Part 1: A/B, Part 2: Cross/Parallel)
            category = "AB" if q_num <= 70 else "CrossParallel"
            
            questions.append({
                "number": q_num,
                "text": q_text,
                "category": category
            })
        
        return questions[:112]  # 最大112問
