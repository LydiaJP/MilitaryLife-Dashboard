
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase settings are missing.")

def get_supabase_client():
    """Create a Supabase client without signing in."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_authenticated_supabase_client(access_token: str):
    """Create a Supabase client using a signed-in user's token."""

    if not access_token:
        raise ValueError("An authenticated access token is required.")

    client = get_supabase_client()

    # Apply the user's JWT to database requests.
    client.postgrest.auth(access_token)

    return client
