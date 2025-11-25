from app import app, db
from models import User, Application

with app.app_context():
    db.create_all()
    print("Database initialized!")
    
    # Check if we can access User table
    try:
        users = User.query.all()
        print(f"Users found: {len(users)}")
    except Exception as e:
        print(f"Error querying users: {e}")
