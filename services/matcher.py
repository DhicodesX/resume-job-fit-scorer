# services/matcher.py
from difflib import SequenceMatcher
import re

def preprocess(text):
    """Clean and normalize text for better comparison."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def calculate_match_score(resume_text, job_text):
    """Calculate how well the resume matches the job description."""
    resume_clean = preprocess(resume_text)
    job_clean = preprocess(job_text)
    ratio = SequenceMatcher(None, resume_clean, job_clean).ratio()
    return round(ratio * 100, 2)
