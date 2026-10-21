
from pathlib import Path

from app.document_parser import extract_text_from_pdf
from app.chunker import chunk_pages
from app.answerer import answer_question


pdf_path = Path("sample_documents/AJAX_MidSem_Answers.pdf")

pages = extract_text_from_pdf(pdf_path)
chunks = chunk_pages(pages)

query = "What is the role of XMLHttpRequest in AJAX?"

result = answer_question(query, chunks)

print(f"Question: {query}")
print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(f"Page: {source['page']}")
    print(f"Relevance score: {source['score']:.4f}")
