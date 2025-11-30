from extensions import db
import datetime
import json

class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(100), nullable=True)
    raw_text = db.Column(db.Text, nullable=True)
    processed_text = db.Column(db.Text, nullable=True)
    candidate_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.Text, nullable=True)          # JSON string
    experience = db.Column(db.Text, nullable=True)      # JSON string
    education = db.Column(db.Text, nullable=True)       # JSON string
    certifications = db.Column(db.Text, nullable=True)  # JSON string
    keywords = db.Column(db.Text, nullable=True)        # JSON string
    ocr_confidence = db.Column(db.Float, nullable=True)
    processing_status = db.Column(db.String(50), default="pending")
    error_message = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Resume {self.filename}>"

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "raw_text": self.raw_text,
            "processed_text": self.processed_text,
            "candidate_name": self.candidate_name,
            "email": self.email,
            "phone": self.phone,
            "skills": json.loads(self.skills) if self.skills else [],
            "experience": json.loads(self.experience) if self.experience else [],
            "education": json.loads(self.education) if self.education else [],
            "certifications": json.loads(self.certifications) if self.certifications else [],
            "keywords": json.loads(self.keywords) if self.keywords else [],
            "ocr_confidence": self.ocr_confidence,
            "processing_status": self.processing_status,
            "error_message": self.error_message,
            "uploaded_at": self.uploaded_at,
            "processed_at": self.processed_at,
        }

