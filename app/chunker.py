
def chunk_pages(pages, chunk_size=500, overlap=100):
    """Split extracted PDF pages into smaller, overlapping text chunks."""
    chunks = []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "page": page_number,
                    "text": chunk_text
                })

            if end == len(text):
                break

            start = end - overlap

    return chunks
