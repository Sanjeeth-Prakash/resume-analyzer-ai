# Universal Resume Analyzer AI

A web application that provides a detailed, real-world analysis of a user's resume against any job description. This tool goes beyond simple keyword matching to parse requirements, understand context, and provide an actionable preparation plan for unmet skills.

## Key Features

- **Multi-Format Input:** Accepts job descriptions via text paste, PDF upload, or image upload (OCR).
- **Intelligent Requirement Parsing:** Correctly understands "AND" conditions (e.g., "Python and C++") and "OR" conditions (e.g., "IT or related").
- **Context-Aware Analysis:** Provides a percentage score based on how many distinct job requirements are met by the resume.
- **Actionable Feedback:** Generates a personalized preparation plan for every unmet technical skill, complete with study topics, project ideas, and learning resources.

## Tech Stack

- **Backend:** Python, Flask
- **Natural Language Processing:** spaCy
- **PDF/Image Reading:** pdfplumber, Pytesseract (OCR)
- **Frontend:** HTML, CSS
- **Deployment:** Render (or Heroku/PythonAnywhere)

## How to Run Locally

1. Clone the repository: `git clone <your-repo-url>`
2. Create and activate a virtual environment: `python -m venv venv` and `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. **Important:** You must have Google's Tesseract OCR engine installed on your system.
5. Run the application: `python app.py`