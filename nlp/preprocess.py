import re
import string

# A simple English stopword list (you can expand this later)
STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were",
    "in", "on", "at", "for", "of", "to", "and", "or", "but",
    "with", "from", "by", "as", "that", "this", "these", "those",
    "it", "its", "be", "been", "being",
    "i", "you", "he", "she", "we", "they", "them",
    "your", "our", "their",
    "have", "has", "had", "do", "does", "did",
    "will", "would", "can", "could", "should",
    "about", "into", "over", "under", "up", "down",
    "not", "no", "yes"
}

def clean_text(text: str) -> str:
    """
    Lowercase, remove punctuation, numbers and extra spaces.
    """
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Replace URLs and email addresses (optional, keeps things cleaner)
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove numbers
    text = re.sub(r"\d+", " ", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Collapse multiple spaces into one
    text = re.sub(r"\s+", " ", text).strip()

    return text

def tokenize(text: str) -> list:
    """
    Split cleaned text into individual tokens (words).
    """
    if not text:
        return []
    return text.split(" ")

def remove_stopwords(tokens: list) -> list:
    """
    Remove common stopwords from the token list.
    """
    if not tokens:
        return []
    return [t for t in tokens if t and t not in STOPWORDS]

def preprocess(text: str) -> dict:
    """
    Full preprocessing pipeline:
    - clean text
    - tokenize
    - remove stopwords

    Returns:
        {
            "clean_text": "...",
            "tokens": [...],
        }
    """
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens_no_stop = remove_stopwords(tokens)

    return {
        "clean_text": " ".join(tokens_no_stop),
        "tokens": tokens_no_stop,
    }

# Quick manual test
if __name__ == "__main__":
    sample_text = """
    I am a B.Tech CSE student with experience in Python, SQL and Machine Learning.
    I have worked on data analysis and API integration in multiple academic projects.
    """
    result = preprocess(sample_text)
    print("CLEAN TEXT:\n", result["clean_text"])
    print("\nTOKENS:\n", result["tokens"])
