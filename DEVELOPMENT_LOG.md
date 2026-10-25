# CampusLens AI — Development Log

Tracking development progress, time invested, implementation status, and lessons learned.

## Project Information

- **Project:** CampusLens AI
- **Type:** Source-Grounded Academic Document Assistant
- **Tech Stack:** Python, FastAPI, Streamlit, PyMuPDF, scikit-learn, SQLite, python-pptx, python-docx
- **Development Approach:** Solo project

## Work Sessions

| Date       | Work Completed                                                                                                                                                                                                     | Status                                                                      | Time Spent         |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------ |
| 2026-10-21 | Set up the Python environment and dependencies; implemented PDF text extraction, text chunking, TF-IDF retrieval, initial retrieval-based answering, FastAPI health endpoint, and initial Streamlit interface.     | Implemented                                                                 | 2 hours 30 minutes |
| 2026-10-24 | Added PDF upload to the Streamlit interface and tested the upload workflow. Implemented PDF text extraction and preserved page references. Commits included `6d07f52` and `8a1b47a`.                               | Implemented and tested                                                      | Not recorded       |
| 2026-10-25 | Added PowerPoint and Word document extraction using `python-pptx` and `python-docx`. Updated the interface to accept PDF, PPTX, and DOCX files. Successfully tested all three upload formats.                      | Implemented and tested                                                      | Not recorded       |
| 2026-10-25 | Improved extracted-text presentation with whitespace cleanup, paragraph spacing, Markdown headings, list formatting, and table presentation.                                                                       | Implemented; formatting needs further evaluation across different documents | Not recorded       |
| 2026-10-25 | Added detection of short and detailed answer requests and experimented with topic-relevance ranking, passage selection, and duplicate filtering. Identified remaining problems with relevance and source ordering. | Implemented; answer quality not yet verified                                | Not recorded       |

## Current Capabilities

- Upload PDF, PowerPoint (`.pptx`), and Word (`.docx`) files.
- Extract readable text from supported documents.
- Preserve PDF page references and PowerPoint slide references during extraction.
- Preview extracted document content in Streamlit.
- Search document chunks using TF-IDF similarity.
- Return retrieved passages with source references.
- Detect requests for short or detailed answers.
- Display formatted Markdown content in the interface.

## Known Limitations

- The current answerer retrieves and organizes passages; it does not yet generate complete, new explanations using a generative AI model.
- Detailed questions may retrieve unrelated passages or present relevant passages in an unsuitable order.
- Source metadata may be lost during chunking, causing some PowerPoint or Word references to display as page references.
- Heading detection depends partly on formatting in the original document.
- Scanned PDFs and text embedded in images are not currently handled by the existing text-extraction workflow.
- The application has not yet been comprehensively evaluated against a set of test questions.

## Upcoming Milestones

- [ ] Improve topic-specific retrieval and passage ordering.
- [ ] Ensure short answers remain concise and detailed answers remain focused on the requested topic.
- [ ] Preserve page, slide, and document source metadata throughout chunking and retrieval.
- [ ] Improve document formatting and heading detection across PDF, PPTX, and DOCX files.
- [ ] Display a clear message when the uploaded document contains insufficient information.
- [ ] Evaluate an optional AI-assisted mode for generating explanations and finding reliable external educational sources.
- [ ] Add automated tests for document extraction, retrieval relevance, answer length, and source references.
- [ ] Complete documentation and prepare a project demonstration.

## Development Notes

- PDF, PPTX, and DOCX upload and extraction were tested successfully on 2026-10-25.
- The answer-quality changes made on 2026-10-25 still require testing.
- External information, if introduced in a future AI-assisted mode, should be clearly distinguished from content retrieved from the uploaded document.
- Development time is recorded only when it can be established reliably.
