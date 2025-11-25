import google.generativeai as genai
import os
import json
import typing_extensions as typing

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables")
        else:
            genai.configure(api_key=api_key)
            
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def analyze_gap(self, resume_text, jd_text):
        prompt = f"""
        You are an expert resume analyst. Compare the following resume text against the job description.
        Identify missing skills or keywords that are critical for the job but missing or weak in the resume.
        For each missing item, formulate a specific question to ask the candidate to gather more context.
        
        Resume Text:
        {resume_text}
        
        Job Description:
        {jd_text}
        
        Output strictly in JSON format with the following structure:
        {{
            "missing_keywords": ["keyword1", "keyword2"],
            "context_questions": [
                {{
                    "keyword": "keyword1",
                    "question": "The JD requires experience with keyword1. Can you describe your experience..."
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Error in analyze_gap: {e}")
            return {"error": str(e)}

    def score_resume(self, resume_text, jd_text):
        prompt = f"""
        Rate this resume against the job description on a scale of 0-100.
        Provide a list of specific improvement suggestions.
        
        Resume Text:
        {resume_text}
        
        Job Description:
        {jd_text}
        
        Output strictly in JSON format:
        {{
            "score": <number range from 0 to 100>,
            "improvement_suggestions": ["suggestion1", "suggestion2"]
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Error in score_resume: {e}")
            return {"error": str(e)}

    def tailor_resume(self, resume_text, jd_text, user_answers):
        prompt = f"""
        You are an expert resume writer. Rewrite the candidate's resume to better match the job description, incorporating their answers to specific questions.
        
        Input:
        - Original Resume Text:
        {resume_text}
        
        - Job Description:
        {jd_text}
        
        - Candidate's Answers to Gap Analysis Questions:
        {json.dumps(user_answers)}
        
        Instructions:
        1. Parse the original resume into structured data.
        2. REWRITE the 'Experience' bullet points and 'Skills' section to target the Job Description.
        3. GENERATE a strong 'Objective' (Summary) tailored to the role.
        4. EXTRACT or GENERATE 'Projects' and 'Achievements' if present or relevant.
        5. INTEGRATE the Candidate's Answers to fill gaps or strengthen the resume.
        6. Output strictly in the following JSON format:
        {{
            "name": "Full Name",
            "role": "Target Job Title (e.g. AI Engineer)",
            "email": "email@example.com",
            "phone": "123-456-7890",
            "location": "City, Country",
            "linkedin": "linkedin url",
            "github": "github url",
            "kaggle": "kaggle url (optional)",
            "objective": "2-3 sentence professional summary tailored to the JD.",
            "education": [
                {{ "school": "University", "location": "City, State", "degree": "Degree Name", "dates": "Year-Year" }}
            ],
            "experience": [
                {{ "title": "Job Title", "company": "Company Name", "location": "City, State", "dates": "Date-Date", "points": ["bullet 1", "bullet 2"] }}
            ],
            "projects": [
                {{ "title": "Project Name", "description": "Brief description", "stack": "Tech Stack (e.g. Python, React)" }}
            ],
            "skills": {{
                "languages": "Python, etc",
                "frameworks": "React, etc",
                "tools": "Git, etc",
                "ai_ml": "PyTorch, etc (if applicable)"
            }},
            "achievements": ["Achievement 1", "Achievement 2"]
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Error in tailor_resume: {e}")
            # Return a basic structure with error to avoid crash
            return {
                "name": "Error Generating Resume",
                "objective": f"Failed to tailor resume: {str(e)}",
                "experience": []
            }
