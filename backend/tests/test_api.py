import pytest
from unittest.mock import MagicMock
import json
import io

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_parse_resume_no_file(client):
    response = client.post('/api/parse-resume')
    assert response.status_code == 400
    assert "error" in response.json

def test_parse_resume_success(client, mocker):
    # Mock the parser service
    mocker.patch('services.parser_service.ParserService.extract_text', return_value="Mocked Resume Text")
    
    data = {
        'resume': (io.BytesIO(b"dummy pdf content"), 'resume.pdf')
    }
    response = client.post('/api/parse-resume', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    assert response.json == {"text": "Mocked Resume Text"}

def test_analyze_gap_success(client, mocker):
    # Mock Gemini Service
    mock_response = {
        "missing_keywords": ["Python"],
        "context_questions": [{"keyword": "Python", "question": "Do you know Python?"}]
    }
    mocker.patch('services.gemini_service.GeminiService.analyze_gap', return_value=mock_response)
    
    data = {
        "resume_text": "I know Java",
        "jd_text": "Looking for Python dev"
    }
    response = client.post('/api/analyze-gap', json=data)
    
    assert response.status_code == 200
    assert response.json == mock_response

def test_score_resume_success(client, mocker):
    # Mock Gemini Service
    mock_response = {
        "score": 85,
        "improvement_suggestions": ["Learn Python"]
    }
    mocker.patch('services.gemini_service.GeminiService.score_resume', return_value=mock_response)
    
    data = {
        "resume_text": "I know Java",
        "jd_text": "Looking for Python dev"
    }
    response = client.post('/api/score-resume', json=data)
    
    assert response.status_code == 200
    assert response.json == mock_response
