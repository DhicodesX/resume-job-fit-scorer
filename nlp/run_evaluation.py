from pathlib import Path

from scoring import evaluate_resume_against_jd


# ----- Paths -----

# project root: resume-job-fit-scorer/
BASE_DIR = Path(__file__).resolve().parents[2]
DOCS_DIR = BASE_DIR / "docs"


def read_text_file(path: Path) -> str:
    """
    Read a UTF-8 text file and return its content as a string.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
        return ""


def print_report(result: dict):
    """
    Nicely print the evaluation result.
    """
    print("=" * 60)
    print(f"JOB FIT SCORE: {result['job_fit_score']}%")
    print("=" * 60)

    print("\n[SKILLS]")
    skills = result["skills"]
    print(f"  Match %     : {skills['match_percent']}%")
    print(f"  Matched     : {', '.join(skills['matched']) or '-'}")
    print(f"  Missing     : {', '.join(skills['missing']) or '-'}")
    print(f"  Extra       : {', '.join(skills['extra']) or '-'}")

    print("\n[EXPERIENCE]")
    exp = result["experience"]
    print(f"  Resume years: {exp['resume_years']}")
    print(f"  JD years    : {exp['jd_years']}")
    print(f"  Status      : {exp['status']}")
    print(f"  Score       : {exp['score']}%")

    print("\n[EDUCATION]")
    edu = result["education"]
    print(f"  Resume degs : {', '.join(edu['resume_degrees']) or '-'}")
    print(f"  JD degs     : {', '.join(edu['jd_degrees']) or '-'}")
    print(f"  Status      : {edu['status']}")
    print(f"  Score       : {edu['score']}%")

    print("\n[KEYWORDS]")
    kw = result["keywords"]
    print(f"  Match %     : {kw['match_percent']}%")
    print(f"  Matched     : {', '.join(kw['matched']) or '-'}")
    print(f"  Missing     : {', '.join(kw['missing']) or '-'}")

    print("\nDone.\n")


def main():
    resume_path = DOCS_DIR / "resume_sample.txt"
    jd_path = DOCS_DIR / "jd_sample.txt"

    print(f"Using resume file: {resume_path}")
    print(f"Using JD file    : {jd_path}\n")

    resume_text = read_text_file(resume_path)
    jd_text = read_text_file(jd_path)

    if not resume_text or not jd_text:
        print("[ERROR] One or both input files are empty or missing.")
        return

    result = evaluate_resume_against_jd(resume_text, jd_text)
    print_report(result)


if __name__ == "__main__":
    main()
