from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    applications = db.relationship('Application', backref='user', lazy=True)
    profile = db.relationship('UserProfile', backref='user', uselist=False, lazy=True)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    linkedin_url = db.Column(db.String(200), nullable=True)
    github_url = db.Column(db.String(200), nullable=True)
    portfolio_url = db.Column(db.String(200), nullable=True)
    work_auth_status = db.Column(db.String(50), nullable=True) # e.g., 'Citizen', 'Green Card', 'Visa'
    disability_status = db.Column(db.String(50), nullable=True)
    veteran_status = db.Column(db.String(50), nullable=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    job_url = db.Column(db.String(500), nullable=True) # URL to job listing
    jd_text = db.Column(db.Text, nullable=True)
    # resume_data is deprecated in favor of Resume table, but kept for backward compatibility if needed, 
    # or we can just remove it. The plan said remove or deprecate. I will comment it out to be safe.
    # resume_data = db.Column(db.JSON, nullable=True) 
    status = db.Column(db.String(20), default='Wishlist') # Wishlist, Drafting, Applied, Interviewing, Offer, Rejected
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Resume
    resumes = db.relationship('Resume', backref='application', lazy=True, cascade="all, delete-orphan")

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    json_data = db.Column(db.JSON, nullable=False) # The tailored content
    pdf_path = db.Column(db.String(200), nullable=True)
    score = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
