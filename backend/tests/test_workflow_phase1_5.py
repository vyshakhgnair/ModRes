import pytest
from app import app, db
from models import User, Application, Resume
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test user
            user = User(email='test@example.com', password_hash='hashed')
            db.session.add(user)
            db.session.commit()
            
            # Login
            with client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                
        yield client
        
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_workflow_unification(client):
    # 1. Initiate Tailoring (Create Application)
    response = client.post('/api/initiate-tailoring', json={
        'company_name': 'Test Corp',
        'job_title': 'Software Engineer',
        'job_description': 'Must know Python',
        'job_url': 'http://example.com'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'created'
    app_id = data['application_id']
    assert app_id is not None
    
    # Verify Application created in DB
    with app.app_context():
        application = Application.query.get(app_id)
        assert application.company == 'Test Corp'
        assert application.status == 'Drafting'
        
    # 2. Finalize Resume
    tailored_data = {'role': 'Software Engineer', 'experience': []}
    response = client.post(f'/api/application/{app_id}/finalize-resume', json={
        'tailored_data': tailored_data,
        'score': 85
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'resume_id' in data
    
    # Verify Resume created and Application status updated
    with app.app_context():
        resume = Resume.query.filter_by(application_id=app_id).first()
        assert resume is not None
        assert resume.score == 85
        
        application = Application.query.get(app_id)
        assert application.status == 'Ready to Apply'

def test_initiate_existing_application(client):
    # Create app first
    client.post('/api/initiate-tailoring', json={
        'company_name': 'Test Corp',
        'job_title': 'Software Engineer',
        'job_description': 'Old JD'
    })
    
    # Initiate again with new JD
    response = client.post('/api/initiate-tailoring', json={
        'company_name': 'Test Corp',
        'job_title': 'Software Engineer',
        'job_description': 'New JD'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'exists'
    
    # Verify JD updated
    with app.app_context():
        app_record = Application.query.filter_by(company='Test Corp').first()
        assert app_record.jd_text == 'New JD'
