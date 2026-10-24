
import streamlit as st
import tempfile
import os

from app.document_parser import extract_text_from_pdf

st.set_page_config(
    page_title="CampusLens AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 CampusLens AI")
st.subheader("Your Academic Document Assistant")

st.write(
    "Upload academic documents and find information "
    "with source references."
)

st.divider()

st.header("📄 Upload Your Academic Document")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload a PDF document to begin."
)

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

    st.write("**Filename:**", uploaded_file.name)
    st.write(
        "**File size:**",
        f"{uploaded_file.size / 1024:.2f} KB"
    )

    if st.button("Extract Text from PDF"):
        temporary_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temporary_file:
                temporary_file.write(uploaded_file.getvalue())
                temporary_path = temporary_file.name

            pages = extract_text_from_pdf(temporary_path)

            if pages:
                st.success("Text extracted successfully!")

                for page in pages:
                    with st.expander(f"Page {page['page']}"):
                        st.text(page["text"])
            else:
                st.warning(
                    "No readable text was found in this PDF. "
                    "It may contain scanned images instead of selectable text."
                )

        except Exception as error:
            st.error(f"Could not process this PDF: {error}")

        finally:
            if temporary_path and os.path.exists(temporary_path):
                os.remove(temporary_path)

else:
    st.info("Please upload a PDF document to get started.")
