from document_pytesseract import extract_text

class DocumentProcessor:
    def process_resume(self, file_path):
        # Extract text from file
        text = extract_text(file_path)

        # Extract basic info (placeholder for now)
        candidate_name = ""
        email = ""
        phone = ""

        # Simple skills extraction
        skills = []
        skill_keywords = ["Python", "Java", "SQL", "AWS", "React", "Node.js"]
        for skill in skill_keywords:
            if skill.lower() in text.lower():
                skills.append(skill)

        return {
            "raw_text": text,
            "processed_text": text,
            "candidate_name": candidate_name,
            "email": email,
            "phone": phone,
            "ocr_confidence": 100,
            "skills": skills,
            "experience": [],
            "education": [],
            "certifications": [],
            "keywords": []
        }

# ✅ Wrapper function for easy use in routes
def process_document(file_path):
    processor = DocumentProcessor()
    return processor.process_resume(file_path)
