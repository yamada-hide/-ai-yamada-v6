"""
AI山田v6.0 設定ファイル
"""
import os
from pathlib import Path

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent

# データディレクトリ
DATA_DIR = PROJECT_ROOT / "data"

# OpenAI設定
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.7

# 診断設定
DIAGNOSIS_CONFIG = {
    "enneagram": {
        "total_questions": 90,
        "target_accuracy": 0.70,
        "patterns": 81
    },
    "fourstance": {
        "total_questions": 112,
        "target_accuracy": 0.80,
        "types": ["A1", "A2", "B1", "B2"]
    }
}

# コーチング設定
COACHING_CONFIG = {
    "meta_outcome_questions": 6,
    "grow_questions": 50,
    "emotion_levels": ["ポジティブ", "葛藤", "深刻"],
    "patterns": 15,
    "tennis_methods": 35
}
