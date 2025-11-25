import os
from app import app, db
from sqlalchemy import text

def init_supabase_db():
    """
    Initialize the database tables on Supabase.
    This script should be run once after deploying or setting up the DB.
    """
    print("Initializing Supabase Database...")
    
    # Ensure we are using the correct database URL
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL environment variable is not set.")
        return

    print(f"Connecting to: {db_url.split('@')[1] if '@' in db_url else 'Unknown'}")

    with app.app_context():
        try:
            # Test connection
            db.session.execute(text('SELECT 1'))
            print("Connection successful.")
            
            # Create tables
            print("Creating tables...")
            db.create_all()
            print("Tables created successfully.")
            
        except Exception as e:
            print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_supabase_db()
