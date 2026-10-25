import os
import tempfile
import streamlit as st

from app.document_parser import extract_text_from_document
from app.chunker import chunk_pages
from app.answerer import answer_question


st.set_page_config(
    page_title="CampusLens AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 CampusLens AI")
st.subheader("Your Academic Document Assistant")

st.write(
    "Upload PDFs, PowerPoint presentations, or Word documents "
    "and ask questions about their contents."
)

st.divider()

st.header("📄 Upload Your Study Material")

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "pptx", "docx"],
    help="Supported formats: PDF, PPTX, and DOCX."
)

if uploaded_file is not None:
    st.success("Document uploaded successfully!")

    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    st.write("**Filename:**", uploaded_file.name)
    st.write(
        "**File size:**",
        f"{uploaded_file.size / 1024:.2f} KB"
    )

    if st.button("Process Document"):
        temporary_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temporary_file:
                temporary_file.write(uploaded_file.getvalue())
                temporary_path = temporary_file.name

            extracted_sections = extract_text_from_document(
                temporary_path
            )

            if extracted_sections:
                chunks = chunk_pages(extracted_sections)

                st.session_state["document_chunks"] = chunks
                st.session_state["document_name"] = uploaded_file.name
                st.session_state["document_type"] = file_extension

                st.success("Document processed successfully!")

                st.write(
                    f"**Sections extracted:** {len(extracted_sections)}"
                )
                st.write(f"**Text chunks created:** {len(chunks)}")

                with st.expander("📖 Preview extracted text", expanded=True):
                    for section in extracted_sections:
                        source_type = section.get("source_type", "page")

                        if source_type == "slide":
                            label = f"Slide {section['page']}"
                        elif source_type == "document":
                            label = "Word Document"
                        else:
                            label = f"Page {section['page']}"

                        st.markdown(f"### {label}")

                        # Render headings, lists, and spacing.
                        display_text = section.get(
                            "display_text",
                            section["text"]
                        )

                        st.markdown(
                            display_text,
                            unsafe_allow_html=False
                        )

                        st.divider()

            else:
                st.session_state.pop("document_chunks", None)
                st.session_state.pop("document_name", None)
                st.session_state.pop("document_type", None)

                st.warning(
                    "No readable text was found in this document."
                )

        except Exception as error:
            st.error(f"Could not process this document: {error}")

        finally:
            if temporary_path and os.path.exists(temporary_path):
                os.remove(temporary_path)

st.divider()

st.header("💬 Ask Your Document")

if "document_chunks" in st.session_state:
    st.caption(
        f"Current document: {st.session_state['document_name']}"
    )

    question = st.text_input(
        "Enter your question",
        placeholder="e.g. Explain the main concept in this document."
    )

    if st.button("Get Answer"):
        if question.strip():
            with st.spinner("Searching your document..."):
                result = answer_question(
                    question,
                    st.session_state["document_chunks"]
                )

            st.subheader("Answer")

            if result["sources"]:
                st.markdown(
                    result["answer"],
                    unsafe_allow_html=False
                )

                st.subheader("📚 Sources")

                for source in result["sources"]:
                    source_type = source.get("source_type", "page")

                    if source_type == "slide":
                        label = f"Slide {source['page']}"
                    elif source_type == "document":
                        label = "Word Document"
                    else:
                        label = f"Page {source['page']}"

                    with st.expander(label):
                        st.markdown(
                            source["text"],
                            unsafe_allow_html=False
                        )
                        st.caption(
                            f"Relevance score: {source['score']:.4f}"
                        )
            else:
                st.info(result["answer"])
        else:
            st.warning("Please enter a question first.")

else:
    st.info(
        "Upload a document and click 'Process Document' "
        "before asking questions."
    )