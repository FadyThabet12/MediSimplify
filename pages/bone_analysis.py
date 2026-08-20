import streamlit as st
import torch
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torchvision import models
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

from config import DEVICE, BONE_LABELS
from utils.preprocessing import preprocess_image, prepare_rgb_image
from utils.helpers import process_prediction

class DenseNet121_Bone(torch.nn.Module):
    """DenseNet121 model for bone X-ray classification"""
    def __init__(self, num_labels=12):
        super().__init__()
        self.densenet = models.densenet121(weights=None)
        num_features = self.densenet.classifier.in_features
        self.densenet.classifier = torch.nn.Linear(num_features, num_labels)
    
    def forward(self, x):
        return self.densenet(x)

@st.cache_resource
def load_bone_model():
    """Load bone X-ray model"""
    model = DenseNet121_Bone(num_labels=len(BONE_LABELS))
    model_path = "Models/image_model/bone_model.pth"
    
    try:
        state = torch.load(model_path, map_location=DEVICE)
        model.load_state_dict(state, strict=False)
        model = model.to(DEVICE)
        model.eval()
        return model
    except FileNotFoundError:
        st.error("❌ Bone model not found. Please download bone_model.pth and place it in Models/image_model/")
        return None

def predict_bone_xray(image, model, threshold=0.5):
    """Run prediction on bone X-ray image"""
    input_tensor = preprocess_image(image, DEVICE)
    
    with torch.no_grad():
        logits = model(input_tensor)
        probabilities = torch.sigmoid(logits)[0].cpu().numpy()
    
    results = []
    for label, score in zip(BONE_LABELS, probabilities):
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

def show_bone_cam(image, model, target_layer, target_class, input_tensor):
    """Generate Grad-CAM visualization for bone X-ray"""
    targets = [ClassifierOutputTarget(target_class)]
    
    with GradCAM(model=model, target_layers=target_layer) as cam:
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets)
        grayscale_cam = grayscale_cam[0]
    
    rgb_image = prepare_rgb_image(image)
    visualization = show_cam_on_image(rgb_image, grayscale_cam, use_rgb=True)
    
    return visualization

def show():
    st.title("🦴 Bone X-Ray Analysis")
    st.markdown("Upload a bone X-ray image for AI-powered fracture and pathology analysis.")
    
    model = load_bone_model()
    
    if model is None:
        st.warning("⚠️ Bone model not loaded. Please check the model file.")
        return
    
    uploaded_file = st.file_uploader(
        "Choose a bone X-ray image...",
        type=["jpg", "jpeg", "png"],
        key="bone_uploader"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Bone X-Ray", use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            threshold = st.slider("Confidence Threshold", 0.1, 0.9, 0.5, key="bone_threshold")
        
        with col2:
            st.markdown(f"**Model:** DenseNet121 (Bone)")
            st.markdown(f"**Classes:** {len(BONE_LABELS)}")
        
        if st.button("🔍 Analyze Bone X-Ray", type="primary"):
            with st.spinner("Analyzing bone X-ray..."):
                result = predict_bone_xray(image, model, threshold)
                processed = process_prediction(result["results"], threshold)
                
                # Display results
                st.success("Analysis complete!")
                
                # Status
                if processed["status"] == "No significant finding detected":
                    st.info("✅ No significant bone abnormalities detected")
                else:
                    st.warning("⚠️ Potential bone abnormalities detected")
                
                # Findings table
                st.markdown("### 📊 Findings")
                
                # Show all findings with scores
                display_df = result["results"].copy()
                display_df["Score"] = display_df["Score"].apply(lambda x: f"{x:.3f}")
                display_df["Positive"] = display_df["Positive"].apply(lambda x: "✅" if x else "❌")
                
                st.dataframe(
                    display_df[["Finding", "Score", "Positive"]],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Positive findings summary
                positive = processed["findings"]
                if len(positive) > 0 and positive.iloc[0]["Finding"] != "No Finding":
                    st.markdown("### 🎯 Positive Findings")
                    for _, row in positive.iterrows():
                        st.markdown(f"- **{row['Finding']}** ({row['Score']:.3f})")
                else:
                    st.info("No positive findings above threshold")
                
                # Grad-CAM Visualization
                st.markdown("### 🔥 AI Attention Map (Grad-CAM)")
                
                # Find first positive finding (not "No Finding")
                positive_findings = processed["findings"][
                    processed["findings"]["Finding"] != "No Finding"
                ]
                
                if len(positive_findings) > 0:
                    target_class = BONE_LABELS.index(positive_findings.iloc[0]["Finding"])
                    target_layer = [
                        model.densenet.features.denseblock4.denselayer16.conv2
                    ]
                    
                    vis = show_bone_cam(
                        image, model, target_layer, target_class, result["input_tensor"]
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(image, caption="Original X-Ray", use_container_width=True)
                    with col2:
                        st.image(vis, caption=f"Focus: {positive_findings.iloc[0]['Finding']}", use_container_width=True)
                else:
                    st.info("No significant findings to visualize")