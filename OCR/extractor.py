# OCR/extractor.py
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForMultimodalLM

class SuryaExtractor:
    def __init__(self, model_id="datalab-to/surya-ocr-2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[SuryaExtractor] Initializing on device: {self.device}")
        
        print("[SuryaExtractor] Loading processor and model...")
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        self.model = AutoModelForMultimodalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        print("[SuryaExtractor] Model loaded successfully!")

    def _normalize_image(self, img, max_side=1600):
        """Resize image to prevent out-of-memory errors."""
        img = img.convert("RGB")
        w, h = img.size
        scale = min(max_side / max(w, h), 1.0)
        if scale < 1:
            img = img.resize(
                (int(w * scale), int(h * scale)), 
                Image.Resampling.LANCZOS
            )
        return img

    def extract_raw_html(self, image):
        """
        Runs inference and returns the raw HTML output from the model.
        """
        OCR_PROMPT = (
            "OCR this image to HTML. Each block is a div with data-label and data-bbox "
            "(x0 y0 x1 y1, normalized 0-1000). Preserve all visible text, numbers, "
            "medical values, units, punctuation, tables, and reading order. "
            "Do not summarize or describe the image."
        )

        image = self._normalize_image(image)

        messages = [{
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": OCR_PROMPT},
            ],
        }]

        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )

        inputs = {k: v.to(self.model.device) if torch.is_tensor(v) else v for k, v in inputs.items()}

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=False,
                use_cache=True,
            )

        start = inputs["input_ids"].shape[-1]
        raw_html = self.processor.decode(
            outputs[0][start:], 
            skip_special_tokens=True
        )

        return raw_html