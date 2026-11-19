
import json
from pathlib import Path

# Save the profile in the MilitaryLife project folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFILE_FILE = PROJECT_DIR / "household_profile.json"

# Questions the profile manager will eventually ask.
PROFILE_QUESTIONS = {
    "current_location": "What city and state are you currently living in?",
    "spouse_employment": "What is your current employment status?",
    "children": "Do you and Thomas have any children or other dependents?",
    "sponsor_rank": "What is Thomas's current military rank?",
    "sponsor_installation": "Which military installation is Thomas currently assigned to?",
    "next_duty_station": "Do you know Thomas's next duty station?",
    "deers_status": "Have you been enrolled in DEERS?",
    "dependent_id_status": "Have you received your military dependent ID?",
    "tricare_status": "Have you enrolled in a TRICARE health plan?",
    "bah_status": "Has Thomas submitted the paperwork to update his housing allowance?"
}

# Initial household information.
# Unknown details are left as null.
DEFAULT_PROFILE = {
    "marriage_month": "November 2026",
    "sponsor_name": "Thomas",
    "sponsor_branch": "U.S. Army",
    "sponsor_duty_status": "Active duty",
    "sponsor_training": "AIT",
    "expected_ait_completion": "February 2027",
    "spouse_education": "Bachelor's degree in Computer Science",
    "current_location": None,
    "spouse_employment": None,
    "children": None,
    "sponsor_rank": None,
    "sponsor_installation": None,
    "next_duty_station": None,
    "deers_status": None,
    "dependent_id_status": None,
    "tricare_status": None,
    "bah_status": None
}


def load_profile():
    """Load the saved household profile."""
    if not PROFILE_FILE.exists():
        return DEFAULT_PROFILE.copy()

    with PROFILE_FILE.open("r", encoding="utf-8") as file:
        saved = json.load(file)

    # Preserve newly added fields if the profile schema changes.
    return {**DEFAULT_PROFILE, **saved}


def save_profile(profile):
    """Save the household profile locally."""
    with PROFILE_FILE.open("w", encoding="utf-8") as file:
        json.dump(profile, file, indent=4)


def update_profile(field, value):
    """Update an approved household profile field."""
    if field not in DEFAULT_PROFILE:
        raise ValueError(f"Unknown profile field: {field}")

    if not isinstance(value, (str, bool)) and value is not None:
        raise ValueError("Profile values must be text, boolean, or null.")

    profile = load_profile()
    profile[field] = value
    save_profile(profile)
    return profile


def get_next_question():
    """Return the next unanswered household question."""
    profile = load_profile()

    for field, question in PROFILE_QUESTIONS.items():
        if profile.get(field) is None:
            return {"field": field, "question": question}

    return None


if __name__ == "__main__":
    profile = load_profile()
    print("Current household profile:")
    print(json.dumps(profile, indent=4))

    next_question = get_next_question()
    print("\nNext interview question:")
    print(next_question["question"] if next_question else "Profile complete!")
