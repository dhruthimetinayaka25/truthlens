import streamlit as st
from PIL import Image
from detectors.image_detector import ImageForensicDetector
from detectors.pdf_detector import PDFDocAnalyzer

st.set_page_config(page_title="TruthLens - Multi-Modal Forensics", layout="wide")

@st.cache_resource
def load_detectors():
    return ImageForensicDetector(), PDFDocAnalyzer()

img_detector, pdf_analyzer = load_detectors()

st.title("🛡️ TruthLens: Digital Integrity & Forensic Scanner")
st.caption("Inspect digital media and official documents for synthetic modifications and artifacts.")

tab_img, tab_doc = st.tabs(["🖼️ Image & Deepfake Inspection", "📄 PDF & Document Forensics"])

# TAB 1: IMAGE INSPECTION
with tab_img:
    st.subheader("Visual Artifact & Face Synthesis Analysis")
    uploaded_img = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_img:
        image = Image.open(uploaded_img)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Uploaded Original", use_container_width=True)
            
        with col2:
            with st.spinner("Executing neural scan & frequency analysis..."):
                ela_visual, ela_val = img_detector.generate_ela(image)
                ml_result = img_detector.classify_deepfake(image)
                
            st.metric("Neural Verdict", ml_result["verdict"])
            st.progress(ml_result["fake_probability"])
            st.write(f"**Confidence:** {ml_result['confidence']:.2f}%")
            
            st.divider()
            st.write("**Error Level Analysis (ELA) Heatmap**")
            st.image(ela_visual, caption="High-contrast areas indicate compression mismatches", use_container_width=True)
            st.caption(f"Mean Compression Discrepancy Index: {ela_val:.2f}")

# TAB 2: PDF FORENSICS
with tab_doc:
    st.subheader("Document Metadata & Tampering Inspector")
    uploaded_pdf = st.file_uploader("Upload document (PDF)", type=["pdf"])
    
    if uploaded_pdf:
        with st.spinner("Extracting PDF tree & structural markers..."):
            pdf_bytes = uploaded_pdf.read()
            report = pdf_analyzer.analyze_pdf(pdf_bytes)

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Structural Verdict", report["verdict"])
        metric_col2.metric("Tamper Suspicion Score", f"{report['suspicion_score']}%")
        metric_col3.metric("Embedded Images", report["embedded_image_count"])

        st.subheader("Forensic Findings")
        if report["anomalies"]:
            for item in report["anomalies"]:
                st.warning(f"⚠️ {item}")
        else:
            st.success("✅ No structural anomalies or editing signatures detected.")

        with st.expander("Raw Metadata Tree"):
            st.json(report["metadata"])
