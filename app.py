
import streamlit as st

st.set_page_config(
    page_title="MilitaryLife",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="auto",
)

PAGES = [
    "🏡 Overview",
    "✨ AI Assistant",
    "📋 Applications",
    "✅ Tasks & Deadlines",
    "👥 Household Profile",
    "🔐 Approvals",
]

# Keep the selected page when the app reruns.
if "page" not in st.session_state:
    st.session_state.page = PAGES[0]

# Desktop sidebar
with st.sidebar:
    st.title("🏠 MilitaryLife")
    st.caption("Military Household Management")
    st.divider()

    st.radio(
        "Navigation",
        PAGES,
        key="page",
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("MilitaryLife — Development Preview")

# Always-visible navigation, including on mobile
st.selectbox(
    "Navigate MilitaryLife",
    PAGES,
    key="page",
)

page = st.session_state.page

st.divider()

if page == "🏡 Overview":
    st.title("🏠 MilitaryLife Dashboard")
    st.write("Your AI-powered military household command center.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Applications", "—")
    col2.metric("Pending Tasks", "—")
    col3.metric("Upcoming Deadlines", "—")

    st.subheader("Welcome to MilitaryLife")
    st.info(
        "We're building a shared platform for military "
        "benefits, applications, household tasks, and AI assistance."
    )

elif page == "✨ AI Assistant":
    st.title("✨ AI Assistant")
    st.info("LangGraph AI integration is in development.")

elif page == "📋 Applications":
    st.title("📋 Applications")
    st.info("Application tracking is coming soon.")

elif page == "✅ Tasks & Deadlines":
    st.title("✅ Tasks & Deadlines")
    st.info("Shared task management is coming soon.")

elif page == "👥 Household Profile":
    st.title("👥 Household Profile")
    st.info("Secure household profiles are coming soon.")

elif page == "🔐 Approvals":
    st.title("🔐 Approvals")
    st.info("Review and approval workflows are coming soon.")
