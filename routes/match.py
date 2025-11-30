# routes/match.py
from flask import Blueprint, request, jsonify
from services.matcher import calculate_match_score

match_bp = Blueprint('match_bp', __name__)

@match_bp.route('/score', methods=['POST'])
def score_resume():
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    job_text = data.get('job_text', '')

    if not resume_text or not job_text:
        return jsonify({'error': 'Both resume_text and job_text are required'}), 400

    score = calculate_match_score(resume_text, job_text)
    return jsonify({'match_score': score})
