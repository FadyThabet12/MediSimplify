import torch
from torchvision import transforms
from PIL import Image
import numpy as np

def get_image_transform():
    """Get image transforms for model input"""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def preprocess_image(image, device):
    """Preprocess image for model input"""
    transform = get_image_transform()
    
    if not isinstance(image, Image.Image):
        image = Image.open(image).convert("RGB")
    else:
        image = image.convert("RGB")
    
    input_tensor = transform(image).unsqueeze(0).to(device)
    return input_tensor

def prepare_rgb_image(image):
    """Prepare image for Grad-CAM visualization"""
    if not isinstance(image, Image.Image):
        image = Image.open(image).convert("RGB")
    else:
        image = image.convert("RGB")
    
    return np.array(image.resize((224, 224))).astype(np.float32) / 255.0