import os
import pickle
from wordfreq import top_n_list
import Levenshtein
from time import perf_counter

# -----------------------------
# Config
# -----------------------------
PICKLE_PATH = "words.pkl"
MAX_DISTANCE = 4  # max Levenshtein distance for typo correction
TOP_N = 32000     # number of top words to load per language

# -----------------------------
# Load or build word list
# -----------------------------
def load_or_build_wordlist():
    if os.path.exists(PICKLE_PATH):
        with open(PICKLE_PATH, "rb") as f:
            print("[INFO] Loading cached word lists...")
            return pickle.load(f)
    else:
        print("[INFO] Generating word lists (first time)...")
        data = {
            "en": set(top_n_list("en", TOP_N)),
            "id": set(top_n_list("id", TOP_N))
        }
        with open(PICKLE_PATH, "wb") as f:
            pickle.dump(data, f)
        print("[INFO] Word lists cached successfully.")
        return data

# -----------------------------
# Levenshtein typo correction
# -----------------------------
def get_closest_word(word, dictionary, max_distance=MAX_DISTANCE):
    if word in dictionary:
        return word
    # filter candidates with length difference <= max_distance
    candidates = [(w, Levenshtein.distance(word, w))
                  for w in dictionary if abs(len(w) - len(word)) <= max_distance]
    candidates = [c for c in candidates if c[1] <= max_distance]
    if not candidates:
        return word  # no close match found
    return min(candidates, key=lambda x: x[1])[0]

# -----------------------------
# Simple language detection
# -----------------------------
def detect_language(words, en_words, id_words):
    en_count = sum(1 for w in words if w in en_words)
    id_count = sum(1 for w in words if w in id_words)
    return "id" if id_count > en_count else "en"

# -----------------------------
# Correct sentence
# -----------------------------
def correct_sentence(sentence, en_words, id_words):
    words = [w.lower() for w in sentence.split()]
    lang = detect_language(words, en_words, id_words)
    dictionary = id_words if lang == "id" else en_words
    corrected = [get_closest_word(w, dictionary) for w in words]
    return " ".join(corrected), lang

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    start_time = perf_counter()

    # Load word lists
    data = load_or_build_wordlist()
    en_words = data["en"]
    id_words = data["id"]

    # Sample sentences with typos
    sentences = [
        "plase giv me a repot for january",      # English typo
        "tolong berikn laporn bulan januari"    # Indonesian typo
    ]

    for s in sentences:
        corrected, lang = correct_sentence(s, en_words, id_words)
        print(f"[{lang}] Original : {s}")
        print(f"[{lang}] Corrected: {corrected}\n")

    total_time = perf_counter() - start_time
    print(f"Total processing time: {total_time:.3f} seconds")
