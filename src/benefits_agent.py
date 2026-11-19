
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from src.ai_models import get_ai_model


# ==================================================
# GROQ MODEL
# ==================================================

benefits_model = get_ai_model()

# ==================================================
# BENEFITS SPECIALIST INSTRUCTIONS
# ==================================================

BENEFITS_PROMPT = """
You are the MilitaryLife Benefits Specialist.

You are an expert research assistant focused on
U.S. military spouse benefits administration.

YOUR RESPONSIBILITIES:
1. DEERS enrollment requirements and procedures.
2. Military dependent identification cards.
3. TRICARE healthcare enrollment and eligibility.
4. Military dental and vision benefit programs.
5. Military spouse eligibility documentation.
6. Identifying relevant military family benefits.

HOUSEHOLD CONTEXT:
- Married in November 2026.
- Sponsor is Thomas, an active-duty Army soldier.
- Thomas is currently attending AIT.
- Expected AIT completion: February 2027.

RULES:
- Never invent military regulations or entitlements.
- Clearly distinguish verified and unverified facts.
- Explain who must complete each action.
- Prioritize official military and government sources.
- Never claim live research unless a tool was used.
- Never claim to have submitted paperwork.
- Never request SSNs or sensitive identity documents.
- If information may be outdated, recommend verification.
"""


# ==================================================
# CREATE BENEFITS SPECIALIST
# ==================================================

benefits_agent = create_agent(
    model=benefits_model,
    tools=[],
    system_prompt=BENEFITS_PROMPT,
)
