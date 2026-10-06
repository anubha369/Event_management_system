import sys
from pathlib import Path
import pandas as pd
import random
from datetime import datetime

# Setup paths
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from database import engine, SessionLocal, Base
from models import User, Organizer, Event

def seed_database():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    csv_path = HERE / "Opportunity_Hub_Master_Dataset_5000.csv"
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        return

    print(f"Reading dataset from {csv_path.name}...")
    df = pd.read_csv(csv_path)

    # 1. Create default user and organizers
    organizations = df['organization'].dropna().unique().tolist()
    print(f"Found {len(organizations)} unique organizations in CSV.")

    organizer_map = {}

    for idx, org_name in enumerate(organizations, start=1):
        # Check if user already exists
        email = f"org{idx}@example.com"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                name=f"Admin {org_name}",
                email=email,
                password_hash="hashed_password_123",
                role="ORGANIZER",
                status="ACTIVE"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        organizer = db.query(Organizer).filter(Organizer.organization_name == org_name).first()
        if not organizer:
            organizer = Organizer(
                user_id=user.id,
                organization_name=org_name,
                description=f"Official account for {org_name}",
                verification_status="VERIFIED"
            )
            db.add(organizer)
            db.commit()
            db.refresh(organizer)

        organizer_map[org_name] = organizer.id

    # Default fallback organizer for missing values
    default_org_id = list(organizer_map.values())[0]

    # 2. Check existing event count
    existing_events_count = db.query(Event).count()
    if existing_events_count > 0:
        print(f"Database already contains {existing_events_count} events. Skipping insert.")
        db.close()
        return

    print(f"Populating {len(df)} events into opportunity_hub.db...")

    statuses = ["APPROVED", "PENDING", "REJECTED"]

    event_objects = []
    for _, row in df.iterrows():
        org_name = row.get("organization")
        org_id = organizer_map.get(org_name, default_org_id)

        # Distribute status realistically (e.g. 70% APPROVED, 20% PENDING, 10% REJECTED)
        status = random.choices(statuses, weights=[70, 20, 10])[0]

        event = Event(
            organizer_id=org_id,
            title=str(row.get("title", "Untitled Opportunity")),
            description=str(row.get("description", "")),
            domain=str(row.get("domain", "")),
            category=str(row.get("category", "")),
            mode=str(row.get("mode", "Online")),
            start_date=str(row.get("start_date", "")),
            deadline=str(row.get("deadline", "")),
            location=str(row.get("location", "")),
            prize_money=int(row.get("prize_money_inr", 0)) if pd.notnull(row.get("prize_money_inr")) else 0,
            application_fee=int(row.get("application_fee_inr", 0)) if pd.notnull(row.get("application_fee_inr")) else 0,
            certificate_available=bool(row.get("certificate_available", False)),
            team_required=bool(row.get("team_required", False)),
            eligibility=str(row.get("eligibility_year", "")),
            status=status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        event_objects.append(event)

        # Bulk save in batches of 1000
        if len(event_objects) >= 1000:
            db.bulk_save_objects(event_objects)
            db.commit()
            event_objects = []

    if event_objects:
        db.bulk_save_objects(event_objects)
        db.commit()

    total_inserted = db.query(Event).count()
    print(f"Successfully populated {total_inserted} events into opportunity_hub.db!")
    db.close()

if __name__ == "__main__":
    seed_database()
