
import streamlit as st
from supabase import create_client


def create_supabase_client():
    """Create a Supabase client."""
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_PUBLISHABLE_KEY"],
    )


def sign_in(email: str, password: str, remember_me=False):
    """Authenticate a user with Supabase."""
    client = create_supabase_client()

    response = client.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    if not response.session or not response.user:
        raise ValueError("Sign-in failed.")

    st.session_state["supabase_access_token"] = (
        response.session.access_token
    )
    st.session_state["supabase_refresh_token"] = (
        response.session.refresh_token
    )
    st.session_state["supabase_user_id"] = response.user.id

    metadata = response.user.user_metadata or {}

    st.session_state["display_name"] = (
        metadata.get("display_name")
        or metadata.get("full_name")
        or metadata.get("name")
        or (response.user.email or "").split("@")[0]
        or "Household Member"
    )

    return response.user


def sign_out():
    """Sign out of Supabase and clear local session data."""
    try:
        access_token = st.session_state.get(
            "supabase_access_token"
        )
        refresh_token = st.session_state.get(
            "supabase_refresh_token"
        )

        if access_token and refresh_token:
            client = create_supabase_client()
            client.auth.set_session(
                access_token,
                refresh_token,
            )
            client.auth.sign_out()

    except Exception:
        pass

    for key in (
        "supabase_access_token",
        "supabase_refresh_token",
        "supabase_user_id",
        "display_name",
        "remember_me",
        "chat_messages",
        "dashboard_navigation",
    ):
        st.session_state.pop(key, None)
