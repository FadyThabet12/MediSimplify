import streamlit as st
import torch
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from torchvision import models
from safetensors.torch import load_file
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

from config import LABELS, DEVICE
from utils.preprocessing import preprocess_image, prepare_rgb_image
from utils.helpers import process_prediction

class DenseNet121_CheXpert(torch.nn.Module):
    def __init__(self, num_labels=14):
        super().__init__()
        self.densenet = models.densenet121(weights=None)
        num_features = self.densenet.classifier.in_features
        self.densenet.classifier = torch.nn.Linear(num_features, num_labels)
    
    def forward(self, x):
        return self.densenet(x)

@st.cache_resource
def load_model():
    model = DenseNet121_CheXpert(num_labels=14)
    model_path = "Models/image_model/model.keras"
    state = load_file(model_path)
    model.load_state_dict(state, strict=False)
    model = model.to(DEVICE)
    model.eval()
    return model

def predict_xray(image, model, threshold=0.5):
    """Run prediction on X-ray image"""
    import pandas as pd
    
    input_tensor = preprocess_image(image, DEVICE)
    
    with torch.no_grad():
        logits = model(input_tensor)
        probabilities = torch.sigmoid(logits)[0].cpu().numpy()
    
    results = []
    for label, score in zip(LABELS, probabilities):
        results.append({
            "Finding": label,
            "Score": float(score),
            "Positive": bool(score >= threshold)
        })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("Score", ascending=False).reset_index(drop=True)
    
    return {
        "image": image,
        "input_tensor": input_tensor,
        "probabilities": probabilities,
        "results": results_df,
        "positive_findings": results_df[results_df["Positive"]].copy()
    }

def show_cam(image, model, target_layer, target_class, input_tensor):
    """Generate Grad-CAM visualization"""
    targets = [ClassifierOutputTarget(target_class)]
    
    with GradCAM(model=model, target_layers=target_layer) as cam:
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
        grayscale_cam = grayscale_cam[0]
    
    rgb_image = prepare_rgb_image(image)
    visualization = show_cam_on_image(rgb_image, grayscale_cam, use_rgb=True)
    
    return visualization

def show():
    st.title("🩻 X-Ray Analysis")
    st.markdown("Upload a chest X-ray image for AI-powered analysis.")
    
    model = load_model()
    
    uploaded_file = st.file_uploader(
        "Choose a chest X-ray image...",
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded X-Ray", use_container_width=True)
        
        if st.button("Analyze Image", type="primary"):
            with st.spinner("Analyzing image..."):
                result = predict_xray(image, model)
                processed = process_prediction(result["results"])
                
                # Display results
                st.success("Analysis complete!")
                
                # Status
                if processed["status"] == "No significant finding detected":
                    st.info(" No significant findings detected")
                else:
                    st.warning(" Potential findings detected")
                
                # Findings table
                st.markdown("###  Findings")
                st.dataframe(
                    processed["findings"][["Finding", "Score"]],
                    use_container_width=True
                )
                
                # Grad-CAM Visualization
                st.markdown("###  AI Attention Map (Grad-CAM)")
                
                # Find first positive finding (not "No Finding")
                positive_findings = processed["findings"][
                    processed["findings"]["Finding"] != "No Finding"
                ]
                
                if len(positive_findings) > 0:
                    target_class = LABELS.index(positive_findings.iloc[0]["Finding"])
                    target_layer = [
                        model.densenet.features.denseblock4.denselayer16.conv2
                    ]
                    
                    vis = show_cam(
                        image, model, target_layer, target_class, result["input_tensor"]
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(image, caption="Original X-Ray", use_container_width=True)
                    with col2:
                        st.image(vis, caption=f"Focus: {positive_findings.iloc[0]['Finding']}", use_container_width=True)
                else:
                    st.info("No significant findings to visualize")