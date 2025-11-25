from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def test_pdf():
    try:
        c = canvas.Canvas("test_output.pdf", pagesize=letter)
        c.drawString(100, 750, "Hello World")
        c.save()
        print("PDF generated successfully.")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    test_pdf()
