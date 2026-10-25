import re

from app.retrieval import retrieve_relevant_chunks


STOP_WORDS = {
    "what", "is", "are", "the", "a", "an", "of", "to", "in",
    "on", "for", "and", "or", "it", "its", "this", "that",
    "with", "by", "from", "about", "explain", "describe",
    "briefly", "brief", "short", "detail", "detailed",
    "give", "me", "please", "tell", "show", "define",
    "how", "does", "do", "can", "you", "i", "as",
}


def detect_answer_length(query):
    """Identify whether the user wants a short or detailed answer."""

    question = query.lower()

    short_phrases = (
        "in short",
        "briefly",
        "short answer",
        "in brief",
        "few words",
        "keep it short",
    )

    detailed_phrases = (
        "in detail",
        "in details",
        "detailed answer",
        "explain fully",
        "elaborate",
        "step by step",
        "step-by-step",
        "in depth",
        "comprehensive",
    )

    if any(phrase in question for phrase in short_phrases):
        return "short"

    if any(phrase in question for phrase in detailed_phrases):
        return "detailed"

    return "normal"


def extract_topic_terms(query):
    """Extract meaningful terms from the user's question."""

    words = re.findall(r"[a-zA-Z0-9]+", query.lower())

    return {
        word for word in words
        if word not in STOP_WORDS and len(word) > 1
    }


def sentence_list(text):
    """Split a passage into readable sentences."""

    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]


def topic_relevance(text, topic_terms):
    """Estimate how strongly a passage relates to the requested topic."""

    words = set(re.findall(r"[a-zA-Z0-9]+", text.lower()))

    if not topic_terms:
        return 0.0

    matches = len(topic_terms & words)

    return matches / len(topic_terms)


def clean_answer_text(text):
    """Clean excessive whitespace without changing the wording."""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def answer_question(query, chunks, top_k=None):
    """
    Retrieve and organize relevant passages from the uploaded document.

    This function does not invent information missing from the source.
    """

    if not query or not query.strip():
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    answer_length = detect_answer_length(query)
    topic_terms = extract_topic_terms(query)

    if top_k is None:
        if answer_length == "short":
            top_k = 3
        elif answer_length == "detailed":
            top_k = 12
        else:
            top_k = 5

    retrieved = retrieve_relevant_chunks(
        query,
        chunks,
        top_k=max(top_k * 3, 15),
    )

    if not retrieved:
        return {
            "answer": (
                "There is no relevant information about this topic "
                "in the uploaded document."
            ),
            "sources": [],
        }

    # Rank results using both retrieval similarity and topic overlap.
    ranked_results = []

    for result in retrieved:
        text = result.get("text", "").strip()

        if not text:
            continue

        relevance = topic_relevance(text, topic_terms)

        similarity = result.get("score", 0.0)

        combined_score = (0.65 * similarity) + (0.35 * relevance)

        ranked_results.append({
            **result,
            "topic_relevance": relevance,
            "combined_score": combined_score,
        })

    ranked_results.sort(
        key=lambda item: item["combined_score"],
        reverse=True,
    )

    # Exclude passages with no meaningful overlap with the topic.
    relevant_results = [
        result for result in ranked_results
        if result["topic_relevance"] > 0
    ]

    if not relevant_results:
        return {
            "answer": (
                "There is no relevant information about this topic "
                "in the uploaded document."
            ),
            "sources": [],
        }

    # Keep highly relevant passages and avoid duplicate passages.
    selected_results = []
    seen_texts = set()

    minimum_relevance = 0.20

    for result in relevant_results:
        if result["topic_relevance"] < minimum_relevance:
            continue

        normalized_text = re.sub(
            r"\W+",
            " ",
            result["text"].lower(),
        ).strip()

        if not normalized_text or normalized_text in seen_texts:
            continue

        seen_texts.add(normalized_text)
        selected_results.append(result)

        if len(selected_results) >= top_k:
            break

    if not selected_results:
        return {
            "answer": (
                "There is no relevant information about this topic "
                "in the uploaded document."
            ),
            "sources": [],
        }

    # For short answers, retain the most relevant passage only.
    if answer_length == "short":
        selected_results = selected_results[:1]

    # Remove sentences that do not contain any of the requested
    # topic terms, while preserving context when possible.
    answer_parts = []
    sources = []

    for result in selected_results:
        sentences = sentence_list(result["text"])

        relevant_sentences = [
            sentence for sentence in sentences
            if topic_relevance(sentence, topic_terms) > 0
        ]

        # Fall back to the original passage if sentence filtering
        # would remove all its information.
        if not relevant_sentences:
            relevant_sentences = sentences

        formatted_text = clean_answer_text(
            " ".join(relevant_sentences)
        )

        if not formatted_text:
            continue

        source_type = result.get("source_type", "page")
        source_number = result.get("page", 1)

        if source_type == "slide":
            source_label = f"Slide {source_number}"
        elif source_type == "document":
            source_label = "Word Document"
        else:
            source_label = f"Page {source_number}"

        answer_parts.append(
            f"**Source: {source_label}**\n\n{formatted_text}"
        )

        sources.append({
            "page": source_number,
            "source_type": source_type,
            "text": formatted_text,
            "score": result.get("score", 0.0),
        })

    if not answer_parts:
        return {
            "answer": (
                "There is no relevant information about this topic "
                "in the uploaded document."
            ),
            "sources": [],
        }

    return {
        "answer": "\n\n---\n\n".join(answer_parts),
        "sources": sources,
    }