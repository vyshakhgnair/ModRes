import os
import subprocess
from jinja2 import Environment, FileSystemLoader
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

class LatexService:
    def __init__(self, template_dir='templates'):
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), template_dir)
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            block_start_string='\\BLOCK{',
            block_end_string='}',
            variable_start_string='\\VAR{',
            variable_end_string='}',
            comment_start_string='\\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
        )
        self.env.filters['latex_escape'] = self.latex_escape

    @staticmethod
    def latex_escape(value):
        if not isinstance(value, str):
            return value
        escaped = value.replace('\\', '\\textbackslash{}') \
                    .replace('&', '\\&') \
                    .replace('%', '\\%') \
                    .replace('$', '\\$') \
                    .replace('#', '\\#') \
                    .replace('_', '\\_') \
                    .replace('{', '\\{') \
                    .replace('}', '\\}') \
                    .replace('~', '\\textasciitilde{}') \
                    .replace('^', '\\textasciicircum{}')
        return escaped

    def render_latex(self, data):
        """Renders the LaTeX template with the provided data."""
        try:
            template = self.env.get_template('resume.tex')
            return template.render(data)
        except Exception as e:
            print(f"Error rendering template: {e}")
            return None

    def compile_pdf_from_string(self, latex_content):
        """Compiles a raw LaTeX string into a PDF."""
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        unique_id = str(uuid.uuid4())
        tex_filename = f"resume_{unique_id}.tex"
        pdf_filename = f"resume_{unique_id}.pdf"
        tex_path = os.path.join(output_dir, tex_filename)
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        print(f"tex_path: {tex_path}")
        print(f"pdf_path: {pdf_path}")
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
            
        try:
            subprocess.run(['pdflatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return pdf_path
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"LaTeX compilation failed: {e}")
            raise e

    def generate_pdf(self, data):
        # 1. Render LaTeX
        latex_content = self.render_latex(data)
        
        # 2. Try to compile LaTeX
        if latex_content:
            try:
                return self.compile_pdf_from_string(latex_content)
            except Exception:
                print("Falling back to ReportLab...")
        
        # 3. Fallback
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(output_dir, exist_ok=True)
        unique_id = str(uuid.uuid4())
        pdf_path = os.path.join(output_dir, f"resume_{unique_id}.pdf")
        self.generate_fallback_pdf(data, pdf_path)
        return pdf_path

    def generate_fallback_pdf(self, data, output_path):
        """Generates a simple PDF using ReportLab when LaTeX is unavailable."""
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        y = height - 50
        
        # Helper to draw text and move cursor
        def draw_line(text, font="Helvetica", size=10, space=15):
            nonlocal y
            if y < 50:
                c.showPage()
                y = height - 50
            c.setFont(font, size)
            c.drawString(50, y, text)
            y -= space

        # Header
        draw_line(data.get('name', 'Name'), "Helvetica-Bold", 16, 20)
        contact = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('linkedin', '')}"
        draw_line(contact, "Helvetica", 10, 30)
        
        # Education
        if data.get('education'):
            draw_line("Education", "Helvetica-Bold", 12, 20)
            for edu in data['education']:
                draw_line(f"{edu.get('school')} - {edu.get('degree')}", "Helvetica-Bold", 10, 15)
                draw_line(f"{edu.get('location')} | {edu.get('dates')}", "Helvetica", 10, 20)
        
        # Experience
        if data.get('experience'):
            draw_line("Experience", "Helvetica-Bold", 12, 20)
            for exp in data['experience']:
                draw_line(f"{exp.get('title')} at {exp.get('company')}", "Helvetica-Bold", 10, 15)
                draw_line(f"{exp.get('location')} | {exp.get('dates')}", "Helvetica", 10, 15)
                if exp.get('points'):
                    for point in exp['points']:
                        # Simple wrapping for bullet points
                        lines = simpleSplit(f"- {point}", "Helvetica", 10, width - 100)
                        for line in lines:
                            draw_line(line, "Helvetica", 10, 12)
                y -= 10

        # Skills
        if data.get('skills'):
            draw_line("Skills", "Helvetica-Bold", 12, 20)
            skills = data['skills']
            if isinstance(skills, dict):
                for category, items in skills.items():
                    draw_line(f"{category.capitalize()}: {items}", "Helvetica", 10, 15)
            
        c.save()
