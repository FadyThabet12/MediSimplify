# import streamlit as st

# # ============================================
# # PAGE CONFIG
# # ============================================
# st.set_page_config(
#     page_title="MediSimplify",
#     page_icon="🏥",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ============================================
# # SESSION STATE - Initialize
# # ============================================
# if "page" not in st.session_state:
#     st.session_state.page = "Home"

# # ============================================
# # IMPORT PAGES
# # ============================================
# import pages.home as home
# import pages.medical_qa as medical_qa
# import pages.image_analysis as image_analysis
# import pages.bone_analysis as bone_analysis

# try:
#     import pages.ocr_report as ocr_report
#     HAS_OCR = True
# except ImportError:
#     ocr_report = None
#     HAS_OCR = False

# # ============================================
# # CUSTOM CSS
# # ============================================
# st.markdown("""
# <style>
#     /* Sidebar Navigation */
#     .nav-btn {
#         display: block;
#         width: 100%;
#         padding: 0.7rem 1rem;
#         margin: 0.3rem 0;
#         border: none;
#         border-radius: 10px;
#         background: transparent;
#         color: #4b5563;
#         font-size: 0.9rem;
#         font-weight: 500;
#         text-align: left;
#         cursor: pointer;
#         transition: all 0.2s ease;
#         font-family: 'Segoe UI', sans-serif;
#     }
    
#     .nav-btn:hover {
#         background: #e5e7eb;
#         transform: translateX(4px);
#     }
    
#     .nav-btn.active {
#         background: linear-gradient(135deg, #005bea 0%, #00c6fb 100%);
#         color: white;
#         box-shadow: 0 4px 15px rgba(0, 91, 234, 0.3);
#     }
    
#     .nav-btn .nav-icon {
#         margin-right: 10px;
#     }
    
#     /* Hero Section - Clean without box */
#     .hero-title {
#         font-size: 3.2rem;
#         font-weight: 800;
#         background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.2rem;
#         text-align: center;
#     }
    
#     .hero-sub {
#         font-size: 1.1rem;
#         color: #475569;
#         text-align: center;
#         max-width: 600px;
#         margin: 0 auto;
#         -webkit-text-fill-color: #475569;
#     }
    
#     .hero-desc {
#         font-size: 0.95rem;
#         color: #64748b;
#         text-align: center;
#         max-width: 650px;
#         margin: 0.5rem auto 0 auto;
#         -webkit-text-fill-color: #64748b;
#     }
    
#     /* Mini Cards */
#     .mini-card {
#         background: white;
#         border-radius: 16px;
#         padding: 1.2rem 1rem;
#         text-align: center;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.06);
#         border: 1px solid rgba(0,0,0,0.04);
#         transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#         height: 100%;
#         cursor: pointer;
#         position: relative;
#         overflow: hidden;
#     }
    
#     .mini-card::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         height: 4px;
#         background: linear-gradient(90deg, #3b82f6, #8b5cf6);
#         opacity: 0;
#         transition: opacity 0.3s ease;
#     }
    
#     .mini-card:hover {
#         transform: translateY(-4px);
#         box-shadow: 0 8px 30px rgba(0,0,0,0.12);
#         border-color: rgba(59, 130, 246, 0.2);
#     }
    
#     .mini-card:hover::before {
#         opacity: 1;
#     }
    
#     .mini-card .icon {
#         font-size: 2.2rem;
#         margin-bottom: 0.4rem;
#         display: block;
#     }
    
#     .mini-card .title {
#         font-size: 0.95rem;
#         font-weight: 700;
#         color: #1e293b;
#         margin-bottom: 0.2rem;
#     }
    
#     .mini-card .desc {
#         font-size: 0.75rem;
#         color: #64748b;
#         line-height: 1.3;
#         margin-bottom: 0.3rem;
#     }
    
#     .mini-card .badge {
#         display: inline-block;
#         background: #f1f5f9;
#         padding: 0.15rem 0.7rem;
#         border-radius: 12px;
#         font-size: 0.6rem;
#         color: #475569;
#         font-weight: 600;
#     }
    
#     /* Card Colors */
#     .card-blue .badge { background: #dbeafe; color: #1d4ed8; }
#     .card-green .badge { background: #d1fae5; color: #059669; }
#     .card-purple .badge { background: #ede9fe; color: #7c3aed; }
#     .card-orange .badge { background: #fef3c7; color: #d97706; }
#     .card-cyan .badge { background: #cffafe; color: #0891b2; }
#     .card-pink .badge { background: #fce7f3; color: #db2777; }
    
#     /* Stat Box */
#     .stat-box {
#         text-align: center;
#         padding: 0.8rem;
#         background: white;
#         border-radius: 12px;
#         border: 1px solid #f1f5f9;
#     }
    
#     .stat-box .num {
#         font-size: 1.5rem;
#         font-weight: 800;
#         color: #1e293b;
#     }
    
#     .stat-box .label {
#         font-size: 0.7rem;
#         color: #94a3b8;
#         font-weight: 500;
#     }
    
#     .footer {
#         text-align: center;
#         padding: 1.5rem 0 0.5rem 0;
#         color: #94a3b8;
#         font-size: 0.7rem;
#         border-top: 1px solid #f1f5f9;
#         margin-top: 1.5rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ============================================
# # SIDEBAR - Navigation
# # ============================================
# with st.sidebar:
#     st.markdown("### 📋 Navigation")
    
#     # Navigation buttons
#     nav_items = [
#         {"label": "🏠 Home", "page": "Home"},
#         {"label": "💬 Medical Q&A", "page": "Medical Q&A"},
#         {"label": "🫁 Chest X-Ray", "page": "Chest X-Ray"},
#         {"label": "🦴 Bone X-Ray", "page": "Bone X-Ray"},
#     ]
    
#     if HAS_OCR:
#         nav_items.append({"label": "📄 OCR Report", "page": "OCR Report"})
    
#     for item in nav_items:
#         is_active = st.session_state.page == item["page"]
#         if st.button(
#             item["label"],
#             key=f"sidebar_{item['page']}",
#             use_container_width=True,
#             type="primary" if is_active else "secondary"
#         ):
#             st.session_state.page = item["page"]
#             st.rerun()
    
#     st.markdown("---")
#     st.caption("⚠️ For educational purposes only")

# # ============================================
# # MAIN CONTENT
# # ============================================

# # Get current page
# page = st.session_state.page

# # ============================================
# # PAGE ROUTING
# # ============================================

# if page == "Home":
#     # ============================================
#     # HOME PAGE - Clean version without box
#     # ============================================
    
#     # Hero - Clean title without box
#     st.markdown("""
#     <div style="text-align: center; padding: 0.5rem 0 0.5rem 0;">
#         <h1 class="hero-title">🏥 MediSimplify</h1>
#         <p class="hero-sub">AI-Powered Medical Assistant — Simplifying Healthcare Information</p>
#         <p class="hero-desc">MediSimplify helps you understand complex medical information, analyze X-rays, and extract insights from medical reports — all in one place.</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Feature Cards
#     features = [
#         {"icon": "💬", "title": "Medical Q&A", "desc": "Ask medical questions, get patient-friendly answers", "badge": "RAG · Bilingual", "page": "Medical Q&A", "color": "card-blue"},
#         {"icon": "🫁", "title": "Chest X-Ray", "desc": "AI-powered analysis with CheXpert model", "badge": "14 Classes", "page": "Chest X-Ray", "color": "card-green"},
#         {"icon": "🦴", "title": "Bone X-Ray", "desc": "Fracture, arthritis, tumor detection", "badge": "12 Classes", "page": "Bone X-Ray", "color": "card-purple"},
#         {"icon": "📄", "title": "OCR Report", "desc": "Extract text & explain medical reports", "badge": "Arabic/English", "page": "OCR Report", "color": "card-orange"},
#         {"icon": "🌍", "title": "Bilingual", "desc": "Ask & receive answers in Arabic or English", "badge": "عربي / English", "page": "Home", "color": "card-cyan"},
#         {"icon": "🔬", "title": "AI Explainability", "desc": "Grad-CAM shows what the AI focuses on", "badge": "Transparent AI", "page": "Home", "color": "card-pink"}
#     ]
    
#     for i in range(0, len(features), 3):
#         cols = st.columns(3)
#         for j in range(3):
#             if i + j < len(features):
#                 f = features[i + j]
#                 with cols[j]:
#                     st.markdown(f"""
#                     <div class="mini-card {f['color']}">
#                         <span class="icon">{f['icon']}</span>
#                         <div class="title">{f['title']}</div>
#                         <div class="desc">{f['desc']}</div>
#                         <span class="badge">{f['badge']}</span>
#                     </div>
#                     """, unsafe_allow_html=True)
                    
#                     if f['page'] != "Home":
#                         if st.button(f"🔗 Open {f['title']}", key=f"card_{i}_{j}", use_container_width=True):
#                             st.session_state.page = f['page']
#                             st.rerun()
    
#     # Stats
#     st.markdown("---")
#     col1, col2, col3, col4, col5 = st.columns(5)
#     stats = [
#         {"num": "216K+", "label": "📚 Medical Docs"},
#         {"num": "14", "label": "🩻 Chest Classes"},
#         {"num": "12", "label": "🦴 Bone Classes"},
#         {"num": "2", "label": "🌍 Languages"},
#         {"num": "5", "label": "🧠 AI Models"}
#     ]
#     for idx, stat in enumerate(stats):
#         with [col1, col2, col3, col4, col5][idx]:
#             st.markdown(f"""
#             <div class="stat-box">
#                 <div class="num">{stat['num']}</div>
#                 <div class="label">{stat['label']}</div>
#             </div>
#             """, unsafe_allow_html=True)
    
#     st.markdown('<div class="footer">⚠️ For educational purposes only · Always consult healthcare professionals</div>', unsafe_allow_html=True)

# elif page == "Medical Q&A":
#     medical_qa.show()

# elif page == "Chest X-Ray":
#     image_analysis.show()

# elif page == "Bone X-Ray":
#     bone_analysis.show()

# elif page == "OCR Report" and HAS_OCR:
#     ocr_report.show()

# else:
#     st.info("📄 OCR Report page coming soon!")
# pages/ocr_report.py
# app.py
import streamlit as st

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="MediSimplify",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE - Initialize
# ============================================
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ============================================
# IMPORT PAGES (Only existing pages)
# ============================================
import pages.medical_qa as medical_qa
import pages.image_analysis as image_analysis
import pages.bone_analysis as bone_analysis

try:
    import pages.ocr_report as ocr_report
    HAS_OCR = True
except ImportError:
    ocr_report = None
    HAS_OCR = False

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Sidebar Navigation */
    .nav-btn {
        display: block;
        width: 100%;
        padding: 0.7rem 1rem;
        margin: 0.3rem 0;
        border: none;
        border-radius: 10px;
        background: transparent;
        color: #4b5563;
        font-size: 0.9rem;
        font-weight: 500;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .nav-btn:hover {
        background: #e5e7eb;
        transform: translateX(4px);
    }
    
    .nav-btn.active {
        background: linear-gradient(135deg, #005bea 0%, #00c6fb 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 91, 234, 0.3);
    }
    
    .nav-btn .nav-icon {
        margin-right: 10px;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    
    .hero-sub {
        font-size: 1.1rem;
        color: #475569;
        text-align: center;
        max-width: 600px;
        margin: 0 auto;
        -webkit-text-fill-color: #475569;
    }
    
    .hero-desc {
        font-size: 0.95rem;
        color: #64748b;
        text-align: center;
        max-width: 650px;
        margin: 0.5rem auto 0 auto;
        -webkit-text-fill-color: #64748b;
    }
    
    /* Mini Cards */
    .mini-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .mini-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .mini-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border-color: rgba(59, 130, 246, 0.2);
    }
    
    .mini-card:hover::before {
        opacity: 1;
    }
    
    .mini-card .icon {
        font-size: 2.2rem;
        margin-bottom: 0.4rem;
        display: block;
    }
    
    .mini-card .title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    
    .mini-card .desc {
        font-size: 0.75rem;
        color: #64748b;
        line-height: 1.3;
        margin-bottom: 0.3rem;
    }
    
    .mini-card .badge {
        display: inline-block;
        background: #f1f5f9;
        padding: 0.15rem 0.7rem;
        border-radius: 12px;
        font-size: 0.6rem;
        color: #475569;
        font-weight: 600;
    }
    
    .card-blue .badge { background: #dbeafe; color: #1d4ed8; }
    .card-green .badge { background: #d1fae5; color: #059669; }
    .card-purple .badge { background: #ede9fe; color: #7c3aed; }
    .card-orange .badge { background: #fef3c7; color: #d97706; }
    .card-cyan .badge { background: #cffafe; color: #0891b2; }
    .card-pink .badge { background: #fce7f3; color: #db2777; }
    
    /* Stat Box */
    .stat-box {
        text-align: center;
        padding: 0.8rem;
        background: white;
        border-radius: 12px;
        border: 1px solid #f1f5f9;
    }
    
    .stat-box .num {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1e293b;
    }
    
    .stat-box .label {
        font-size: 0.7rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    .footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #94a3b8;
        font-size: 0.7rem;
        border-top: 1px solid #f1f5f9;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - Navigation
# ============================================
with st.sidebar:
    st.markdown("### 📋 Navigation")
    
    # Navigation buttons
    nav_items = [
        {"label": "🏠 Home", "page": "Home"},
        {"label": "💬 Medical Q&A", "page": "Medical Q&A"},
        {"label": "🫁 Chest X-Ray", "page": "Chest X-Ray"},
        {"label": "🦴 Bone X-Ray", "page": "Bone X-Ray"},
    ]
    
    if HAS_OCR:
        nav_items.append({"label": "📄 OCR Report", "page": "OCR Report"})
    
    for item in nav_items:
        is_active = st.session_state.page == item["page"]
        if st.button(
            item["label"],
            key=f"sidebar_{item['page']}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = item["page"]
            st.rerun()
    
    st.markdown("---")
    st.caption("⚠️ For educational purposes only")

# ============================================
# MAIN CONTENT
# ============================================
page = st.session_state.page

# ============================================
# PAGE ROUTING
# ============================================
if page == "Home":
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 0.5rem 0;">
        <h1 class="hero-title">🏥 MediSimplify</h1>
        <p class="hero-sub">AI-Powered Medical Assistant — Simplifying Healthcare Information</p>
        <p class="hero-desc">MediSimplify helps you understand complex medical information, analyze X-rays, and extract insights from medical reports — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    features = [
        {"icon": "💬", "title": "Medical Q&A", "desc": "Ask medical questions, get patient-friendly answers", "badge": "RAG · Bilingual", "page": "Medical Q&A", "color": "card-blue"},
        {"icon": "🫁", "title": "Chest X-Ray", "desc": "AI-powered analysis with CheXpert model", "badge": "14 Classes", "page": "Chest X-Ray", "color": "card-green"},
        {"icon": "🦴", "title": "Bone X-Ray", "desc": "Fracture, arthritis, tumor detection", "badge": "12 Classes", "page": "Bone X-Ray", "color": "card-purple"},
        {"icon": "📄", "title": "OCR Report", "desc": "Extract text & explain medical reports", "badge": "Arabic/English", "page": "OCR Report", "color": "card-orange"},
        {"icon": "🌍", "title": "Bilingual", "desc": "Ask & receive answers in Arabic or English", "badge": "عربي / English", "page": "Home", "color": "card-cyan"},
        {"icon": "🔬", "title": "AI Explainability", "desc": "Grad-CAM shows what the AI focuses on", "badge": "Transparent AI", "page": "Home", "color": "card-pink"}
    ]
    
    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(features):
                f = features[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="mini-card {f['color']}">
                        <span class="icon">{f['icon']}</span>
                        <div class="title">{f['title']}</div>
                        <div class="desc">{f['desc']}</div>
                        <span class="badge">{f['badge']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if f['page'] != "Home":
                        if st.button(f"🔗 Open {f['title']}", key=f"card_{i}_{j}", use_container_width=True):
                            st.session_state.page = f['page']
                            st.rerun()
    
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    stats = [
        {"num": "216K+", "label": "📚 Medical Docs"},
        {"num": "14", "label": "🩻 Chest Classes"},
        {"num": "12", "label": "🦴 Bone Classes"},
        {"num": "2", "label": "🌍 Languages"},
        {"num": "5", "label": "🧠 AI Models"}
    ]
    for idx, stat in enumerate(stats):
        with [col1, col2, col3, col4, col5][idx]:
            st.markdown(f"""
            <div class="stat-box">
                <div class="num">{stat['num']}</div>
                <div class="label">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="footer">⚠️ For educational purposes only · Always consult healthcare professionals</div>', unsafe_allow_html=True)

elif page == "Medical Q&A":
    medical_qa.show()

elif page == "Chest X-Ray":
    image_analysis.show()

elif page == "Bone X-Ray":
    bone_analysis.show()

elif page == "OCR Report" and HAS_OCR:
    ocr_report.show()

else:
    st.info("📄 OCR Report page coming soon!")