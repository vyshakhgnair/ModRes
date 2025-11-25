import PyPDF2
import docx
import io

class ParserService:
    def extract_text(self, file_storage):
        filename = file_storage.filename.lower()
        
        if filename.endswith('.pdf'):
            return self._extract_from_pdf(file_storage)
        elif filename.endswith('.docx'):
            return self._extract_from_docx(file_storage)
        else:
            return "Unsupported file format. Please upload PDF or DOCX."

    def _extract_from_pdf(self, file_storage):
        try:
            pdf_reader = PyPDF2.PdfReader(file_storage)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    def _extract_from_docx(self, file_storage):
        try:
            doc = docx.Document(file_storage)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
