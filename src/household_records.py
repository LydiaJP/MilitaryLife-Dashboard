
import sqlite3
import uuid
from pathlib import Path


# ==================================================
# DATABASE CONFIGURATION
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_DIR / "militarylife.db"


def get_connection():
    """Connect to the MilitaryLife SQLite database."""

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

def initialize_database():
    """Create all MilitaryLife database tables."""

    with get_connection() as conn:

        # ------------------------------------------
        # Applications
        # ------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                responsible_person TEXT,
                status TEXT NOT NULL DEFAULT 'Not started',
                submitted_date TEXT,
                deadline TEXT,
                next_followup TEXT,
                source_url TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ------------------------------------------
        # Application proposals
        # ------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS application_proposals (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                responsible_person TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                approved_at TEXT,
                saved_application_id INTEGER,
                FOREIGN KEY (saved_application_id)
                    REFERENCES applications(id)
            )
        """)

        # ------------------------------------------
        # Household tasks
        # ------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                title TEXT NOT NULL,
                assigned_to TEXT,
                status TEXT NOT NULL DEFAULT 'Not started',
                due_date TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
            )
        """)

        # ------------------------------------------
        # Application status history
        # ------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS application_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                old_status TEXT,
                new_status TEXT NOT NULL,
                change_source TEXT NOT NULL,
                notes TEXT,
                changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
            )
        """)

        # ------------------------------------------
        # Reminders and deadlines
        # ------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                title TEXT NOT NULL,
                reminder_date TEXT NOT NULL,
                recurring_rule TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id)
                    REFERENCES applications(id)
            )
        """)

        # ------------------------------------------
        # Installations and PCS history
        # ------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS installations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                installation_name TEXT NOT NULL,
                state_or_country TEXT,
                assignment_type TEXT,
                start_date TEXT,
                end_date TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ------------------------------------------
        # Military resources and programs
        # ------------------------------------------

        conn.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                installation_id INTEGER,
                official_url TEXT,
                eligibility_notes TEXT,
                last_verified TEXT,
                notes TEXT,
                FOREIGN KEY (installation_id)
                    REFERENCES installations(id)
            )
        """)

    print("MilitaryLife database initialized successfully!")
    print(f"Database location: {DATABASE_FILE}")


# ==================================================
# APPLICATION MANAGEMENT
# ==================================================

def add_application(name, category, responsible_person=None):
    """Create a new household application record."""

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO applications
                (name, category, responsible_person)
            VALUES (?, ?, ?)
            """,
            (name, category, responsible_person)
        )

        return cursor.lastrowid


def get_applications():
    """Retrieve all household applications."""

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                id,
                name,
                category,
                responsible_person,
                status
            FROM applications
            ORDER BY id
            """
        ).fetchall()

        return [dict(row) for row in rows]


# ==================================================
# APPLICATION STATUS TRACKING
# ==================================================

def update_application_status(
    application_id,
    new_status,
    change_source,
    notes=None
):
    """Update an application and record its status history."""

    allowed_statuses = {
        "Not started",
        "Preparing",
        "Submitted",
        "Pending review",
        "Action required",
        "Approved",
        "Denied",
        "Completed"
    }

    if new_status not in allowed_statuses:
        raise ValueError(f"Invalid status: {new_status}")

    if not change_source or not change_source.strip():
        raise ValueError("A change source is required.")

    with get_connection() as conn:

        application = conn.execute(
            """
            SELECT status
            FROM applications
            WHERE id = ?
            """,
            (application_id,)
        ).fetchone()

        if application is None:
            raise ValueError("Application not found.")

        old_status = application["status"]

        conn.execute(
            """
            UPDATE applications
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (new_status, application_id)
        )

        conn.execute(
            """
            INSERT INTO application_history (
                application_id,
                old_status,
                new_status,
                change_source,
                notes
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                application_id,
                old_status,
                new_status,
                change_source,
                notes
            )
        )

    return {
        "application_id": application_id,
        "previous_status": old_status,
        "current_status": new_status,
        "change_source": change_source
    }


def get_application_history(application_id):
    """Retrieve the status history of an application."""

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                old_status,
                new_status,
                change_source,
                notes,
                changed_at
            FROM application_history
            WHERE application_id = ?
            ORDER BY id
            """,
            (application_id,)
        ).fetchall()

        return [dict(row) for row in rows]


# ==================================================
# APPLICATION PROPOSAL MANAGEMENT
# ==================================================

def create_application_proposal(
    name,
    category,
    responsible_person="Unassigned"
):
    """Create a pending application proposal.

    This does not create an actual application.
    """

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Application name is required.")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Application category is required.")

    proposal_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO application_proposals (
                id,
                name,
                category,
                responsible_person
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                proposal_id,
                name.strip(),
                category.strip(),
                responsible_person
            )
        )

    return {
        "proposal_id": proposal_id,
        "name": name.strip(),
        "category": category.strip(),
        "responsible_person": responsible_person,
        "status": "Pending",
        "saved": False
    }


def get_application_proposal(proposal_id):
    """Retrieve a previously created application proposal."""

    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM application_proposals
            WHERE id = ?
            """,
            (proposal_id,)
        ).fetchone()

        return dict(row) if row else None


def approve_application_proposal(proposal_id):
    """Approve and save a proposal.

    IMPORTANT: This function must only be called by
    trusted application code after user confirmation.
    Never expose it directly as an AI agent tool.
    """

    with get_connection() as conn:
        proposal = conn.execute(
            """
            SELECT *
            FROM application_proposals
            WHERE id = ?
            """,
            (proposal_id,)
        ).fetchone()

        if proposal is None:
            raise ValueError("Proposal not found.")

        if proposal["status"] != "Pending":
            raise ValueError(
                "This proposal has already been processed."
            )

        # Prevent duplicate applications
        normalized_name = " ".join(
            proposal["name"].casefold().split()
        )

        existing = conn.execute(
            "SELECT id, name FROM applications"
        ).fetchall()

        for application in existing:
            existing_name = " ".join(
                application["name"].casefold().split()
            )

            if existing_name == normalized_name:
                raise ValueError(
                    "This application is already being tracked."
                )

        # Save the approved application
        cursor = conn.execute(
            """
            INSERT INTO applications (
                name,
                category,
                responsible_person
            )
            VALUES (?, ?, ?)
            """,
            (
                proposal["name"],
                proposal["category"],
                proposal["responsible_person"]
            )
        )

        application_id = cursor.lastrowid

        # Mark the proposal as approved
        conn.execute(
            """
            UPDATE application_proposals
            SET status = 'Approved',
                approved_at = CURRENT_TIMESTAMP,
                saved_application_id = ?
            WHERE id = ?
            """,
            (application_id, proposal_id)
        )

    return {
        "saved": True,
        "application_id": application_id,
        "proposal_id": proposal_id,
        "name": proposal["name"],
        "status": "Not started"
    }

if __name__ == "__main__":
    initialize_database()
