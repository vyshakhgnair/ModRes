import pytest
from services.latex_service import LatexService

def test_latex_escape_characters():
    service = LatexService()
    data = {
        "name": "Test & User",
        "role": "R&D Engineer",
        "email": "test_email@example.com",
        "phone": "123",
        "location": "City",
        "linkedin": "link",
        "github": "git",
        "objective": "To test $ and %",
        "education": [],
        "experience": [],
        "projects": [],
        "skills": {},
        "achievements": []
    }
    
    latex_code = service.render_latex(data)
    
    assert "R\\&D Engineer" in latex_code
    assert "Test \\& User" in latex_code
    assert "test\\_email" in latex_code
    assert "To test \\$ and \\%" in latex_code
