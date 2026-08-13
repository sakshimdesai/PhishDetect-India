from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


def create_tfidf_vectorizer():
    """Create the TF-IDF vectorizer used by the SMS model."""

    return TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=1000
    )


def save_vectorizer(vectorizer, path):
    """Save a fitted TF-IDF vectorizer."""

    joblib.dump(vectorizer, path)


def load_vectorizer(path):
    """Load a saved TF-IDF vectorizer."""

    return joblib.load(path)