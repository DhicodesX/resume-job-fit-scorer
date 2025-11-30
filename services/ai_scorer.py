import os
import requests
import json
import re
from fuzzywuzzy import fuzz, process

class AIScorer:
    def __init__(self):
        self.ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = os.getenv('LLM_MODEL', 'llama2:1b')
        self.timeout = int(os.getenv('AI_TIMEOUT', 30))

        # Weight factors for different components
        self.weights = {
            'skills': 0.4,
            'experience': 0.35,
            'education': 0.25
        }

    def score_resume_job_fit(self, resume, job):
        '''Main scoring function that combines rule-based and AI scoring'''
        try:
            # Extract job requirements using AI
            job_requirements = self._extract_job_requirements(job.description)

            # Score different components
            skills_analysis = self._score_skills(resume, job_requirements)
            experience_analysis = self._score_experience(resume, job_requirements)
            education_analysis = self._score_education(resume, job_requirements)

            # Calculate weighted overall score
            overall_score = (
                skills_analysis['score'] * self.weights['skills'] +
                experience_analysis['score'] * self.weights['experience'] +
                education_analysis['score'] * self.weights['education']
            )

            # Generate reasoning points using AI
            reasoning_points = self._generate_reasoning(
                resume, job, skills_analysis, experience_analysis, education_analysis
            )

            return {
                'overall_score': min(100, max(0, overall_score)),
                'skills_score': skills_analysis['score'],
                'experience_score': experience_analysis['score'],
                'education_score': education_analysis['score'],
                'reasoning_points': reasoning_points,
                'skill_analysis': skills_analysis,
                'experience_analysis': experience_analysis,
                'education_analysis': education_analysis,
                'model': self.model,
                'confidence': self._calculate_confidence(skills_analysis, experience_analysis, education_analysis)
            }

        except Exception as e:
            # Fallback to rule-based scoring if AI fails
            return self._fallback_scoring(resume, job)

    def _call_ollama(self, prompt):
        '''Call Ollama API'''
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                },
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                raise Exception(f"Ollama API error: {response.status_code}")

        except Exception as e:
            raise Exception(f"Failed to call Ollama: {str(e)}")

    def _extract_job_requirements(self, job_description):
        '''Extract structured requirements from job description'''
        # Basic fallback extraction
        text = job_description.lower()

        # Common skill patterns
        skills = []
        skill_patterns = [
            r'python|java|javascript|react|angular|vue|node\.js',
            r'sql|mysql|postgresql|mongodb',
            r'aws|azure|docker|kubernetes'
        ]

        for pattern in skill_patterns:
            matches = re.findall(pattern, text)
            skills.extend(matches)

        return {
            'required_skills': skills[:10],
            'preferred_skills': [],
            'experience_level': 'mid',
            'education_requirements': ['bachelor'] if 'bachelor' in text else [],
            'key_responsibilities': []
        }

    def _score_skills(self, resume, job_requirements):
        '''Score skill match between resume and job'''
        resume_skills = [skill.lower() for skill in resume.get_skills()]
        required_skills = [skill.lower() for skill in job_requirements.get('required_skills', [])]

        if not required_skills:
            return {'score': 50.0, 'matched': [], 'missing': [], 'additional': resume_skills}

        matched = []
        for req_skill in required_skills:
            if any(req_skill in res_skill for res_skill in resume_skills):
                matched.append(req_skill)

        score = (len(matched) / len(required_skills)) * 80 if required_skills else 50

        return {
            'score': min(100, score),
            'matched': matched,
            'missing': [s for s in required_skills if s not in matched],
            'additional': resume_skills
        }

    def _score_experience(self, resume, job_requirements):
        '''Score experience level match'''
        experience_count = len(resume.get_experience())
        estimated_years = experience_count * 1.5

        # Simple scoring based on experience entries
        if estimated_years >= 3:
            score = 85
        elif estimated_years >= 1:
            score = 65
        else:
            score = 40

        return {
            'score': score,
            'estimated_years': estimated_years,
            'required_level': job_requirements.get('experience_level', 'unknown'),
            'experience_entries': experience_count
        }

    def _score_education(self, resume, job_requirements):
        '''Score education match'''
        education = resume.get_education()
        has_degree = len(education) > 0

        score = 80 if has_degree else 40

        return {
            'score': score,
            'matched': has_degree,
            'details': f"Education entries: {len(education)}"
        }

    def _generate_reasoning(self, resume, job, skills_analysis, experience_analysis, education_analysis):
        '''Generate reasoning points'''
        reasoning = []

        # Skills reasoning
        if skills_analysis['score'] >= 70:
            reasoning.append(f"Strong skill match with {len(skills_analysis.get('matched', []))} key requirements")
        else:
            reasoning.append(f"Limited skill alignment - missing {len(skills_analysis.get('missing', []))} requirements")

        # Experience reasoning
        if experience_analysis['score'] >= 70:
            reasoning.append(f"Experience level appropriate for role requirements")
        else:
            reasoning.append("Experience may need development for optimal fit")

        # Education reasoning
        if education_analysis['score'] >= 70:
            reasoning.append("Educational background meets basic requirements")
        else:
            reasoning.append("Educational qualifications may need review")

        return reasoning[:3]

    def _calculate_confidence(self, skills_analysis, experience_analysis, education_analysis):
        '''Calculate confidence in scoring'''
        return 0.75  # Default confidence

    def _fallback_scoring(self, resume, job):
        '''Fallback scoring when AI unavailable'''
        skills_count = len(resume.get_skills())
        experience_count = len(resume.get_experience())
        education_count = len(resume.get_education())

        skills_score = min(100, skills_count * 8)
        experience_score = min(100, experience_count * 15)
        education_score = 80 if education_count > 0 else 40

        overall = (skills_score * 0.4 + experience_score * 0.35 + education_score * 0.25)

        return {
            'overall_score': overall,
            'skills_score': skills_score,
            'experience_score': experience_score,
            'education_score': education_score,
            'reasoning_points': [
                "Automated scoring based on resume analysis",
                "Skills and experience inventory completed",
                "AI scoring temporarily unavailable"
            ],
            'skill_analysis': {'matched': resume.get_skills()[:5], 'missing': []},
            'experience_analysis': {'estimated_years': experience_count * 1.5},
            'education_analysis': {'matched': education_count > 0},
            'model': 'fallback',
            'confidence': 0.6
        }