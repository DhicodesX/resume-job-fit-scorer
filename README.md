# Resume-to-Job Fit Quick Scorer

A lightweight AI-powered recruitment tool that automates resume screening using Python-based NLP processing.
Built for speed, transparency, and accuracy — without requiring heavy machine learning models.

## Features

- **Resume Text Extraction**: Supports plain text input from resumes
- **Job Description Matching**: Compare resume skills and experience with JD
- **AI-Like Scoring**: Generates a 0–100 Job Fit Score
- **Explainability**: Shows matched, missing, and extra skills
- **Experience Matching**: Automatically extracts years of experience
- **Education Detection**: Identifies degrees like B.Tech, BE, MCA, etc.
- **Keyword Scoring**: Identifies JD-specific keywords
- **CLI Tool**: Evaluate resume vs JD with one command
- **Customizable Dictionaries**: Technical skills, soft skills, JD keywords

## Tech Stack

- **Core Language**: Python
- **NLP**: Custom preprocessing + rule-based extraction
- **Backend Structure**: Flask-compatible architecture
- **Database**: SQLite (resume_scorer.db)
- **OCR**: Tesseract (document_pytesseract.py)
- **File Handling**: Text-based resume/JD samples
- **CLI Tool**: run_evaluation.py

## Prerequisites

- Python 3.8 or later
- Pip installed
- Tesseract OCR for image/PDF extraction

## Installation

# Clone repository
```bash
git clone https://github.com/DhicodesX/resume-job-fit-scorer
cd resume-job-fit-scorer
```

# Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

# Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Scorer

Edit these two files with your own content:
```bash
docs/resume_sample.txt  
docs/jd_sample.txt
```

## Run the evaluator:
```bash
python backend/nlp/run_evaluation.py
```

You will get:
```bash
Job Fit Score (0–100)
Matched skills
Missing skills
Extra skills
Experience comparison
Education match
Keyword match
```

## Project Structure

```
resume-job-fit-scorer/
│
├── backend/
│   ├── nlp/                      # Preprocessing, extraction & scoring
│   │   ├── preprocess.py
│   │   ├── feature_extractor.py
│   │   ├── scoring.py
│   │   └── run_evaluation.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── uploads/
│   ├── app.py
│   ├── extensions.py
│   ├── document_pytesseract.py
│   └── resume_scorer.db
│
├── data/
│   ├── technical_skills.txt
│   ├── soft_skills.txt
│   └── jd_keywords.txt
│
├── docs/
│   ├── resume_sample.txt
│   ├── jd_sample.txt
│   ├── input.txt
│   ├── output.txt
│   └── sample.txt
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Sample Output (from CLI)
```
============================================================
JOB FIT SCORE: 75.0%
============================================================

[SKILLS]
  Match %     : 100%
  Matched     : python, sql, aws, machine learning, rest api
  Extra       : data analysis

[EXPERIENCE]
  Resume years: 2
  JD years    : 3
  Status      : Partially Matched

[EDUCATION]
  Resume degs : b.tech
  JD degs     : b.e, b.tech
  Status      : Matched
```

## MVP Features

- Upload/paste resume & JD text
- Extract skills, keywords, experience, education
- Generate transparent Job Fit Score
- Flexible skills database (editable .txt files)
- Fast, lightweight NLP — no ML model required
- Perfect for HR automation & student career guidance

## Development Timeline

- **Week 1**→ Preprocessing + dictionaries
- **Week 2** → Feature extraction (skills, education, exp)
- **Week 3** → Scoring engine
- **Week 4** → Folder restructuring & CLI tool
- **Week 5** → OCR integration
- **Week 6** → Cleanup, testing, documentation
- **Week 7** → GitHub repo setup
- **Week 8** → Final report & submission

## Future Enhancements

- Resume PDF → text extraction
- Full Flask backend
- React UI for interactive scoring
- ML models for skill inference
- JD classification (Data Analyst / Python Dev / etc.)
- Cloud deployment (Render/AWS)

## Author

**Dhivya S V**  
Intern — Digital Blinc  
Project: Resume-to-Job Fit Quick Scorer


## License

This project is licensed under the ISC License.
