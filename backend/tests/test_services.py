import pytest
from services.latex_service import LatexService
import os

def test_latex_generation_structure():
    service = LatexService()
    # We can't easily test full PDF generation without pdflatex installed in the environment
    # But we can test if the service initializes and methods exist
    assert hasattr(service, 'generate_pdf')
    assert hasattr(service, 'render_latex')

def test_render_latex_template():
    service = LatexService()
    data = {
        "name": "Test User",
        "role": "Developer",
        "email": "test@test.com",
        "phone": "123",
        "location": "Test City",
        "linkedin": "link",
        "github": "git",
        "objective": "To test",
        "education": [],
        "experience": [],
        "projects": [],
        "skills": {"languages": "Python"},
        "achievements": []
    }
    
    # This might fail if templates folder isn't found relative to where test runs
    # So we might need to mock jinja environment or ensure path is correct
    # For now, let's just try to call it and catch potential template not found error
    # to at least verify the logic runs up to that point.
    
    try:
        latex_code = service.render_latex(data)
        assert "Test User" in latex_code
        assert "Developer" in latex_code
    except Exception as e:
        # If template not found, that's a configuration issue we might need to fix
        # but for unit testing logic, we might want to mock the template loader
        pytest.fail(f"Latex rendering failed: {e}")
