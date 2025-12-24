import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="PDF Digital Signature Tool", layout="centered")
st.title("📄 PDF Digital Signature Automation")

pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
signature_file = st.file_uploader("Upload Signature Image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

signature_width = st.slider("Signature Width (px)", 80, 300, 150)

if pdf_file and signature_file:
    st.success("Files uploaded successfully")

    if st.button("Apply Digital Signature"):
        # Load PDF
        pdf_bytes = pdf_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Load signature image
        sig_img = Image.open(signature_file).convert("RGBA")
        sig_ratio = sig_img.height / sig_img.width
        sig_height = int(signature_width * sig_ratio)

        sig_buffer = io.BytesIO()
        sig_img.save(sig_buffer, format="PNG")
        sig_bytes = sig_buffer.getvalue()

        for page in doc:
            page_width = page.rect.width
            page_height = page.rect.height

            # Bottom-right placement with margin
            margin = 20
            x1 = page_width - signature_width - margin
            y1 = page_height - sig_height - margin
            x2 = page_width - margin
            y2 = page_height - margin

            rect = fitz.Rect(x1, y1, x2, y2)
            page.insert_image(rect, stream=sig_bytes)

        output_pdf = io.BytesIO()
        doc.save(output_pdf)
        doc.close()

        st.success("Signature applied to all pages")

        st.download_button(
            label="Download Signed PDF",
            data=output_pdf.getvalue(),
            file_name="signed_document.pdf",
            mime="application/pdf"
        )
