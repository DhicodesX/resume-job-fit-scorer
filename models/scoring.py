from extensions import db
from datetime import datetime
import json

class ScoringResult(db.Model):
    __tablename__ = 'scoring_results'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)

    # Scoring results
    overall_score = db.Column(db.Float, nullable=False)  # 0-100
    skills_score = db.Column(db.Float, default=0.0)      # 0-100
    experience_score = db.Column(db.Float, default=0.0)  # 0-100
    education_score = db.Column(db.Float, default=0.0)   # 0-100

    # Top reasoning points (JSON array of strings)
    reasoning_points = db.Column(db.Text)  # JSON array - top 3 reasons

    # Detailed analysis (JSON objects)
    skill_matches = db.Column(db.Text)     # JSON - matched vs missing skills
    experience_analysis = db.Column(db.Text) # JSON - experience breakdown
    education_analysis = db.Column(db.Text)  # JSON - education match

    # Processing metadata
    ai_model_used = db.Column(db.String(100))
    processing_time = db.Column(db.Float)  # seconds
    confidence = db.Column(db.Float, default=0.0)  # AI confidence in scoring

    # Batch processing info
    batch_id = db.Column(db.String(100))  # For batch processing tracking

    # Timestamps
    scored_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(ScoringResult, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'job_id': self.job_id,
            'overall_score': round(self.overall_score, 2),
            'skills_score': round(self.skills_score, 2),
            'experience_score': round(self.experience_score, 2),
            'education_score': round(self.education_score, 2),
            'reasoning_points': json.loads(self.reasoning_points) if self.reasoning_points else [],
            'skill_matches': json.loads(self.skill_matches) if self.skill_matches else {},
            'experience_analysis': json.loads(self.experience_analysis) if self.experience_analysis else {},
            'education_analysis': json.loads(self.education_analysis) if self.education_analysis else {},
            'ai_model_used': self.ai_model_used,
            'processing_time': round(self.processing_time, 3) if self.processing_time else None,
            'confidence': round(self.confidence, 3) if self.confidence else None,
            'batch_id': self.batch_id,
            'scored_at': self.scored_at.isoformat() if self.scored_at else None
        }

    def set_reasoning_points(self, points_list):
        # Ensure only top 3 points
        top_points = points_list[:3] if points_list else []
        self.reasoning_points = json.dumps(top_points)

    def get_reasoning_points(self):
        return json.loads(self.reasoning_points) if self.reasoning_points else []

    def set_skill_matches(self, matches_dict):
        self.skill_matches = json.dumps(matches_dict) if matches_dict else None

    def get_skill_matches(self):
        return json.loads(self.skill_matches) if self.skill_matches else {}

    def set_experience_analysis(self, analysis_dict):
        self.experience_analysis = json.dumps(analysis_dict) if analysis_dict else None

    def get_experience_analysis(self):
        return json.loads(self.experience_analysis) if self.experience_analysis else {}

    def set_education_analysis(self, analysis_dict):
        self.education_analysis = json.dumps(analysis_dict) if analysis_dict else None

    def get_education_analysis(self):
        return json.loads(self.education_analysis) if self.education_analysis else {}

    def get_score_category(self):
        '''Return score category for easy filtering'''
        if self.overall_score >= 80:
            return 'excellent'
        elif self.overall_score >= 60:
            return 'good'
        elif self.overall_score >= 40:
            return 'fair'
        else:
            return 'poor'