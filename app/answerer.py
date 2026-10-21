
from app.retrieval import retrieve_relevant_chunks


def answer_question(query, chunks, top_k=3):
    """Answer a question using relevant passages from the document."""

    results = retrieve_relevant_chunks(query, chunks, top_k=top_k)

    if not results:
        return {
            "answer": "I couldn't find relevant information in the provided document.",
            "sources": []
        }

    answer_parts = []

    for result in results:
        answer_parts.append(
            f"[Page {result['page']}] {result['text']}"
        )

    return {
        "answer": "\n\n".join(answer_parts),
        "sources": [
            {
                "page": result["page"],
                "text": result["text"],
                "score": result["score"]
            }
            for result in results
        ]
    }
