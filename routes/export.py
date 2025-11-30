from flask import Blueprint, request, jsonify, send_file, current_app
import os
import csv
from datetime import datetime
from extensions import db
from models.scoring import ScoringResult

export_bp = Blueprint('export', __name__)

@export_bp.route('/csv', methods=['POST'])
def export_csv():
    '''Export scoring results to CSV'''
    try:
        data = request.get_json()
        result_ids = data.get('result_ids', [])
        batch_id = data.get('batch_id')
        job_id = data.get('job_id')

        # Build query
        query = ScoringResult.query

        if result_ids:
            query = query.filter(ScoringResult.id.in_(result_ids))
        elif batch_id:
            query = query.filter_by(batch_id=batch_id)
        elif job_id:
            query = query.filter_by(job_id=job_id)
        else:
            return jsonify({'error': 'No results specified for export'}), 400

        results = query.order_by(ScoringResult.overall_score.desc()).all()

        if not results:
            return jsonify({'error': 'No results found'}), 404

        # Generate CSV filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'resume_scores_{timestamp}.csv'
        filepath = os.path.join(current_app.config['EXPORT_FOLDER'], filename)

        # Write CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Rank', 'Candidate Name', 'Resume File', 'Overall Score', 
                'Skills Score', 'Experience Score', 'Education Score',
                'Top Reason 1', 'Top Reason 2', 'Top Reason 3',
                'Email', 'Phone', 'Job Title', 'Scored At'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, result in enumerate(results, 1):
                reasoning = result.get_reasoning_points()
                writer.writerow({
                    'Rank': i,
                    'Candidate Name': result.resume.candidate_name or 'N/A',
                    'Resume File': result.resume.original_filename,
                    'Overall Score': f"{result.overall_score:.1f}",
                    'Skills Score': f"{result.skills_score:.1f}",
                    'Experience Score': f"{result.experience_score:.1f}",
                    'Education Score': f"{result.education_score:.1f}",
                    'Top Reason 1': reasoning[0] if len(reasoning) > 0 else '',
                    'Top Reason 2': reasoning[1] if len(reasoning) > 1 else '',
                    'Top Reason 3': reasoning[2] if len(reasoning) > 2 else '',
                    'Email': result.resume.email or '',
                    'Phone': result.resume.phone or '',
                    'Job Title': result.job.title,
                    'Scored At': result.scored_at.strftime('%Y-%m-%d %H:%M:%S')
                })

        return jsonify({
            'filename': filename,
            'record_count': len(results),
            'message': 'CSV export completed successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': f'CSV export failed: {str(e)}'}), 500

@export_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    '''Download exported file'''
    try:
        filepath = os.path.join(current_app.config['EXPORT_FOLDER'], filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500