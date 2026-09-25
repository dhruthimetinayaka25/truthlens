import fitz  # PyMuPDF

class PDFDocAnalyzer:
    SUSPICIOUS_PRODUCERS = ["canva", "photoshop", "gimp", "ilovepdf", "pdfescape", "smallpdf"]

    def analyze_pdf(self, pdf_stream: bytes) -> dict:
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        metadata = doc.metadata or {}
        
        anomalies = []
        suspicion_score = 0

        producer = metadata.get("producer", "").lower()
        creator = metadata.get("creator", "").lower()

        for tool in self.SUSPICIOUS_PRODUCERS:
            if tool in producer or tool in creator:
                anomalies.append(f"Document produced or altered with graphics tool: {tool.title()}")
                suspicion_score += 25

        creation_date = metadata.get("creationDate", "")
        mod_date = metadata.get("modDate", "")
        if creation_date and mod_date and creation_date != mod_date:
            anomalies.append("Document was modified after initial generation.")
            suspicion_score += 15

        total_images = 0
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            image_list = page.get_images(full=True)
            total_images += len(image_list)

        if total_images > 0 and len(doc) == 1:
            anomalies.append(f"Single-page document contains {total_images} embedded raster object(s). Verify layers.")
            suspicion_score += 10

        if not creation_date:
            anomalies.append("Creation metadata stripped or missing.")
            suspicion_score += 10

        suspicion_score = min(suspicion_score, 100)

        return {
            "metadata": metadata,
            "page_count": len(doc),
            "embedded_image_count": total_images,
            "anomalies": anomalies,
            "suspicion_score": suspicion_score,
            "verdict": "Suspicious / Modified" if suspicion_score >= 40 else "Clean Structure"
        }
