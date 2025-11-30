from extensions import db
from datetime import datetime
import json

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)

    # Parsed job requirements
    required_skills = db.Column(db.Text)  # JSON array
    preferred_skills = db.Column(db.Text)  # JSON array
    experience_level = db.Column(db.String(50))  # entry, mid, senior, executive
    education_requirements = db.Column(db.Text)  # JSON array
    location = db.Column(db.String(255))
    remote_ok = db.Column(db.Boolean, default=False)

    # Job metadata
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    job_type = db.Column(db.String(50))  # full-time, part-time, contract, internship

    # Processing info
    keywords = db.Column(db.Text)  # JSON array - extracted keywords
    processed = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scoring_results = db.relationship('ScoringResult', backref='job', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(Job, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'required_skills': json.loads(self.required_skills) if self.required_skills else [],
            'preferred_skills': json.loads(self.preferred_skills) if self.preferred_skills else [],
            'experience_level': self.experience_level,
            'education_requirements': json.loads(self.education_requirements) if self.education_requirements else [],
            'location': self.location,
            'remote_ok': self.remote_ok,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'job_type': self.job_type,
            'keywords': json.loads(self.keywords) if self.keywords else [],
            'processed': self.processed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def set_required_skills(self, skills_list):
        self.required_skills = json.dumps(skills_list) if skills_list else None

    def get_required_skills(self):
        return json.loads(self.required_skills) if self.required_skills else []

    def set_preferred_skills(self, skills_list):
        self.preferred_skills = json.dumps(skills_list) if skills_list else None

    def get_preferred_skills(self):
        return json.loads(self.preferred_skills) if self.preferred_skills else []

    def set_education_requirements(self, edu_list):
        self.education_requirements = json.dumps(edu_list) if edu_list else None

    def get_education_requirements(self):
        return json.loads(self.education_requirements) if self.education_requirements else []

    def set_keywords(self, keywords_list):
        self.keywords = json.dumps(keywords_list) if keywords_list else None

    def get_keywords(self):
        return json.loads(self.keywords) if self.keywords else []

    def mark_processed(self):
        self.processed = True
        self.updated_at = datetime.utcnow()
        db.session.commit()