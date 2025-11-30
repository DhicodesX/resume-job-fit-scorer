import json
from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from models.resume import Resume
from extensions import db
from services.document_processor import process_document

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Process the document
    extracted_data = process_document(file_path)

    # Store in database
    new_resume = Resume(
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        raw_text=extracted_data.get('raw_text'),
        processed_text=extracted_data.get('processed_text'),
        candidate_name=extracted_data.get('candidate_name'),
        email=extracted_data.get('email'),
        phone=extracted_data.get('phone'),
        skills=json.dumps(extracted_data.get('skills')),
        experience=json.dumps(extracted_data.get('experience')),
        education=json.dumps(extracted_data.get('education')),
        certifications=json.dumps(extracted_data.get('certifications')),
        keywords=json.dumps(extracted_data.get('keywords')),
        ocr_confidence=extracted_data.get('ocr_confidence'),
        processing_status='processed'
    )

    db.session.add(new_resume)
    db.session.commit()

    return jsonify({
        'message': 'Resume uploaded and processed successfully!',
        'data': new_resume.to_dict()
    })
