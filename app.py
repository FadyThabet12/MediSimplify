import streamlit as st

# Page configuration
st.set_page_config(
    page_title="MediSimplify",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar navigation
st.sidebar.title(" MediSimplify")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Medical Q&A", "X-Ray Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "** Disclaimer:**\n"
    "This is for educational purposes only.\n"
    "Always consult healthcare professionals."
)

# Page routing
if page == "Home":
    import pages.home as home
    home.show()
elif page == "Medical Q&A":
    import pages.medical_qa as medical_qa
    medical_qa.show()
elif page == "X-Ray Analysis":
    import pages.image_analysis as image_analysis
    image_analysis.show()