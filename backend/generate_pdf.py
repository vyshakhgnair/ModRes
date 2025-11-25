from reportlab.pdfgen import canvas
import os

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "John Doe")
    c.drawString(100, 730, "Software Engineer")
    c.drawString(100, 700, "Experience:")
    c.drawString(100, 680, "- Developed web applications using Vue.js and Python.")
    c.drawString(100, 660, "- Familiar with Docker and Git.")
    c.drawString(100, 630, "Education:")
    c.drawString(100, 610, "- BS in Computer Science")
    c.save()

if __name__ == "__main__":
    create_dummy_pdf("dummy_resume.pdf")
    print("Created dummy_resume.pdf")
