import io
import numpy as np
import torch
from PIL import Image, ImageChops, ImageEnhance
from transformers import AutoImageProcessor, AutoModelForImageClassification

class ImageForensicDetector:
    def __init__(self):
        self.model_name = "dima806/deepfake_vs_real_image_detection"
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
        self.model.eval()

    def generate_ela(self, original_img: Image.Image, quality: int = 90) -> tuple[Image.Image, float]:
        rgb_img = original_img.convert("RGB")
        
        buffer = io.BytesIO()
        rgb_img.save(buffer, "JPEG", quality=quality)
        buffer.seek(0)
        compressed_img = Image.open(buffer)

        diff = ImageChops.difference(rgb_img, compressed_img)
        
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0 / max_diff if max_diff != 0 else 1.0
        ela_img = ImageEnhance.Brightness(diff).enhance(scale)
        
        diff_arr = np.array(diff, dtype=np.float32)
        mean_anomaly_score = float(np.mean(diff_arr))
        
        return ela_img, mean_anomaly_score

    def classify_deepfake(self, image: Image.Image) -> dict:
        inputs = self.processor(images=image.convert("RGB"), return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)[0]
        
        id2label = self.model.config.id2label
        results = {id2label[i].lower(): float(probs[i]) for i in range(len(probs))}
        
        fake_prob = results.get("fake", 0.0)
        return {
            "fake_probability": fake_prob,
            "verdict": "Likely AI-Generated / Spliced" if fake_prob > 0.55 else "Likely Authentic",
            "confidence": max(fake_prob, 1 - fake_prob) * 100
        }
