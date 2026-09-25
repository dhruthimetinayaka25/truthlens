import cv2
import tempfile
import numpy as np
from PIL import Image
import torch

class VideoForensicDetector:
    def __init__(self, image_detector):
        # Re-use the existing ViT model from image detector to save RAM
        self.image_detector = image_detector

    def analyze_video(self, video_bytes: bytes, sample_rate_fps: int = 1) -> dict:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(video_bytes)
            temp_path = temp_file.name

        cap = cv2.VideoCapture(temp_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 24
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        frame_interval = max(1, int(fps / sample_rate_fps))
        analyzed_frames = 0
        fake_probabilities = []
        sampled_images = []

        curr_frame_idx = 0
        while cap.isOpened() and analyzed_frames < 10:  # Sample up to 10 keyframes for stability
            ret, frame = cap.read()
            if not ret:
                break

            if curr_frame_idx % frame_interval == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_frame)
                
                result = self.image_detector.classify_deepfake(pil_img)
                fake_probabilities.append(result["fake_probability"])
                sampled_images.append(pil_img)
                analyzed_frames += 1

            curr_frame_idx += 1

        cap.release()

        if not fake_probabilities:
            return {"error": "Unable to decode video streams."}

        avg_fake_prob = float(np.mean(fake_probabilities))
        variance_score = float(np.var(fake_probabilities))

        return {
            "average_fake_prob": avg_fake_prob,
            "temporal_flicker_variance": variance_score,
            "sampled_frames_count": len(fake_probabilities),
            "verdict": "Manipulated / Deepfake Video" if avg_fake_prob > 0.50 else "Likely Authentic Footage",
            "sampled_previews": sampled_images[:4]
        }
