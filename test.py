import streamlit as st
from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text

st.title("📄 CV Extractor")

uploaded_file = st.file_uploader("Upload a CV (PDF)", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted CV Text", text, height=400)