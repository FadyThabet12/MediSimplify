# pages/ocr_page.py
import streamlit as st
from PIL import Image
import os
import time

# Import your OCR modules
from OCR.extractor import SuryaExtractor
from OCR.processor import SuryaProcessor

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="OCR Extraction", page_icon="📄", layout="wide")

# --- CACHING THE HEAVY MODEL ---
@st.cache_resource
def load_ocr_engine():
    """Loads the Surya-OCR model once and keeps it in memory."""
    local_model_path = os.path.join(os.getcwd(), "local_models", "surya-ocr-2")
    
    # Check if the local folder exists
    if os.path.exists(local_model_path):
        st.info(f"Loading Surya-OCR from local path: `{local_model_path}`")
        return SuryaExtractor(local_model_path=local_model_path)
    else:
        st.info("Local model not found. Downloading from Hugging Face... (This might take a few minutes)")
        return SuryaExtractor() # Fallback to Hugging Face

def main():
    st.title("📄 Medical OCR Extractor")
    st.markdown("Upload a medical image to extract all text, numbers, and tables using Surya-OCR-2.")

    # 1. Initialize Engine (This happens only once per session)
    with st.spinner("Initializing OCR Engine..."):
        extractor = load_ocr_engine()
    processor = SuryaProcessor() # Processor is stateless, no caching needed

    # 2. Sidebar Options
    st.sidebar.header("⚙️ Settings")
    show_raw_html = st.sidebar.checkbox("Show Raw HTML Output", value=False)

    # 3. File Upload
    uploaded_file = st.file_uploader(
        "Choose a medical image...", 
        type=["png", "jpg", "jpeg", "bmp", "tiff"],
        help="Upload an image of a medical report, prescription, or lab results."
    )

    if uploaded_file is not None:
        # Load the image
        try:
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🖼️ Uploaded Image")
                st.image(image, use_container_width=True)
                st.caption(f"Dimensions: {image.width} x {image.height}")

            with col2:
                st.subheader("📝 Extracted Text")
                
                if st.button("🚀 Run OCR Extraction", type="primary"):
                    with st.spinner("Processing image with Surya-OCR... This may take 10-30 seconds."):
                        start_time = time.perf_counter()
                        
                        # Run the OCR
                        try:
                            raw_html = extractor.extract_raw_html(image)
                            clean_text = processor.html_to_text(raw_html)
                            duration = time.perf_counter() - start_time
                            
                            st.success(f"OCR completed in {duration:.2f} seconds!")
                            
                            # Display the clean text
                            st.text_area("Extracted Text", clean_text, height=400)
                            
                            # Optionally show raw HTML in an expander
                            if show_raw_html:
                                with st.expander("View Raw HTML Output"):
                                    st.code(raw_html, language="html")

                            # Download button for the extracted text
                            st.download_button(
                                label="📥 Download Extracted Text (.txt)",
                                data=clean_text,
                                file_name="ocr_extracted_text.txt",
                                mime="text/plain"
                            )

                        except Exception as e:
                            st.error(f"An error occurred during OCR: {e}")
                            
        except Exception as e:
            st.error(f"Error loading image: {e}")

    else:
        st.info("👈 Please upload a medical image to begin OCR extraction.")
        st.markdown("""
        ### Supported Features:
        - **Text Extraction**: Pulls all printed and handwritten text.
        - **Preserves Structure**: Maintains the reading order and table layouts.
        - **Medical Accuracy**: Designed to preserve numbers, units (mg, ml, %), and clinical values.
        """)

if __name__ == "__main__":
    main()