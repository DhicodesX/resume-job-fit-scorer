import re
from pathlib import Path

from preprocess import preprocess  # using your Step 3 code


# ---------- Paths & Helpers ----------

# This finds your project root (resume-job-fit-scorer/)
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_list(filepath: Path) -> list:
    """
    Load a text file where each line is one item.
    Returns a list of lowercase strings.
    """
    items = []
    try:
        with filepath.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(line.lower())
    except FileNotFoundError:
        print(f"[WARN] File not found: {filepath}")
    return items


# Load dictionaries from Step 2 files
TECH_SKILLS = load_list(DATA_DIR / "technical_skills.txt")
SOFT_SKILLS = load_list(DATA_DIR / "soft_skills.txt")
JD_KEYWORDS = load_list(DATA_DIR / "jd_keywords.txt")


# Split skills into single-word and multi-word for better matching
TECH_SINGLE = {s for s in TECH_SKILLS if " " not in s}
TECH_MULTI = {s for s in TECH_SKILLS if " " in s}

SOFT_SINGLE = {s for s in SOFT_SKILLS if " " not in s}
SOFT_MULTI = {s for s in SOFT_SKILLS if " " in s}


# ---------- Extraction Functions ----------

def extract_skills(tokens: list, clean_text: str, single_set: set, multi_set: set) -> set:
    """
    Generic skill extractor:
    - For single-word skills: match against tokens.
    - For multi-word skills: match against the cleaned text (string).
    """
    token_set = set(tokens)

    found = set()

    # Single word skills
    for skill in single_set:
        if skill in token_set:
            found.add(skill)

    # Multi word skills
    for phrase in multi_set:
        if phrase in clean_text:
            found.add(phrase)

    return found


def extract_technical_skills(tokens: list, clean_text: str) -> set:
    return extract_skills(tokens, clean_text, TECH_SINGLE, TECH_MULTI)


def extract_soft_skills(tokens: list, clean_text: str) -> set:
    return extract_skills(tokens, clean_text, SOFT_SINGLE, SOFT_MULTI)


def extract_jd_keywords(clean_text: str) -> set:
    """
    Extract JD-related keywords that appear in clean_text.
    """
    found = set()
    for kw in JD_KEYWORDS:
        if kw in clean_text:
            found.add(kw)
    return found


def extract_experience_years(raw_text: str):
    """
    Try to detect years of experience from the original (un-cleaned) text.
    Looks for patterns like:
        2 years, 3+ years, 5 yrs, etc.
    Returns the maximum number found, or None if nothing.
    """
    text = raw_text.lower()
    pattern = r"(\d+)\s*\+?\s*(?:years?|yrs?)"
    matches = re.findall(pattern, text)

    if not matches:
        return None

    # Convert all matches to int and return the maximum (most experience mentioned)
    years = [int(m) for m in matches]
    return max(years) if years else None


def extract_education(raw_text: str) -> set:
    """
    Look for common degree names in the raw text.
    Returns a set of degrees detected.
    """
    text = raw_text.lower()
    degrees = {
        "b.tech": ["b.tech", "btech", "bachelor of technology"],
        "b.e": ["b.e", "be", "bachelor of engineering"],
        "b.sc": ["b.sc", "bsc", "bachelor of science"],
        "bca": ["bca", "bachelor of computer applications"],
        "m.tech": ["m.tech", "mtech", "master of technology"],
        "m.sc": ["m.sc", "msc", "master of science"],
        "mca": ["mca", "master of computer applications"],
        "bca": ["bca", "bachelor of computer applications"],
        "phd": ["phd", "doctor of philosophy"]
    }

    found_degrees = set()

    for label, patterns in degrees.items():
        for p in patterns:
            if p in text:
                found_degrees.add(label)
                break

    return found_degrees


def extract_features(raw_text: str) -> dict:
    """
    Main function: given raw resume or JD text,
    returns a dictionary of extracted features.
    """
    # Use your existing preprocessing
    pre = preprocess(raw_text)
    clean_text = pre["clean_text"]
    tokens = pre["tokens"]

    tech = extract_technical_skills(tokens, clean_text)
    soft = extract_soft_skills(tokens, clean_text)
    jd_kw = extract_jd_keywords(clean_text)
    exp_years = extract_experience_years(raw_text)
    degrees = extract_education(raw_text)

    return {
        "clean_text": clean_text,
        "tokens": tokens,
        "technical_skills": sorted(tech),
        "soft_skills": sorted(soft),
        "jd_keywords": sorted(jd_kw),
        "experience_years": exp_years,
        "education": sorted(degrees),
    }


# ---------- Quick Manual Test ----------

if __name__ == "__main__":
    sample_resume = """
    I am a B.Tech CSE student with 2 years of experience in Python, SQL, Data Analysis,
    and Machine Learning. I have worked on REST API integration and basic cloud deployment on AWS.
    I have good communication and teamwork skills.
    """

    result = extract_features(sample_resume)

    print("CLEAN TEXT:\n", result["clean_text"])
    print("\nTOKENS:\n", result["tokens"])
    print("\nTECHNICAL SKILLS:\n", result["technical_skills"])
    print("\nSOFT SKILLS:\n", result["soft_skills"])
    print("\nEXPERIENCE (years):\n", result["experience_years"])
    print("\nEDUCATION:\n", result["education"])
    print("\nJD KEYWORDS (if any):\n", result["jd_keywords"])

def extract_resume_features(resume_text: str) -> dict:
    """
    Wrapper for clarity: extract features from a resume.
    """
    return extract_features(resume_text)


def extract_jd_features(jd_text: str) -> dict:
    """
    Wrapper for clarity: extract features from a job description.
    """
    return extract_features(jd_text)
