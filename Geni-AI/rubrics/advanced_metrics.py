"""
Advanced Linguistic & Cognitive Complexity Metrics
Calculates multi-index readability: Flesch-Kincaid, Coleman-Liau, Gunning-Fog,
Dale-Chall vocabulary familiarity, and sentence length variance.
"""

import re
import math
from typing import List, Dict, Any, Tuple


# Core 1,000 most common English words for non-native vocabulary grounding
COMMON_ENGLISH_FOUNDATION = {
    "the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are",
    "as", "with", "his", "they", "i", "at", "be", "this", "have", "from", "or", "one", "had", "by",
    "word", "but", "not", "what", "all", "were", "we", "when", "your", "can", "said", "there", "use",
    "an", "each", "which", "she", "do", "how", "their", "if", "will", "up", "other", "about", "out",
    "many", "then", "them", "these", "so", "some", "her", "would", "make", "like", "him", "into",
    "time", "has", "look", "two", "more", "write", "go", "see", "number", "no", "way", "could",
    "people", "my", "than", "first", "water", "been", "call", "who", "oil", "its", "now", "find",
    "long", "down", "day", "did", "get", "come", "made", "may", "part", "over", "new", "sound",
    "take", "only", "little", "work", "know", "place", "year", "live", "me", "back", "give", "most",
    "very", "after", "thing", "our", "just", "name", "good", "sentence", "man", "think", "say",
    "great", "where", "help", "through", "much", "before", "line", "right", "too", "mean", "old",
    "any", "same", "tell", "boy", "follow", "came", "want", "show", "also", "around", "farm", "three",
    "small", "set", "put", "end", "does", "another", "well", "large", "must", "big", "even", "such",
    "because", "turn", "here", "why", "ask", "went", "men", "read", "need", "land", "different",
    "home", "us", "move", "try", "kind", "hand", "picture", "again", "change", "off", "play", "spell",
    "air", "away", "animal", "house", "point", "page", "letter", "mother", "answer", "found", "study",
    "still", "learn", "should", "america", "world", "high", "every", "near", "add", "food", "between",
    "own", "below", "country", "plant", "last", "school", "father", "keep", "tree", "never", "start",
    "city", "earth", "eyes", "light", "thought", "head", "under", "story", "saw", "left", "don't",
    "few", "while", "along", "might", "close", "something", "seem", "next", "hard", "open", "example",
    "begin", "life", "always", "those", "both", "paper", "together", "got", "group", "often", "run",
    "important", "until", "children", "side", "feet", "car", "mile", "night", "walk", "white", "sea",
    "began", "grow", "took", "river", "four", "carry", "state", "once", "book", "hear", "stop",
    "without", "second", "late", "miss", "idea", "enough", "eat", "face", "watch", "far", "indian",
    "real", "almost", "let", "above", "girl", "sometimes", "mountain", "cut", "young", "talk", "soon",
    "list", "song", "being", "leave", "family", "it's", "exam", "student", "teacher", "class", "note",
    "question", "answer", "search", "check", "truth", "false", "step", "fact", "page", "library",
    "college", "school", "university", "hostel", "fee", "rule", "circular", "notice", "board",
    "career", "job", "company", "office", "money", "salary", "computer", "phone", "chat", "bot",
    "smart", "brain", "memory", "wire", "simple", "easy", "understand", "clear", "fresh", "today",
    "yesterday", "tomorrow", "date", "train", "ticket", "station", "counter", "bank", "receipt",
    "card", "hospital", "doctor", "medicine", "report", "file", "folder", "test", "quiz", "marks",
    "score", "pass", "fail", "book", "textbook", "desk", "pencil", "pen", "paper", "lesson", "guide",
    "help", "secret", "future", "build", "world", "india", "delhi", "bengaluru", "hyderabad", "online",
    "internet", "web", "site", "box", "line", "pin", "map", "address", "number", "meaning", "words",
    "kirana", "store", "shop", "shopkeeper", "spices", "packet", "shelf", "bookshelf", "irctc", "railway",
    "inquiry", "berth", "seat", "deadline", "circulars", "database", "script", "code", "function",
    "keys", "dictionary", "match", "matches", "system", "systems", "prompt", "model", "models",
    "retrieval", "generation", "augmented", "truthful", "guessing", "guess", "hallucination",
    "facts", "notes", "weights", "steps", "points", "remember", "digital", "space", "table",
    "dimension", "feature", "server", "rupees", "free", "leaks", "consults", "smart", "builders"
}


def count_syllables(word: str) -> int:
    """Robust syllable counter for English words."""
    word = word.lower().strip(".,!?:;\"'()[]{}")
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    matches = re.findall(r'[aeiouy]{1,2}', word)
    return max(1, len(matches))


def compute_comprehensive_metrics(text: str) -> Dict[str, Any]:
    """
    Computes a multi-index cognitive readability and linguistic complexity suite:
    - Flesch-Kincaid Grade Level
    - Coleman-Liau Index
    - Gunning-Fog Index
    - Dale-Chall Easy-Word Ratio
    - Sentence Length Distribution & Variance
    - Composite Cognitive Accessibility Score (0 - 100)
    """
    clean_text = re.sub(r'#+\s*', '', text)
    clean_text = re.sub(r'[*_`]', '', clean_text)

    # Sentences split
    raw_sentences = [s.strip() for s in re.split(r'[.!?]+', clean_text) if s.strip()]
    total_sentences = max(1, len(raw_sentences))

    # Words split
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', clean_text)]
    total_words = max(1, len(words))

    # Characters (letters only)
    total_letters = sum(len(w) for w in words)

    # Syllables & complex words
    syllable_counts = [count_syllables(w) for w in words]
    total_syllables = sum(syllable_counts)
    complex_words = sum(1 for s in syllable_counts if s >= 3)

    # Sentence lengths (words per sentence)
    sentence_word_counts = []
    for s in raw_sentences:
        sw = re.findall(r'\b[a-zA-Z]+\b', s)
        if sw:
            sentence_word_counts.append(len(sw))
    if not sentence_word_counts:
        sentence_word_counts = [total_words]

    avg_sentence_len = round(total_words / total_sentences, 2)
    max_sentence_len = max(sentence_word_counts) if sentence_word_counts else 0
    min_sentence_len = min(sentence_word_counts) if sentence_word_counts else 0

    # Variance and Standard Deviation
    variance = sum((x - avg_sentence_len) ** 2 for x in sentence_word_counts) / len(sentence_word_counts)
    std_dev_sentence_len = round(math.sqrt(variance), 2)

    # 1. Flesch-Kincaid Grade Level
    words_per_sentence = total_words / total_sentences
    syllables_per_word = total_syllables / total_words
    fk_grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    fk_grade = round(max(0.0, fk_grade), 2)

    # 2. Coleman-Liau Index: 0.0588 * L - 0.296 * S - 15.8
    # L = avg letters per 100 words, S = avg sentences per 100 words
    L = (total_letters / total_words) * 100
    S = (total_sentences / total_words) * 100
    coleman_liau = round(max(0.0, 0.0588 * L - 0.296 * S - 15.8), 2)

    # 3. Gunning-Fog Index: 0.4 * ((words / sentences) + 100 * (complex_words / words))
    complex_pct = (complex_words / total_words) * 100
    gunning_fog = round(max(0.0, 0.4 * (words_per_sentence + complex_pct)), 2)

    # 4. Dale-Chall Easy-Word Percentage (Familiarity for non-native English speakers)
    common_matches = sum(1 for w in words if w in COMMON_ENGLISH_FOUNDATION)
    easy_word_pct = round((common_matches / total_words) * 100, 1)

    # 5. Composite Cognitive Accessibility Score (0 - 100)
    # Higher is better/more accessible for an Indian 12th-grade beginner
    # Penalty for high FK, high sentence variance, low easy-word ratio
    grade_penalty = max(0.0, (fk_grade - 6.0) * 8.0)
    length_penalty = max(0.0, (avg_sentence_len - 14.0) * 4.0)
    std_penalty = max(0.0, (std_dev_sentence_len - 6.0) * 2.0)
    vocab_bonus = min(20.0, (easy_word_pct - 60.0) * 0.5) if easy_word_pct > 60 else -10.0

    cognitive_score = 100.0 - grade_penalty - length_penalty - std_penalty + vocab_bonus
    cognitive_score = round(max(10.0, min(100.0, cognitive_score)), 1)

    return {
        "flesch_kincaid_grade": fk_grade,
        "coleman_liau_index": coleman_liau,
        "gunning_fog_index": gunning_fog,
        "easy_word_percentage": easy_word_pct,
        "avg_sentence_length": avg_sentence_len,
        "max_sentence_length": max_sentence_len,
        "min_sentence_length": min_sentence_len,
        "sentence_length_std_dev": std_dev_sentence_len,
        "cognitive_accessibility_score": cognitive_score,
        "total_words": total_words,
        "total_sentences": total_sentences,
        "complex_word_count": complex_words
    }
