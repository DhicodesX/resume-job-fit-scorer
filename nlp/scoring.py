from typing import Dict, List, Set, Tuple

from feature_extractor import (
    extract_resume_features,
    extract_jd_features,
)


# ---------- Skill Matching ----------

def compute_skill_match(resume_skills: List[str], jd_skills: List[str]) -> Dict:
    """
    Compare resume technical skills vs JD technical skills.
    Returns:
        {
            "matched": [...],
            "missing": [...],
            "extra": [...],
            "match_percent": float (0-100)
        }
    """
    resume_set: Set[str] = set(resume_skills)
    jd_set: Set[str] = set(jd_skills)

    matched = sorted(list(resume_set & jd_set))
    missing = sorted(list(jd_set - resume_set))
    extra = sorted(list(resume_set - jd_set))

    if len(jd_set) == 0:
        match_percent = 0.0
    else:
        match_percent = (len(matched) / len(jd_set)) * 100.0

    return {
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "match_percent": round(match_percent, 2),
    }


# ---------- Experience Matching ----------

def compute_experience_match(resume_years, jd_years) -> Dict:
    """
    Compare years of experience from resume vs JD.
    Returns:
        {
            "resume_years": int or None,
            "jd_years": int or None,
            "status": "Fully Matched" | "Partially Matched" | "Not Matched" | "Unknown",
            "score": float (0-100)
        }
    """
    if resume_years is None and jd_years is None:
        return {
            "resume_years": None,
            "jd_years": None,
            "status": "Unknown",
            "score": 0.0,
        }

    if jd_years is None:
        # JD has no explicit requirement, so we can't judge strongly
        return {
            "resume_years": resume_years,
            "jd_years": None,
            "status": "Unknown",
            "score": 50.0,  # neutral
        }

    if resume_years is None:
        return {
            "resume_years": None,
            "jd_years": jd_years,
            "status": "Not Matched",
            "score": 0.0,
        }

    # Both present
    if resume_years >= jd_years:
        status = "Fully Matched"
        score = 100.0
    elif resume_years > 0:
        status = "Partially Matched"
        # e.g., resume 2 vs jd 3 => 2/3 ~ 66%
        score = (resume_years / jd_years) * 100.0
    else:
        status = "Not Matched"
        score = 0.0

    return {
        "resume_years": resume_years,
        "jd_years": jd_years,
        "status": status,
        "score": round(min(max(score, 0.0), 100.0), 2),
    }


# ---------- Education Matching ----------

def compute_education_match(resume_degrees: List[str], jd_degrees: List[str]) -> Dict:
    """
    Compare education sets.
    If there is any overlap => Matched.
    If JD has no degrees listed => Unknown/Neutral.
    """
    resume_set = set(resume_degrees)
    jd_set = set(jd_degrees)

    if not resume_set and not jd_set:
        return {
            "resume_degrees": [],
            "jd_degrees": [],
            "status": "Unknown",
            "score": 0.0,
        }

    if not jd_set:
        # JD doesn't specify, neutral
        return {
            "resume_degrees": sorted(list(resume_set)),
            "jd_degrees": [],
            "status": "Unknown",
            "score": 50.0,
        }

    overlap = resume_set & jd_set
    if overlap:
        status = "Matched"
        score = 100.0
    else:
        status = "Not Matched"
        score = 0.0

    return {
        "resume_degrees": sorted(list(resume_set)),
        "jd_degrees": sorted(list(jd_set)),
        "status": status,
        "score": score,
    }


# ---------- Keyword Matching ----------

def compute_keyword_match(resume_keywords: List[str], jd_keywords: List[str]) -> Dict:
    """
    Compare JD-related keywords found in resume text vs JD text.
    """
    resume_set = set(resume_keywords)
    jd_set = set(jd_keywords)

    matched = sorted(list(resume_set & jd_set))
    missing = sorted(list(jd_set - resume_set))

    if len(jd_set) == 0:
        match_percent = 0.0
    else:
        match_percent = (len(matched) / len(jd_set)) * 100.0

    return {
        "matched": matched,
        "missing": missing,
        "match_percent": round(match_percent, 2),
    }


# ---------- Final Fit Score ----------

def calculate_fit_score(
    skill_match_percent: float,
    exp_score: float,
    edu_score: float,
    keyword_match_percent: float,
    weights=None,
) -> float:
    """
    Combine scores into final Job Fit Score using weights.
    Default weights:
        skills: 0.4
        experience: 0.3
        education: 0.15
        keywords: 0.15
    """
    if weights is None:
        weights = {
            "skills": 0.4,
            "experience": 0.3,
            "education": 0.15,
            "keywords": 0.15,
        }

    final = (
        skill_match_percent * weights["skills"] / 100.0 +
        exp_score * weights["experience"] / 100.0 +
        edu_score * weights["education"] / 100.0 +
        keyword_match_percent * weights["keywords"] / 100.0
    ) * 100.0

    return round(final, 2)


# ---------- Main API ----------

def evaluate_resume_against_jd(resume_text: str, jd_text: str) -> Dict:
    """
    High-level function:
    - Extract features from resume and JD
    - Compute all partial scores
    - Compute final Job Fit Score
    """
    resume_feat = extract_resume_features(resume_text)
    jd_feat = extract_jd_features(jd_text)

    # Technical skills
    skill_match = compute_skill_match(
        resume_feat["technical_skills"],
        jd_feat["technical_skills"],
    )

    # Experience
    exp_match = compute_experience_match(
        resume_feat["experience_years"],
        jd_feat["experience_years"],
    )

    # Education
    edu_match = compute_education_match(
        resume_feat["education"],
        jd_feat["education"],
    )

    # Keywords (we'll reuse jd_keywords sets)
    kw_match = compute_keyword_match(
        resume_feat["jd_keywords"],
        jd_feat["jd_keywords"],
    )

    # Final score
    final_score = calculate_fit_score(
        skill_match_percent=skill_match["match_percent"],
        exp_score=exp_match["score"],
        edu_score=edu_match["score"],
        keyword_match_percent=kw_match["match_percent"],
    )

    return {
        "job_fit_score": final_score,
        "skills": skill_match,
        "experience": exp_match,
        "education": edu_match,
        "keywords": kw_match,
        "resume_features": resume_feat,
        "jd_features": jd_feat,
    }


# ---------- Quick Manual Test ----------

if __name__ == "__main__":
    sample_resume = """
    I am a B.Tech CSE student with 2 years of experience in Python, SQL, Data Analysis,
    and Machine Learning. I have worked on REST API integration and basic cloud deployment on AWS.
    I have good communication and teamwork skills.
    """

    sample_jd = """
    We are looking for a Python Developer with at least 3 years of experience.
    Required skills: Python, SQL, Machine Learning, REST API, AWS.
    The candidate should have a B.Tech or B.E in Computer Science or related field.
    Good communication skills and ability to work in a team are essential.
    """

    result = evaluate_resume_against_jd(sample_resume, sample_jd)

    print("JOB FIT SCORE:", result["job_fit_score"])
    print("\nSKILL MATCH:", result["skills"])
    print("\nEXPERIENCE MATCH:", result["experience"])
    print("\nEDUCATION MATCH:", result["education"])
    print("\nKEYWORD MATCH:", result["keywords"])
