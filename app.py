import streamlit as st

st.set_page_config(
    page_title="MilitaryLife",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Page configuration
# -----------------------------

PAGES = {
    "Overview": "🏡 Overview",
    "AI Assistant": "✨ AI Assistant",
    "All Applications": "📋 All Applications",
    "In Progress": "⏳ In Progress",
    "Completed": "✅ Completed",
    "All Tasks": "📌 All Tasks",
    "Upcoming Deadlines": "📅 Upcoming Deadlines",
    "Household Members": "👥 Household Members",
    "Household Information": "🏠 Household Information",
    "Pending Approvals": "🔐 Pending Approvals",
    "Approval History": "📜 Approval History",
}

if "page" not in st.session_state:
    st.session_state.page = "Overview"


def navigate(page):
    st.session_state.page = page


def nav_button(page):
    selected = st.session_state.page == page

    st.button(
        PAGES[page],
        key=f"nav_{page}",
        use_container_width=True,
        type="primary" if selected else "secondary",
        on_click=navigate,
        args=(page,),
    )


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.title("🏠 MilitaryLife")
    st.caption("Military Household Management")

    st.divider()

    nav_button("Overview")
    nav_button("AI Assistant")

    st.divider()

    with st.expander("📋 Applications", expanded=True):
        nav_button("All Applications")
        nav_button("In Progress")
        nav_button("Completed")

    with st.expander("✅ Tasks & Deadlines"):
        nav_button("All Tasks")
        nav_button("Upcoming Deadlines")

    with st.expander("👥 Household Profile"):
        nav_button("Household Members")
        nav_button("Household Information")

    with st.expander("🔐 Approvals"):
        nav_button("Pending Approvals")
        nav_button("Approval History")

    st.divider()
    st.caption("MilitaryLife — Development Preview")


# -----------------------------
# Main dashboard
# -----------------------------

page = st.session_state.page

if page == "Overview":
    st.title("🏠 MilitaryLife Dashboard")
    st.write("Your AI-powered military household command center.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Applications", "—")
    col2.metric("Pending Tasks", "—")
    col3.metric("Upcoming Deadlines", "—")

    st.subheader("Welcome to MilitaryLife")

    st.info(
        "We're building a shared platform for military "
        "benefits, applications, household tasks, "
        "and AI assistance."
    )

elif page == "AI Assistant":
    st.title("✨ MilitaryLife AI Assistant")
    st.caption("Your AI-powered military household coordinator")
    st.info("LangGraph AI integration is in development.")

elif page in ["All Applications", "In Progress", "Completed"]:
    st.title(PAGES[page])
    st.info("Application tracking is coming soon.")

elif page in ["All Tasks", "Upcoming Deadlines"]:
    st.title(PAGES[page])
    st.info("Shared task management is coming soon.")

elif page in ["Household Members", "Household Information"]:
    st.title(PAGES[page])
    st.info("Secure household profiles are coming soon.")

elif page in ["Pending Approvals", "Approval History"]:
    st.title(PAGES[page])
    st.info("Application approval workflows are coming soon.")
