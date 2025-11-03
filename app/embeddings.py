# app/embeddings.py
from sklearn.metrics.pairwise import cosine_similarity as cos_sim
import numpy as np
import hashlib

def get_embeddings(text: str):
    # Dummy text embedding using hashing (for local testing)
    return np.array([hashlib.sha256(text.encode()).hexdigest()], dtype=object)

def cosine_similarity(vec1, vec2):
    # Simple numeric similarity mock
    if vec1[0] == vec2[0]:
        return 1.0
    return 0.45  # random similarity for testing