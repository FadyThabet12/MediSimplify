import streamlit as st

def show():
    st.title(" MediSimplify")
    
    st.markdown("""
    ### Your AI-Powered Medical Assistant
    
    MediSimplify helps you understand medical information in simple terms.
    
    **Features:**
    - 📝 **Medical Q&A**: Ask medical questions and get patient-friendly answers
    - 🩻 **X-Ray Analysis**: Upload chest X-rays for AI-powered analysis
    
    ### How it works:
    1. Choose a feature from the sidebar
    2. Enter your question or upload an image
    3. Get instant, easy-to-understand results
    
    ### Important:
    ⚠️ This tool is for **educational purposes only**. 
    Always consult healthcare professionals for medical decisions.
    """)