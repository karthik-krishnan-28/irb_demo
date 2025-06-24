import streamlit as st
import fitz 

st.set_page_config(page_title="PDF to Editable Text", layout="wide")
st.title("📄 Protocol/Template Uploader + Text Converter")

uploaded_file = st.file_uploader("Upload a PDF protocol or template", type=["pdf"])

if uploaded_file:
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Load and convert PDF to text
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = "\n\n".join([page.get_text() for page in doc])

    # Editable text area
    st.subheader("📝 Editable Text Output")
    edited_text = st.text_area("You can review and edit the extracted text here:", value=text, height=600)

    # Prepare for download
    filename = uploaded_file.name.replace(".pdf", ".txt")
    st.download_button(
        label="📥 Download Text File",
        data=edited_text,
        file_name=filename,
        mime="text/plain"
    )
