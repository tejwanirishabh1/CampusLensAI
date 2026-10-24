
import streamlit as st

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
else:
    st.info("Please upload a PDF document to get started.")
