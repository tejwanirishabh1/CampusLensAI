
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_relevant_chunks(query, chunks, top_k=3):
    """Return the most relevant text chunks for a search query."""

    if not query.strip() or not chunks:
        return []

    documents = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(stop_words="english")
    document_vectors = vectorizer.fit_transform(documents + [query])

    similarities = cosine_similarity(
        document_vectors[-1],
        document_vectors[:-1]
    ).flatten()

    ranked_indices = similarities.argsort()[::-1]

    results = []

    for index in ranked_indices:
        if similarities[index] <= 0:
            continue

        result = chunks[index].copy()
        result["score"] = float(similarities[index])
        results.append(result)

        if len(results) >= top_k:
            break

    return results
