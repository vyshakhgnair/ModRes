from app import app, db
from models import UserProfile

with app.app_context():
    # This is a hacky way to update schema in dev without migrations
    # It attempts to create tables that don't exist
    db.create_all()
    print("Database schema updated!")
    
    # Verify UserProfile table exists
    try:
        profiles = UserProfile.query.all()
        print(f"Profiles found: {len(profiles)}")
    except Exception as e:
        print(f"Error querying profiles: {e}")
