import re


def chunk_pages(pages, chunk_size=500, overlap=100):
    """Split PDF pages into chunks while preserving sentence boundaries."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )

    chunks = []

    for page in pages:
        text = re.sub(r"\s+", " ", page["text"]).strip()
        page_number = page["page"]

        if not text:
            continue

        # Split text at likely sentence boundaries.
        sentences = re.split(
            r'(?<=[.!?])\s+(?=[A-Z0-9"\'])',
            text
        )

        current_sentences = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue

            # Keep unusually long sentences intact rather than cutting
            # them in the middle.
            sentence_length = len(sentence)

            if current_sentences and (
                current_length + sentence_length + 1 > chunk_size
            ):
                chunks.append({
                    "page": page_number,
                    "text": " ".join(current_sentences)
                })

                # Retain recent sentences as context for the next chunk.
                overlap_sentences = []
                overlap_length = 0

                for previous in reversed(current_sentences):
                    added_length = len(previous) + 1

                    if overlap_length + added_length > overlap:
                        break

                    overlap_sentences.insert(0, previous)
                    overlap_length += added_length

                current_sentences = overlap_sentences
                current_length = overlap_length

            current_sentences.append(sentence)
            current_length += sentence_length + 1

        if current_sentences:
            chunks.append({
                "page": page_number,
                "text": " ".join(current_sentences)
            })

    return chunks