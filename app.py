import streamlit as st
from PIL import Image
from detectors.image_detector import ImageForensicDetector
from detectors.pdf_detector import PDFDocAnalyzer
from detectors.video_detector import VideoForensicDetector

# Page Configuration
st.set_page_config(
    page_title="TruthLens Forensics Core",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Cyber Forensic Styling
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Background styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(3, 7, 18, 1) 90%);
        color: #f8fafc;
    }

    /* Metric & Glass Card Container */
    .forensic-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1.2rem;
    }

    .forensic-card-glow {
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.12);
    }

    /* Custom Header Banner */
    .banner-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .banner-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    /* Badges */
    .badge-safe {
        display: inline-block;
        padding: 4px 14px;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid #22c55e;
        border-radius: 20px;
        color: #4ade80;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .badge-danger {
        display: inline-block;
        padding: 4px 14px;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        border-radius: 20px;
        color: #f87171;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* File uploader tweak */
    .stFileUploader section {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px dashed rgba(56, 189, 248, 0.4) !important;
        border-radius: 12px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Load Engines (Reuses ViT memory for images and video frames)
@st.cache_resource
def get_engines():
    img_det = ImageForensicDetector()
    pdf_det = PDFDocAnalyzer()
    vid_det = VideoForensicDetector(img_det)
    return img_det, pdf_det, vid_det

with st.spinner("Initializing Deep Neural Forensics, PyMuPDF, and Video Decoders..."):
    img_detector, pdf_analyzer, video_detector = get_engines()

# Sidebar Navigation & System Telemetry
with st.sidebar:
    st.markdown("### 🔬 System Telemetry")
    st.markdown("""
    * **Image Engine:** Vision Transformer (ViT)
    * **Compression ELA:** Dual Resampling (90Q)
    * **Video Protocol:** Temporal Keyframe Extraction
    * **PDF Tree:** PyMuPDF AST Parsing
    * **Environment:** Secure Container
    """)
    st.divider()
    st.markdown("### 📋 Protocol Selection")
    module_choice = st.radio(
        "Choose Inspection Vector:",
        [
            "🖼️ Multi-Spectral Image Forensics",
            "🎥 Deepfake Video Spatial-Temporal Scan",
            "📄 PDF Structural Dissection"
        ]
    )
    st.divider()
    st.caption("TruthLens Defense Suite v2.4 • Major Project Edition")

# Main Header Section
st.markdown('<div class="banner-title">TRUTHLENS FORENSIC INTELLIGENCE</div>', unsafe_allow_html=True)
st.markdown('<div class="banner-subtitle">Multi-Modal Synthetic Artifact & Document Structural Tamper Diagnostic Framework</div>', unsafe_allow_html=True)

# MODULE 1: IMAGE FORENSICS
if "Image" in module_choice:
    st.markdown("""
    <div class="forensic-card forensic-card-glow">
        <h4 style="margin:0; color:#38bdf8;">Visual & Latent Deepfake Vector</h4>
        <p style="margin:0; font-size:0.85rem; color:#94a3b8;">Compute JPEG Quantization Discrepancies and execute Vision Transformer spatial classification.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Drop target asset for forensic decomposition (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        raw_img = Image.open(uploaded_file)
        
        col_view1, col_view2 = st.columns(2)
        with col_view1:
            st.markdown("##### 📌 Primary Ingestion")
            st.image(raw_img, use_container_width=True)
            
        with col_view2:
            st.markdown("##### 🔍 Real-Time Inference Results")
            with st.spinner("Calculating Error Level Matrices & ViT Embeddings..."):
                ela_img, ela_score = img_detector.generate_ela(raw_img)
                ml_res = img_detector.classify_deepfake(raw_img)
            
            is_fake = ml_res["fake_probability"] > 0.55
            badge_html = f'<span class="badge-danger">CRITICAL: {ml_res["verdict"].upper()}</span>' if is_fake else f'<span class="badge-safe">VERIFIED: {ml_res["verdict"].upper()}</span>'
            
            st.markdown(f"""
            <div class="forensic-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span style="font-weight:600; color:#cbd5e1;">Integrity Status</span>
                    {badge_html}
                </div>
                <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:4px;">Synthetic Generation Probability</div>
                <div style="font-size:1.6rem; font-weight:700; color:#38bdf8; font-family:'JetBrains Mono';">
                    {ml_res["fake_probability"]*100:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(ml_res["fake_probability"])
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Classifier Confidence", f"{ml_res['confidence']:.1f}%")
            col_m2.metric("ELA Anomaly Index", f"{ela_score:.2f}")

        st.divider()
        st.markdown("##### 🔬 Spectral Compression Discrepancy Heatmap (ELA)")
        st.caption("Bright variations reveal localized re-saving, splicing, or non-uniform artifact boundaries.")
        st.image(ela_img, caption="Error Level Analysis Differential Map", use_container_width=True)

# MODULE 2: VIDEO FORENSICS
elif "Video" in module_choice:
    st.markdown("""
    <div class="forensic-card forensic-card-glow">
        <h4 style="margin:0; color:#38bdf8;">Spatial-Temporal Video Deepfake Vector</h4>
        <p style="margin:0; font-size:0.85rem; color:#94a3b8;">Extracts keyframes across temporal intervals, evaluates facial synthesis artifacts, and calculates flicker variance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_video = st.file_uploader("Upload video file (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])
    
    if uploaded_video:
        video_bytes = uploaded_video.read()
        st.video(video_bytes)
        
        with st.spinner("Extracting keyframes and computing ViT spatial-temporal scores..."):
            vid_report = video_detector.analyze_video(video_bytes)
            
        if "error" in vid_report:
            st.error(f"🛑 {vid_report['error']}")
        else:
            is_vid_fake = vid_report["average_fake_prob"] > 0.50
            vid_badge = f'<span class="badge-danger">ALERT: {vid_report["verdict"]}</span>' if is_vid_fake else f'<span class="badge-safe">SECURE: {vid_report["verdict"]}</span>'
            
            st.markdown(f"""
            <div class="forensic-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span style="font-weight:600; color:#cbd5e1;">Video Integrity Assessment</span>
                    {vid_badge}
                </div>
                <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:4px;">Mean Synthesis Probability</div>
                <div style="font-size:1.6rem; font-weight:700; color:#38bdf8; font-family:'JetBrains Mono';">
                    {vid_report["average_fake_prob"]*100:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            v_col1, v_col2 = st.columns(2)
            v_col1.metric("Analyzed Keyframes", vid_report["sampled_frames_count"])
            v_col2.metric("Temporal Variance Index", f"{vid_report['temporal_flicker_variance']:.4f}")
            
            st.markdown("##### 🎞️ Sampled Keyframe Decomposition")
            k_cols = st.columns(len(vid_report["sampled_previews"]))
            for idx, col in enumerate(k_cols):
                with col:
                    st.image(vid_report["sampled_previews"][idx], caption=f"Frame #{idx+1}", use_container_width=True)

# MODULE 3: PDF FORENSICS
else:
    st.markdown("""
    <div class="forensic-card forensic-card-glow">
        <h4 style="margin:0; color:#818cf8;">Document Structure & Metadata Inspector</h4>
        <p style="margin:0; font-size:0.85rem; color:#94a3b8;">Parses xref tables, generation software signatures, modification timelines, and embedded raster overlays.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_pdf = st.file_uploader("Select document to execute structural inspection (PDF)", type=["pdf"])
    
    if uploaded_pdf:
        with st.spinner("Decompiling xref tables and scanning dictionary headers..."):
            pdf_bytes = uploaded_pdf.read()
            report = pdf_analyzer.analyze_pdf(pdf_bytes)

        is_tampered = report["suspicion_score"] >= 40
        status_badge = f'<span class="badge-danger">ALERT: {report["verdict"]}</span>' if is_tampered else f'<span class="badge-safe">AUTHENTIC: {report["verdict"]}</span>'

        st.markdown(f"""
        <div class="forensic-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-weight:600; color:#cbd5e1;">Structural Assessment</span>
                {status_badge}
            </div>
            <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:4px;">Tampering Risk Index</div>
            <div style="font-size:1.6rem; font-weight:700; color:#818cf8; font-family:'JetBrains Mono';">
                {report["suspicion_score"]}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Page Count", report["page_count"])
        col_p2.metric("Embedded Rasters", report["embedded_image_count"])
        col_p3.metric("Producer Tag", "Detected" if report["metadata"].get("producer") else "Missing")

        st.markdown("##### 🚨 Diagnostic Findings")
        if report["anomalies"]:
            for anomaly in report["anomalies"]:
                st.error(f"🛑 {anomaly}")
        else:
            st.success("✅ Clean structural footprint. No editing traces or mismatching revision dates detected.")

        with st.expander("🛠️ Raw Cross-Reference & Metadata Dictionary"):
            st.json(report["metadata"])
