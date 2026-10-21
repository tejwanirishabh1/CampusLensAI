
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

st.info(
    "The interface is under development. "
    "PDF processing and question answering will be connected next."
)
