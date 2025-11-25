# ModRes - Intelligent Resume & Job Application Tracker

ModRes is a powerful, AI-driven application designed to streamline your job search process. It combines a dynamic resume builder, a job application tracker (CRM), and AI-powered tools to help you craft the perfect resume and manage your applications efficiently.

## 🚀 Features

*   **AI-Powered Resume Builder:** Leverage Google Gemini AI to optimize your resume content and perform gap analysis against job descriptions.
*   **Smart Resume Management:** Create, edit, and manage multiple versions of your resume.
*   **PDF Generation:** Export your resumes to professional-quality PDF documents using ReportLab.
*   **Job Application Tracker:** A built-in CRM to track the status of your job applications (Applied, Interview, Offer, Rejected).
*   **Auto-Apply Agent:** (Experimental) Automated application features using Playwright.
*   **User Authentication:** Secure login and registration system to protect your data.

## 🛠️ Tech Stack

### Backend
*   **Framework:** Flask (Python)
*   **Database:** SQLite (with Flask-SQLAlchemy & Flask-Migrate)
*   **AI Engine:** Google Gemini (via `google-generativeai`)
*   **PDF Generation:** ReportLab, PyPDF2
*   **Automation:** Playwright
*   **Authentication:** Flask-Login, Flask-Bcrypt

### Frontend
*   **Framework:** Vue 3
*   **Build Tool:** Vite
*   **Styling:** TailwindCSS
*   **State Management:** Pinia
*   **Routing:** Vue Router
*   **HTTP Client:** Axios

## ⚙️ Installation & Setup

### Prerequisites
*   Python 3.8+
*   Node.js & npm
*   Google Gemini API Key

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Install Playwright browsers (if required for auto-apply features):
```bash
playwright install
```

**Environment Configuration:**
Create a `.env` file in the `backend` directory and add your secrets:
```env
GOOGLE_API_KEY=your_gemini_api_key
SECRET_KEY=your_flask_secret_key
# Add other necessary env variables
```

Initialize the database:
```bash
python init_db.py
# OR
flask db upgrade
```

Run the server:
```bash
python app.py
```
The backend will run on `http://localhost:5000`.

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
```
The frontend will run on `http://localhost:5173` (or the port shown in the terminal).

## 📝 Usage

1.  Register for a new account or log in.
2.  Use the **Resume Builder** to create your profile and generate resumes.
3.  Use the **Job Tracker** to add jobs you are interested in.
4.  Use the **AI Tools** to tailor your resume for specific job descriptions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
