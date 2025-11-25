from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv
from services.gemini_service import GeminiService
from services.parser_service import ParserService
from services.latex_service import LatexService
from extensions import db, login_manager, bcrypt, migrate
from routes.auth import auth_bp
from models import Application, User, Resume
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key') # Change this in prod
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///modres.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session Cookie Configuration for Cross-Site (Vercel -> Render)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'
app.config['REMEMBER_COOKIE_SECURE'] = True

# Robust Fix for IPv6/Network Unreachable errors (Render/Supabase)
# We resolve the hostname to an IPv4 address and pass it as 'hostaddr'
# This forces the connection over IPv4 while keeping the hostname for SSL verification.
try:
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    # Only apply if it's a postgres connection
    if 'postgres' in db_uri:
        hostname = urlparse(db_uri).hostname
        if hostname:
            # Resolve to IPv4
            ip_address = socket.gethostbyname(hostname)
            print(f"Resolved Database Host {hostname} to IPv4: {ip_address}")
            
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                "pool_pre_ping": True,
                "connect_args": {"hostaddr": ip_address}
            }
        else:
             app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
    else:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
except Exception as e:
    print(f"Warning: Failed to resolve DB hostname to IPv4: {e}")
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

# Fix for Supabase/Render (Postgres)
# Fix for Supabase/Render (Postgres)
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

if app.config['SQLALCHEMY_DATABASE_URI'].startswith("https://"):
    raise ValueError(
        "Invalid DATABASE_URL: The URL starts with 'https://'. "
        "This looks like a Supabase Project URL (API URL). "
        "You need the Connection String (starts with 'postgresql://'). "
        "Go to Supabase Dashboard > Settings > Database > Connection String."
    )

# CORS configuration
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:5174"
]

# Add production URL from environment variable
frontend_url = os.getenv('FRONTEND_URL')
if frontend_url:
    # Support comma-separated URLs
    allowed_origins.extend([url.strip() for url in frontend_url.split(',')])

CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

# Initialize Extensions
db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

gemini_service = GeminiService()
parser_service = ParserService()
latex_service = LatexService()

# Create DB tables
with app.app_context():
    db.create_all()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    
    file = request.files['resume']
    text = parser_service.extract_text(file)
    return jsonify({"text": text})

@app.route('/api/analyze-gap', methods=['POST'])
def analyze_gap():
    data = request.json
    resume_text = data.get('resume_text')
    jd_text = data.get('jd_text')
    
    if not resume_text or not jd_text:
        return jsonify({"error": "Missing resume or JD text"}), 400
        
    analysis = gemini_service.analyze_gap(resume_text, jd_text)
    return jsonify(analysis)

@app.route('/api/score-resume', methods=['POST'])
def score_resume():
    data = request.json
    resume_text = data.get('resume_text')
    jd_text = data.get('jd_text')
    
    score_data = gemini_service.score_resume(resume_text, jd_text)
    return jsonify(score_data)

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    # This expects the final merged data structure
    pdf_path = latex_service.generate_pdf(data)
    return send_file(pdf_path, as_attachment=True)

@app.route('/api/compile-latex', methods=['POST'])
def compile_latex():
    data = request.json
    latex_code = data.get('latex_code')
    
    if not latex_code:
        return jsonify({"error": "No LaTeX code provided"}), 400
        
    try:
        pdf_path = latex_service.compile_pdf_from_string(latex_code)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/initiate-tailoring', methods=['POST'])
@login_required
def initiate_tailoring():
    data = request.json
    company_name = data.get('company_name')
    job_title = data.get('job_title')
    jd_text = data.get('job_description')
    job_url = data.get('job_url')
    
    if not company_name or not job_title:
        return jsonify({"error": "Company name and Job title are required"}), 400
        
    # Check if application exists
    existing_app = Application.query.filter_by(
        user_id=current_user.id,
        company=company_name,
        job_title=job_title
    ).first()
    
    if existing_app:
        # Update JD if provided
        if jd_text:
            existing_app.jd_text = jd_text
        if job_url:
            existing_app.job_url = job_url
        db.session.commit()
        return jsonify({"application_id": existing_app.id, "status": "exists", "data": {
            "company": existing_app.company,
            "job_title": existing_app.job_title,
            "jd_text": existing_app.jd_text
        }})
        
    # Create new application
    new_app = Application(
        user_id=current_user.id,
        company=company_name,
        job_title=job_title,
        jd_text=jd_text,
        job_url=job_url,
        status='Drafting'
    )
    
    try:
        db.session.add(new_app)
        db.session.commit()
        return jsonify({"application_id": new_app.id, "status": "created"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/application/<int:app_id>/finalize-resume', methods=['POST'])
@login_required
def finalize_resume(app_id):
    app_record = Application.query.get_or_404(app_id)
    if app_record.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    tailored_data = data.get('tailored_data')
    pdf_path = data.get('pdf_path') # Optional if we generate it here
    score = data.get('score')
    
    if not tailored_data:
        return jsonify({"error": "Tailored data is required"}), 400

    # Create Resume record
    new_resume = Resume(
        application_id=app_record.id,
        json_data=tailored_data,
        pdf_path=pdf_path,
        score=score
    )
    
    # Update Application status if it was Drafting
    if app_record.status == 'Drafting':
        app_record.status = 'Ready to Apply'
        
    try:
        db.session.add(new_resume)
        db.session.commit()
        return jsonify({"message": "Resume finalized", "resume_id": new_resume.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/tailor-resume', methods=['POST'])
def tailor_resume():
    data = request.json
    resume_text = data.get('resume_text')
    jd_text = data.get('jd_text')
    user_answers = data.get('user_answers', [])
    application_id = data.get('application_id') # Optional now
    
    if not resume_text or not jd_text:
        return jsonify({"error": "Missing resume or JD text"}), 400
        
    # 1. Use Gemini to rewrite/tailor the resume into structured JSON
    tailored_data = gemini_service.tailor_resume(resume_text, jd_text, user_answers)
    
    # 2. Render the LaTeX code (but don't compile yet)
    latex_code = latex_service.render_latex(tailored_data)
    
    # 3. Save Application if user is logged in AND application_id is NOT provided (Legacy/Quick Mode)
    # If application_id IS provided, we don't save yet, we wait for finalize-resume
    if current_user.is_authenticated and not application_id:
        try:
            # Extract company/title from tailored data or fallback
            company = tailored_data.get('experience', [{}])[0].get('company', 'Unknown Company')
            job_title = tailored_data.get('role', 'Unknown Role')
            
            # Check if exists to avoid duplicates in Quick Mode
            existing = Application.query.filter_by(user_id=current_user.id, company=company, job_title=job_title).first()
            if not existing:
                new_app = Application(
                    user_id=current_user.id,
                    job_title=job_title,
                    company=company,
                    jd_text=jd_text,
                    # resume_data=tailored_data, # Deprecated
                    status='Drafting'
                )
                db.session.add(new_app)
                db.session.commit()
                # We should probably create a Resume record here too for legacy support?
                # For now, let's just leave it as is, but maybe add the Resume record.
                new_resume = Resume(
                    application_id=new_app.id,
                    json_data=tailored_data
                )
                db.session.add(new_resume)
                db.session.commit()
                
        except Exception as e:
            print(f"Error saving application: {e}")

    # 4. Return both the data and the source code
    return jsonify({
        "tailored_data": tailored_data,
        "latex_code": latex_code
    })

@app.route('/api/applications', methods=['GET'])
@login_required
def get_applications():
    apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).all()
    return jsonify([{
        'id': app.id,
        'job_title': app.job_title,
        'company': app.company,
        'job_url': app.job_url,
        'status': app.status,
        'notes': app.notes,
        'created_at': app.created_at.isoformat()
    } for app in apps])

@app.route('/api/applications/<int:app_id>', methods=['GET'])
@login_required
def get_application(app_id):
    app_record = Application.query.get_or_404(app_id)
    if app_record.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
        
    # Get latest resume
    latest_resume = Resume.query.filter_by(application_id=app_record.id).order_by(Resume.created_at.desc()).first()
    
    resume_data = None
    latex_code = None
    
    if latest_resume:
        resume_data = latest_resume.json_data
        # Regenerate LaTeX code if we have the data
        if resume_data:
            try:
                latex_code = latex_service.render_latex(resume_data)
            except Exception as e:
                print(f"Error rendering latex for app {app_id}: {e}")

    return jsonify({
        'id': app_record.id,
        'job_title': app_record.job_title,
        'company': app_record.company,
        'job_url': app_record.job_url,
        'jd_text': app_record.jd_text,
        'status': app_record.status,
        'notes': app_record.notes,
        'created_at': app_record.created_at.isoformat(),
        'resume': {
            'json_data': resume_data,
            'latex_code': latex_code,
            'pdf_path': latest_resume.pdf_path if latest_resume else None,
            'score': latest_resume.score if latest_resume else None
        } if latest_resume else None
    })

# ===== PHASE 2: Profile & Auto-Apply Routes =====

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    from models import UserProfile
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({}), 200
    
    return jsonify({
        'full_name': profile.full_name,
        'email': profile.email,
        'phone': profile.phone,
        'linkedin_url': profile.linkedin_url,
        'github_url': profile.github_url,
        'portfolio_url': profile.portfolio_url,
        'work_auth_status': profile.work_auth_status,
        'disability_status': profile.disability_status,
        'veteran_status': profile.veteran_status
    })

@app.route('/api/profile', methods=['POST'])
@login_required
def update_profile():
    from models import UserProfile
    try:
        data = request.json
        
        profile = UserProfile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = UserProfile(user_id=current_user.id)
            db.session.add(profile)
        
        # Update fields
        profile.full_name = data.get('full_name')
        profile.email = data.get('email')
        profile.phone = data.get('phone')
        profile.linkedin_url = data.get('linkedin_url')
        profile.github_url = data.get('github_url')
        profile.portfolio_url = data.get('portfolio_url')
        profile.work_auth_status = data.get('work_auth_status')
        profile.disability_status = data.get('disability_status')
        profile.veteran_status = data.get('veteran_status')
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Error updating profile: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/applications', methods=['POST'])
@login_required
def create_application():
    """Create or update an application"""
    try:
        data = request.json
        
        if data.get('id'):
            # Update existing
            app_record = Application.query.get(data['id'])
            if app_record and app_record.user_id == current_user.id:
                # Update all fields
                app_record.job_title = data.get('job_title', app_record.job_title)
                app_record.company = data.get('company', app_record.company)
                app_record.job_url = data.get('job_url', app_record.job_url)
                app_record.status = data.get('status', app_record.status)
                app_record.notes = data.get('notes', app_record.notes)
                db.session.commit()
                return jsonify({'message': 'Application updated'})
        else:
            # Create new
            new_app = Application(
                user_id=current_user.id,
                job_title=data.get('job_title', ''),
                company=data.get('company', ''),
                job_url=data.get('job_url'),
                status=data.get('status', 'Wishlist'),
                notes=data.get('notes')
            )
            db.session.add(new_app)
            db.session.commit()
            return jsonify({'message': 'Application created', 'id': new_app.id})
        
        return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error creating/updating application: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>', methods=['DELETE'])
@login_required
def delete_application(app_id):
    """Delete an application"""
    try:
        app_record = Application.query.get(app_id)
        if not app_record:
            return jsonify({'error': 'Application not found'}), 404
        
        if app_record.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(app_record)
        db.session.commit()
        return jsonify({'message': 'Application deleted successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting application: {e}")
        return jsonify({'error': str(e)}), 500




@app.route('/api/auto-apply', methods=['POST'])
@login_required
def trigger_auto_apply():
    """Trigger the auto-apply agent"""
    # Check for CLOUD_MODE
    if os.getenv('CLOUD_MODE') == 'true':
        return jsonify({'error': 'Agent mode requires local hosting due to cloud memory limits.'}), 400

    import threading
    import asyncio
    from services.agent_service import AutoApplyAgent
    from models import UserProfile
    
    data = request.json
    job_url = data.get('job_url')
    application_id = data.get('application_id')
    headless = data.get('headless', False)
    
    if not job_url:
        return jsonify({'error': 'job_url is required'}), 400
    
    # Get user profile
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({'error': 'Please complete your profile first'}), 400
    
    profile_dict = {
        'full_name': profile.full_name,
        'email': profile.email,
        'phone': profile.phone,
        'linkedin_url': profile.linkedin_url,
        'github_url': profile.github_url,
        'portfolio_url': profile.portfolio_url
    }
    
    # Get the latest resume for this user (or use a specific one)
    latest_app = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).first()
    
    if not latest_app:
        return jsonify({'error': 'No application found. Please generate a resume first.'}), 400
        
    # Get the latest resume for this application
    latest_resume = Resume.query.filter_by(application_id=latest_app.id).order_by(Resume.created_at.desc()).first()
    
    if not latest_resume:
        return jsonify({'error': 'No resume found for this application.'}), 400
    
    # Generate a PDF from the resume_data (simplified - in production, retrieve the actual PDF)
    resume_path = latest_resume.pdf_path or os.path.join('output', 'latest_resume.pdf')
    # For now, we'll assume the PDF exists. In production, you'd generate it here.
    
    def run_agent():
        """Run the agent in a background thread"""
        agent = AutoApplyAgent(headless=headless)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(agent.start_application(job_url, profile_dict, resume_path))
        
        # Update application status based on result
        if application_id:
            app_record = Application.query.get(application_id)
            if app_record and result.get('success'):
                app_record.status = 'Applied' if result.get('status') == 'applied' else app_record.status
                app_record.notes = f"Agent log:\n" + "\n".join(result.get('log', []))
                db.session.commit()
        
        print(f"Agent completed: {result}")
    
    # Start agent in background thread
    thread = threading.Thread(target=run_agent, daemon=True)
    thread.start()
    
    return jsonify({
        'message': 'Auto-apply agent started',
        'status': 'running'
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
