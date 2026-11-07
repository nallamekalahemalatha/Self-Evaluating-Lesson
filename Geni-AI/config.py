"""
System Configuration & Persona Specification
Self-Evaluating RAG Lesson Content Generator - Configuration Settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MEMORY_DIR = DATA_DIR / "memory"
DELIVERABLES_DIR = BASE_DIR / "deliverables"

# Ensure runtime directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)

# Database & Storage paths
DB_PATH = MEMORY_DIR / "engine_history.db"
EVOLUTION_STORE_PATH = MEMORY_DIR / "evolved_guardrails.json"

# Target Learner Persona Specification
TARGET_PERSONA = {
    "title": "12th-Grade Graduate from India (Non-English Medium Background)",
    "education_level": "Class 12 pass-out (State Board or CBSE/ICSE non-English primary medium)",
    "language_proficiency": "Limited English vocabulary; conversational reading ability; struggles with dense academic syntax",
    "goal": "Wants to enter the AI industry, understand core GenAI concepts, and build a career",
    "cultural_anchors": [
        "Open-book exam vs closed-book memorization",
        "School/College library with a reference librarian",
        "Railway enquiry counter or Tatkal ticket booking chart update",
        "Doctor consulting a medical diagnostic reference manual"
    ],
    "pedagogical_rules": [
        "Use short sentences (maximum 15-18 words per sentence).",
        "Every single technical term must be demystified immediately with a familiar real-life analogy before using it again.",
        "Zero unexplained acronyms or mathematical formulas.",
        "Warm, respectful, encouraging tone — never condescending.",
        "Include a concrete step-by-step query walkthrough.",
        "End with a clear, active 'Check Your Understanding' mini-quiz with conversational explanations."
    ]
}

# Algorithmic Evaluation Thresholds
RUBRIC_THRESHOLDS = {
    "max_flesch_kincaid_grade": 7.5,
    "max_avg_sentence_length": 18.0,
    "min_word_count": 600,
    "max_word_count": 1800,
    "min_analogies_required": 1,
    "max_consecutive_complex_words": 2
}

# Pipeline Execution Settings
MAX_RETRIES = 2
DEFAULT_TOPIC = "Introduction to RAG (Retrieval-Augmented Generation)"

# LLM Provider Detection
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_PROVIDER = "gemini" if GEMINI_API_KEY else ("openai" if OPENAI_API_KEY else "mock")

# Models
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_MODEL = "gpt-4o-mini"
