# routes/job_upload.py
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

job_bp = Blueprint('job_bp', __name__)

@job_bp.route('/', methods=['POST'])
def upload_job_description():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty file name'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    # Optional: read text from the job description
    with open(save_path, 'r', encoding='utf-8', errors='ignore') as f:
        job_text = f.read()

    return jsonify({
        'message': 'Job description uploaded successfully ✅',
        'file_name': filename,
        'file_path': save_path,
        'job_text_preview': job_text[:500]  # Return first 500 chars as preview
    })
