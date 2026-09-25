import streamlit as st
import plotly.graph_objects as go
from PIL import Image
from detectors.image_detector import ImageForensicDetector
from detectors.pdf_detector import PDFDocAnalyzer
from detectors.video_detector import VideoForensicDetector

st.set_page_config(
    page_title="TruthLens Forensics Core | Major Project Edition",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(3, 7, 18, 1) 95%);
        color: #f8fafc;
    }
    .forensic-panel {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 10px;
        padding: 18px;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    .badge-safe {
        padding: 5px 14px;
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid #22c55e;
        border-radius: 6px;
        color: #4ade80;
        font-weight: 700;
        font-family: 'JetBrains Mono';
        font-size: 0.85rem;
    }
    .badge-danger {
        padding: 5px 14px;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        border-radius: 6px;
        color: #f87171;
        font-weight: 700;
        font-family: 'JetBrains Mono';
        font-size: 0.85rem;
    }
    .hash-box {
        background: #020617;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px 12px;
        font-family: 'JetBrains Mono';
        font-size: 0.8rem;
        color: #38bdf8;
        word-break: break-all;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

@st.cache_resource
def get_engines():
    img_det = ImageForensicDetector()
    pdf_det = PDFDocAnalyzer()
    vid_det = VideoForensicDetector(img_det)
    return img_det, pdf_det, vid_det

with st.spinner("Compiling Neural Ingestion Pipeline & Signal Decoders..."):
    img_detector, pdf_analyzer, video_detector = get_engines()

# Sidebar: System Specifications & Vector Selection
with st.sidebar:
    st.markdown("### 🔬 TruthLens Core v3.0")
    st.caption("Forensic Engineering Capstone Platform")
    st.markdown("""
    * **ViT Architecture:** `dima806/ViT-Deepfake`
    * **Frequency Domain:** 2D-FFT Log-Polar
    * **Compression Map:** ELA (Quality=90)
    * **Video Frame Extraction:** OpenCV Pipeline
    * **Document Parser:** PyMuPDF Lexer
    """)
    st.divider()
    module_choice = st.radio(
        "Select Diagnostic Vector:",
        [
            "🖼️ Dual-Domain Image Forensics (ViT + FFT)",
            "🎥 Temporal Video Consistency Scan",
            "📄 Document Structural & Metadata Analysis"
        ]
    )
    st.divider()
    st.caption("Cryptographic Chain-of-Custody Verified • SHA-256")

# Header
st.markdown('<h2 style="margin:0; font-weight:700; letter-spacing:-0.03em; color:#38bdf8;">TRUTHLENS FORENSIC OPERATIONS CENTER</h2>', unsafe_allow_html=True)
st.caption("Automated Multi-Modal Integrity Verification & Spatial-Frequency Forensic Analysis")

# VECTOR 1: DUAL-DOMAIN IMAGE FORENSICS
if "Image" in module_choice:
    uploaded_file = st.file_uploader("Ingest target image for multi-spectral decomposition (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        raw_bytes = uploaded_file.read()
        sha256_hash = img_detector.compute_sha256(raw_bytes)
        raw_img = Image.open(uploaded_file)
        
        # Provenance Header
        st.markdown(f"""
        <div class="forensic-panel">
            <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase; margin-bottom:4px;">Cryptographic Chain of Custody (SHA-256 Digest)</div>
            <div class="hash-box">{sha256_hash}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Computing Vision Transformer Logits, ELA Residuals, and 2D-FFT Spectrum..."):
            ela_img, ela_score = img_detector.generate_ela(raw_img)
            fft_img, hf_power = img_detector.compute_fft_spectrum(raw_img)
            ml_res = img_detector.classify_deepfake(raw_img)
            
        col1, col2, col3 = st.columns([1.2, 1, 1])
        
        with col1:
            st.markdown("##### 📌 Ingested Asset")
            st.image(raw_img, use_container_width=True)
            
        with col2:
            st.markdown("##### 🔲 Compression Residuals (ELA)")
            st.image(ela_img, caption="Error Level Analysis Differential", use_container_width=True)
            st.caption(f"Discrepancy Score: {ela_score:.2f}")

        with col3:
            st.markdown("##### 🌐 2D-FFT Power Spectrum")
            st.image(fft_img, caption="Deconvolution Grid Detector", use_container_width=True)
            st.caption(f"High-Freq Energy Ratio: {hf_power:.2f}")

        # Diagnostic Gauge & Verdict
        is_fake = ml_res["fake_probability"] > 0.55
        badge_html = f'<span class="badge-danger">CRITICAL: {ml_res["verdict"].upper()}</span>' if is_fake else f'<span class="badge-safe">SECURE: {ml_res["verdict"].upper()}</span>'
        
        st.markdown(f"""
        <div class="forensic-panel" style="margin-top:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-weight:600;">Neural Forensic Classification</span>
                {badge_html}
            </div>
            <div style="font-size:0.85rem; color:#94a3b8;">Synthetic Synthesis Probability: <b>{ml_res["fake_probability"]*100:.2f}%</b> (ViT Confidence: {ml_res["confidence"]:.2f}%)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Multi-Vector Polar Radar Plot
        fig = go.Figure(go.Scatterpolar(
            r=[ml_res["fake_probability"]*100, min(100, ela_score * 4), min(100, hf_power / 1000), ml_res["confidence"]],
            theta=['ViT Probability', 'Compression Drift', 'Spectral Discontinuity', 'Inference Confidence'],
            fill='toself',
            marker=dict(color='#38bdf8')
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], color="#94a3b8")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=40, r=40, t=20, b=20),
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig, use_container_width=True)

# VECTOR 2: TEMPORAL VIDEO CONSISTENCY SCAN
elif "Video" in module_choice:
    uploaded_video = st.file_uploader("Ingest video sequence for spatial-temporal inspection (MP4, MOV)", type=["mp4", "mov"])
    
    if uploaded_video:
        raw_v_bytes = uploaded_video.read()
        v_sha256 = img_detector.compute_sha256(raw_v_bytes)
        
        st.markdown(f"""
        <div class="forensic-panel">
            <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase; margin-bottom:4px;">Video Cryptographic Digest (SHA-256)</div>
            <div class="hash-box">{v_sha256}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.video(raw_v_bytes)
        
        with st.spinner("Extracting keyframes and tracking temporal probability variance..."):
            vid_report = video_detector.analyze_video(raw_v_bytes)
            
        if "error" in vid_report:
            st.error(vid_report["error"])
        else:
            is_vid_fake = vid_report["average_fake_prob"] > 0.50
            v_badge = f'<span class="badge-danger">ALERT: {vid_report["verdict"]}</span>' if is_vid_fake else f'<span class="badge-safe">SECURE: {vid_report["verdict"]}</span>'
            
            st.markdown(f"""
            <div class="forensic-panel" style="margin-top:1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span style="font-weight:600;">Temporal Stream Diagnosis</span>
                    {v_badge}
                </div>
                <div style="font-size:0.85rem; color:#94a3b8;">Mean Synthesis Probability: <b>{vid_report["average_fake_prob"]*100:.2f}%</b></div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.metric("Analyzed Keyframes", vid_report["sampled_frames_count"])
            c2.metric("Temporal Variance Index", f"{vid_report['temporal_flicker_variance']:.5f}")
            
            st.markdown("##### 🎞️ Extracted Inter-Frame Decompositions")
            cols = st.columns(len(vid_report["sampled_previews"]))
            for idx, col in enumerate(cols):
                with col:
                    st.image(vid_report["sampled_previews"][idx], caption=f"Frame #{idx+1}", use_container_width=True)

# VECTOR 3: DOCUMENT STRUCTURAL ANALYSIS
else:
    uploaded_pdf = st.file_uploader("Ingest target document for structural xref dissection (PDF)", type=["pdf"])
    
    if uploaded_pdf:
        raw_pdf_bytes = uploaded_pdf.read()
        pdf_sha256 = img_detector.compute_sha256(raw_pdf_bytes)
        
        st.markdown(f"""
        <div class="forensic-panel">
            <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase; margin-bottom:4px;">Document Cryptographic Digest (SHA-256)</div>
            <div class="hash-box">{pdf_sha256}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Parsing AST structural tokens and examining embedded streams..."):
            report = pdf_analyzer.analyze_pdf(raw_pdf_bytes)
            
        is_tampered = report["suspicion_score"] >= 40
        status_badge = f'<span class="badge-danger">ALERT: {report["verdict"]}</span>' if is_tampered else f'<span class="badge-safe">AUTHENTIC: {report["verdict"]}</span>'

        st.markdown(f"""
        <div class="forensic-panel">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-weight:600;">Structural Document Diagnosis</span>
                {status_badge}
            </div>
            <div style="font-size:0.85rem; color:#94a3b8;">Tampering Risk Score: <b>{report["suspicion_score"]}%</b></div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Page Count", report["page_count"])
        col2.metric("Embedded Raster Objects", report["embedded_image_count"])
        col3.metric("Producer Signature", "Detected" if report["metadata"].get("producer") else "Missing")

        st.markdown("##### 🚨 Diagnostic Findings")
        if report["anomalies"]:
            for anomaly in report["anomalies"]:
                st.error(f"🛑 {anomaly}")
        else:
            st.success("✅ Clean structural footprint. No editing traces or mismatched revision dates detected.")

        with st.expander("🛠️ Raw Cross-Reference & Metadata Tree"):
            st.json(report["metadata"])
