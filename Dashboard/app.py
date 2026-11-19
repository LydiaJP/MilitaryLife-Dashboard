import sys
from pathlib import Path

from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

from auth import sign_in, sign_out

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.military_life_coordinator import agent
from src.military_life_context import MilitaryLifeContext
from src.supabase_client import get_authenticated_supabase_client
from src.supabase_records import get_household

st.set_page_config(
    page_title="MilitaryLife",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Authentication
# --------------------------------------------------

def show_login():
    st.title("🏠 MilitaryLife")
    st.caption("Your AI-powered military household assistant")

    st.subheader("Welcome back")
    st.write("Sign in to access your household dashboard.")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password",
        )

        remember_me = st.checkbox(
            "Remember this device for 30 days",
            value=True,
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True,
        )

    if submitted:
        if not email or not password:
            st.error("Please enter your email and password.")
            return

        try:
            user = sign_in(
                email,
                password,
                remember_me=remember_me,
            )

            st.success("Signed in successfully!")
            st.rerun()


        except Exception as error:
            st.error("Sign-in failed.")
            st.code(
                f"{type(error).__name__}: {error}"
            )



# Require authentication before displaying dashboard.
if not st.session_state.get("supabase_access_token"):
    show_login()
    st.stop()

# --------------------------------------------------
# Sidebar navigation
# --------------------------------------------------

with st.sidebar:
    st.title("🏠 MilitaryLife")
    st.caption("Your AI-powered military household assistant")

    st.divider()


    st.caption("Signed in as")
    st.subheader(
        f"👤 {st.session_state.get('display_name', 'Household Member')}"
    )

    if st.button("Log Out", use_container_width=True):
        sign_out()
        st.rerun()

    st.divider()


    st.subheader("Navigation")

    if "dashboard_navigation" not in st.session_state:
        st.session_state["dashboard_navigation"] = "🏡 Overview"

    if st.button("🏡 Overview", use_container_width=True):
        st.session_state["dashboard_navigation"] = "🏡 Overview"

    if st.button("✨ AI Assistant", use_container_width=True):
        st.session_state["dashboard_navigation"] = "✨ AI Assistant"

    with st.expander("📋 Applications"):
        if st.button("All Applications", use_container_width=True):
            st.session_state["dashboard_navigation"] = "📋 Applications"

        if st.button("Pending Approvals", use_container_width=True):
            st.session_state["dashboard_navigation"] = "🔐 Approvals"

        if st.button("Application History", use_container_width=True):
            st.session_state["dashboard_navigation"] = "📜 Application History"

    with st.expander("✅ Tasks & Deadlines"):
        if st.button("All Tasks", use_container_width=True):
            st.session_state["dashboard_navigation"] = "✅ Tasks & Deadlines"

        if st.button("Upcoming Deadlines", use_container_width=True):
            st.session_state["dashboard_navigation"] = "📅 Upcoming Deadlines"

    with st.expander("👥 Household Profile"):
        if st.button("Household Information", use_container_width=True):
            st.session_state["dashboard_navigation"] = "👥 Household Profile"

    page = st.session_state["dashboard_navigation"]

    st.divider()
    st.caption("AI Providers")
    st.success("Groq — Primary")
    st.info("Gemini — Backup")
    st.caption("Claude Haiku — Coming later")


# --------------------------------------------------
# Overview
# --------------------------------------------------

if page == "🏡 Overview":
    st.title("MilitaryLife Dashboard")
    st.write("Welcome to your military household command center.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Applications", "—")

    with col2:
        st.metric("Pending Tasks", "—")

    with col3:
        st.metric("Upcoming Deadlines", "—")

    st.subheader("Your AI Assistant")
    st.info(
        "Your MilitaryLife Coordinator will help manage "
        "benefits, paperwork, household tasks, and deadlines."
    )

    if st.button("Open AI Assistant", use_container_width=True):
        st.session_state["dashboard_navigation"] = "✨ AI Assistant"
        st.rerun()


# --------------------------------------------------
# AI Assistant
# --------------------------------------------------


elif page == "✨ AI Assistant":
    st.title("✨ MilitaryLife AI Assistant")
    st.caption("Powered by your LangGraph Coordinator")

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask MilitaryLife anything...")

    if prompt:
        access_token = st.session_state["supabase_access_token"]

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("MilitaryLife is thinking..."):
                try:
                    client = get_authenticated_supabase_client(
                        access_token
                    )

                    household = get_household(client)

                    context = MilitaryLifeContext(
                        access_token=access_token,
                        household_id=household["id"],
                    )

                    history = []

                    for message in st.session_state["chat_messages"]:
                        if message["role"] == "user":
                            history.append(
                                HumanMessage(content=message["content"])
                            )
                        else:
                            history.append(
                                AIMessage(content=message["content"])
                            )

                    history.append(HumanMessage(content=prompt))

                    result = agent.invoke(
                        {"messages": history},
                        context=context,
                    )

                    answer = str(result["messages"][-1].content)

                    st.markdown(answer)

                    st.session_state["chat_messages"].extend([
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": answer},
                    ])

                except Exception as error:
                    st.error("MilitaryLife couldn't process your message.")
                    st.exception(error)


    if prompt:
        result = agent.invoke(
    {"messages": history},
    context=context,
)


# --------------------------------------------------
# Applications
# --------------------------------------------------

elif page == "📋 Applications":
    st.title("📋 Applications")
    st.info("Your existing application records will appear here.")


# --------------------------------------------------
# Tasks
# --------------------------------------------------

elif page == "✅ Tasks & Deadlines":
    st.title("✅ Tasks & Deadlines")
    st.info("Your household tasks and deadlines will appear here.")


# --------------------------------------------------
# Household Profile
# --------------------------------------------------

elif page == "👥 Household Profile":
    st.title("👥 Household Profile")
    st.info("Your shared household information will appear here.")


# --------------------------------------------------
# Approvals
# --------------------------------------------------

elif page == "🔐 Approvals":
    st.title("🔐 Application Approvals")
    st.warning(
        "AI-proposed application records will require "
        "your approval before being saved."
    )

elif page == "📜 Application History":
    st.title("📜 Application History")
    st.info("Your household application history will appear here.")

elif page == "📅 Upcoming Deadlines":
    st.title("📅 Upcoming Deadlines")
    st.info("Your upcoming household deadlines will appear here.")
