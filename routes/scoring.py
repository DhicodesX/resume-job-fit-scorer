from flask import Blueprint, request, jsonify
from app import db
from models.resume import Resume
from models.job import Job
from models.scoring import ScoringResult
from services.ai_scorer import AIScorer
import uuid
import time

scoring_bp = Blueprint('scoring', __name__)

@scoring_bp.route('/score', methods=['POST'])
def score_resume():
    '''Score a single resume against a job description'''
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_description = data.get('job_description')
        job_title = data.get('job_title', 'Untitled Position')

        if not resume_id or not job_description:
            return jsonify({'error': 'resume_id and job_description are required'}), 400

        # Get resume
        resume = Resume.query.get_or_404(resume_id)
        if resume.processing_status != 'completed':
            return jsonify({'error': 'Resume is not fully processed yet'}), 400

        # Create or get job
        job = Job(
            title=job_title,
            description=job_description,
            processed=False
        )
        db.session.add(job)
        db.session.commit()

        # Score the resume
        start_time = time.time()
        scorer = AIScorer()

        scoring_data = scorer.score_resume_job_fit(resume, job)
        processing_time = time.time() - start_time

        # Create scoring result
        result = ScoringResult(
            resume_id=resume.id,
            job_id=job.id,
            overall_score=scoring_data['overall_score'],
            skills_score=scoring_data['skills_score'],
            experience_score=scoring_data['experience_score'],
            education_score=scoring_data['education_score'],
            ai_model_used=scoring_data.get('model', 'unknown'),
            processing_time=processing_time,
            confidence=scoring_data.get('confidence', 0.0)
        )

        # Set structured data
        result.set_reasoning_points(scoring_data['reasoning_points'])
        result.set_skill_matches(scoring_data['skill_analysis'])
        result.set_experience_analysis(scoring_data['experience_analysis'])
        result.set_education_analysis(scoring_data['education_analysis'])

        db.session.add(result)
        db.session.commit()

        return jsonify({
            'scoring_id': result.id,
            'resume_id': resume.id,
            'job_id': job.id,
            'results': result.to_dict(),
            'processing_time': processing_time,
            'message': 'Resume scored successfully'
        }), 201

    except Exception as e:
        return jsonify({'error': f'Scoring failed: {str(e)}'}), 500

@scoring_bp.route('/batch-score', methods=['POST'])
def batch_score():
    '''Score multiple resumes against a job description'''
    try:
        data = request.get_json()
        resume_ids = data.get('resume_ids', [])
        job_description = data.get('job_description')
        job_title = data.get('job_title', 'Untitled Position')

        if not resume_ids or not job_description:
            return jsonify({'error': 'resume_ids and job_description are required'}), 400

        if len(resume_ids) > 25:
            return jsonify({'error': 'Maximum 25 resumes allowed per batch'}), 400

        # Create job
        job = Job(
            title=job_title,
            description=job_description,
            processed=False
        )
        db.session.add(job)
        db.session.commit()

        # Generate batch ID
        batch_id = str(uuid.uuid4())

        # Score all resumes
        scorer = AIScorer()
        results = []
        errors = []

        for resume_id in resume_ids:
            try:
                resume = Resume.query.get(resume_id)
                if not resume:
                    errors.append(f"Resume {resume_id}: Not found")
                    continue

                if resume.processing_status != 'completed':
                    errors.append(f"Resume {resume_id}: Not fully processed")
                    continue

                start_time = time.time()
                scoring_data = scorer.score_resume_job_fit(resume, job)
                processing_time = time.time() - start_time

                # Create scoring result
                result = ScoringResult(
                    resume_id=resume.id,
                    job_id=job.id,
                    overall_score=scoring_data['overall_score'],
                    skills_score=scoring_data['skills_score'],
                    experience_score=scoring_data['experience_score'],
                    education_score=scoring_data['education_score'],
                    ai_model_used=scoring_data.get('model', 'unknown'),
                    processing_time=processing_time,
                    confidence=scoring_data.get('confidence', 0.0),
                    batch_id=batch_id
                )

                # Set structured data
                result.set_reasoning_points(scoring_data['reasoning_points'])
                result.set_skill_matches(scoring_data['skill_analysis'])
                result.set_experience_analysis(scoring_data['experience_analysis'])
                result.set_education_analysis(scoring_data['education_analysis'])

                db.session.add(result)
                results.append(result.to_dict())

            except Exception as e:
                errors.append(f"Resume {resume_id}: {str(e)}")

        db.session.commit()

        # Sort results by score
        results.sort(key=lambda x: x['overall_score'], reverse=True)

        return jsonify({
            'batch_id': batch_id,
            'job_id': job.id,
            'total_processed': len(results),
            'total_errors': len(errors),
            'results': results,
            'errors': errors,
            'message': f'Batch scoring completed. {len(results)}/{len(resume_ids)} resumes scored successfully.'
        }), 201

    except Exception as e:
        return jsonify({'error': f'Batch scoring failed: {str(e)}'}), 500

@scoring_bp.route('/result/<int:result_id>', methods=['GET'])
def get_scoring_result(result_id):
    '''Get detailed scoring result'''
    try:
        result = ScoringResult.query.get_or_404(result_id)

        # Include resume and job info
        response_data = result.to_dict()
        response_data['resume'] = result.resume.to_dict()
        response_data['job'] = result.job.to_dict()

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': f'Failed to fetch result: {str(e)}'}), 500

@scoring_bp.route('/results', methods=['GET'])
def list_scoring_results():
    '''List scoring results with filtering'''
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        batch_id = request.args.get('batch_id')
        job_id = request.args.get('job_id', type=int)
        min_score = request.args.get('min_score', type=float)
        max_score = request.args.get('max_score', type=float)

        query = ScoringResult.query

        if batch_id:
            query = query.filter_by(batch_id=batch_id)
        if job_id:
            query = query.filter_by(job_id=job_id)
        if min_score is not None:
            query = query.filter(ScoringResult.overall_score >= min_score)
        if max_score is not None:
            query = query.filter(ScoringResult.overall_score <= max_score)

        results = query.order_by(ScoringResult.overall_score.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'results': [result.to_dict() for result in results.items],
            'pagination': {
                'page': page,
                'pages': results.pages,
                'per_page': per_page,
                'total': results.total,
                'has_next': results.has_next,
                'has_prev': results.has_prev
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to list results: {str(e)}'}), 500

@scoring_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    '''Get top-scoring resumes for a job or overall'''
    try:
        job_id = request.args.get('job_id', type=int)
        limit = request.args.get('limit', 10, type=int)

        query = ScoringResult.query

        if job_id:
            query = query.filter_by(job_id=job_id)

        top_results = query.order_by(ScoringResult.overall_score.desc()).limit(limit).all()

        leaderboard = []
        for i, result in enumerate(top_results, 1):
            entry = result.to_dict()
            entry['rank'] = i
            entry['resume_name'] = result.resume.candidate_name or result.resume.original_filename
            entry['job_title'] = result.job.title
            leaderboard.append(entry)

        return jsonify({
            'leaderboard': leaderboard,
            'total_entries': len(leaderboard)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to generate leaderboard: {str(e)}'}), 500