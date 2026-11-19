
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from groq import (
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
)

load_dotenv()


def get_ai_model():
    """Return the primary Groq model with a Gemini backup."""

    groq = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        timeout=30,
        max_retries=0,
    )

    gemini = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        max_retries=0,
        timeout=30,
    )

    return groq.with_fallbacks(
        [gemini],
        exceptions_to_handle=(
            RateLimitError,
            APIConnectionError,
            APITimeoutError,
            InternalServerError,
        ),
    )
