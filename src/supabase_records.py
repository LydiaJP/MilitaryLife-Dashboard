
from .supabase_client import get_supabase_client


def get_household(client):
    """Retrieve the signed-in user's household."""

    response = (
        client.table("households")
        .select("id, name")
        .limit(1)
        .execute()
    )

    if not response.data:
        raise ValueError(
            "No household found for this account."
        )

    return response.data[0]


def get_applications(client, household_id):
    """Retrieve applications belonging to a household."""

    response = (
        client.table("applications")
        .select(
            "id, name, category, responsible_person, status"
        )
        .eq("household_id", household_id)
        .order("id")
        .execute()
    )

    return response.data

import uuid


def create_application_proposal(
    client,
    household_id,
    name,
    category,
    responsible_person="Unassigned"
):
    """Create a pending application proposal in Supabase."""

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Application name is required.")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Application category is required.")

    proposal = {
        "id": str(uuid.uuid4()),
        "household_id": household_id,
        "name": name.strip(),
        "category": category.strip(),
        "responsible_person": responsible_person,
        "status": "Pending",
    }

    response = (
        client.table("application_proposals")
        .insert(proposal)
        .execute()
    )

    return {
        "proposal_id": response.data[0]["id"],
        "name": response.data[0]["name"],
        "category": response.data[0]["category"],
        "responsible_person": response.data[0]["responsible_person"],
        "status": "Pending",
        "saved": False,
    }

def get_pending_proposals(client, household_id):
    """Retrieve pending proposals for the authenticated household."""

    response = (
        client.table("application_proposals")
        .select("id, name, category, responsible_person, status")
        .eq("household_id", household_id)
        .eq("status", "Pending")
        .execute()
    )

    return response.data
