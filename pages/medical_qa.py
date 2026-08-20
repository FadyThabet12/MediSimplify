# import streamlit as st
# from rag.pipeline import MedicalRAGPipeline

# def show():
#     st.title(" Medical Q&A")
#     st.markdown("Ask any medical question and get a patient-friendly answer.")
    
#     # Initialize pipeline with caching
#     @st.cache_resource
#     def get_rag_pipeline():
#         return MedicalRAGPipeline()
    
#     rag = get_rag_pipeline()
    
#     # User input
#     question = st.text_area("Your Question:", height=100)
#     k = st.slider("Number of sources to retrieve:", 3, 10, 5)
    
#     if st.button("Get Answer", type="primary"):
#         if not question:
#             st.warning("Please enter a question")
#             return
        
#         with st.spinner("Searching medical knowledge..."):
#             result = rag.answer(question, k=k)
            
#             # Display answer
#             st.success("Answer generated!")
#             st.markdown("### 💡 Answer:")
#             st.write(result["answer"])
            
#             # Display sources
#             with st.expander("📚 View Sources"):
#                 for i, source in enumerate(result["sources"], 1):
#                     st.markdown(f"**Source {i}**")
#                     st.markdown(f"**Title:** {source['title']}")
#                     st.markdown(f"**Score:** {source['score']:.3f}")
#                     st.markdown(f"**Category:** {source['category']}")
#                     st.markdown(f"**Text:**\n{source['text'][:500]}...")
#                     st.divider()
            
#             # Language info
#             lang = "Arabic" if result["language"] == "ar" else "English"
#             st.caption(f"Response language: {lang}")
import streamlit as st
from rag.pipeline import MedicalRAGPipeline

def show():
    st.title("💬 Medical Q&A")
    st.markdown("Ask any medical question and get a patient-friendly answer.")
    
    # Initialize pipeline with caching
    @st.cache_resource
    def get_rag_pipeline():
        return MedicalRAGPipeline()
    
    rag = get_rag_pipeline()
    
    # User input
    question = st.text_area("Your Question:", height=100)
    k = st.slider("Number of sources to retrieve:", 3, 10, 5)
    
    if st.button("Get Answer", type="primary"):
        if not question:
            st.warning("Please enter a question")
            return
        
        with st.spinner("Searching medical knowledge..."):
            result = rag.answer(question, k=k)
            
            # Display answer
            st.success("Answer generated!")
            st.markdown("### 💡 Answer:")
            st.write(result["answer"])
            
            # Display sources
            with st.expander("📚 View Sources"):
                for i, source in enumerate(result["sources"], 1):
                    st.markdown(f"**Source {i}**")
                    st.markdown(f"**Title:** {source['title']}")
                    st.markdown(f"**Score:** {source['score']:.3f}")
                    if "rerank_score" in source:
                        st.markdown(f"**Rerank Score:** {source['rerank_score']:.3f}")
                    st.markdown(f"**Category:** {source['category']}")
                    st.markdown(f"**Text:**\n{source['text'][:500]}...")
                    st.divider()
            
            # Language info
            lang = "Arabic" if result["language"] == "ar" else "English"
            st.caption(f"Response language: {lang}")