"""
Flask app for Safe-Segmentation Test Data Evaluation.
Allows users to upload prediction ZIP files and get evaluation results.
Supports local, Google Drive, and OneDrive ground truth storage.
"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import zipfile
import os
import shutil
from pathlib import Path
import tempfile
import json
import logging
from evaluation_backend import evaluate_predictions
from cloud_storage import GroundTruthStorage, STORAGE_LOCAL, STORAGE_GOOGLE_DRIVE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ============================================================================
# CONFIGURATION - MODIFY THESE SETTINGS
# ============================================================================

# Storage Configuration
STORAGE_CONFIG = {
    'type': STORAGE_LOCAL,  # Options: STORAGE_LOCAL, STORAGE_GOOGLE_DRIVE, 'onedrive'
    
    # For LOCAL storage:
    'path': os.path.abspath('IDDAW_ICPR/test/gt_labels'),
    
    # For GOOGLE DRIVE storage (uncomment and set):
    # 'type': STORAGE_GOOGLE_DRIVE,
    # 'folder_id': 'YOUR_GOOGLE_DRIVE_FOLDER_ID',  # Extract from share link
    
    # For ONEDRIVE storage (uncomment and set):
    # 'type': 'onedrive',
    # 'share_url': 'https://..../download?resid=...',
}

# Other Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB max file size
ENABLE_CACHE = True  # Cache downloaded ground truth for subsequent runs

# ============================================================================
# END CONFIGURATION
# ============================================================================

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Initialize storage backend
storage = GroundTruthStorage(
    storage_type=STORAGE_CONFIG['type'],
    cache_enabled=ENABLE_CACHE
)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_ground_truth_dir():
    """
    Get ground truth directory.
    If using cloud storage, downloads and/or caches the data.
    """
    gt_dir, error = storage.get_ground_truth_dir(STORAGE_CONFIG)
    
    if error:
        logger.error(f"Ground truth error: {error}")
        return None
    
    if not os.path.exists(gt_dir):
        logger.error(f"Ground truth directory not found: {gt_dir}")
        return None
    
    logger.info(f"Using ground truth from: {gt_dir}")
    return gt_dir


def extract_and_validate_zip(zip_path):
    """Extract and validate ZIP file structure."""
    try:
        extract_dir = tempfile.mkdtemp()
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find PNG files in the extracted directory
        from pathlib import Path
        png_files = list(Path(extract_dir).glob('**/*.png'))
        
        if not png_files:
            shutil.rmtree(extract_dir)
            return None, "No PNG files found in ZIP archive"
        
        return extract_dir, None
        
    except zipfile.BadZipFile:
        return None, "Invalid ZIP file format"
    except Exception as e:
        return None, str(e)


@app.route('/')
def index():
    return render_template('evaluate.html')


@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """Accept prediction ZIP file and run evaluation."""
    
    # Get ground truth directory (may download from cloud)
    gt_dir = get_ground_truth_dir()
    if not gt_dir:
        return jsonify({
            'status': 'error',
            'message': 'Ground truth directory is not available. Please check server configuration.'
        }), 500
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file provided'
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'No file selected'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': 'File must be a ZIP archive (.zip)'
        }), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    user_id = request.form.get('user_id', 'anonymous')
    user_name = request.form.get('user_name', 'Anonymous')
    
    # Create user-specific folder
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_id))
    os.makedirs(user_folder, exist_ok=True)
    
    zip_path = os.path.join(user_folder, filename)
    file.save(zip_path)
    
    try:
        # Extract ZIP file
        extract_dir, error = extract_and_validate_zip(zip_path)
        if error:
            return jsonify({
                'status': 'error',
                'message': error
            }), 400
        
        # Run evaluation
        results = evaluate_predictions(gt_dir, extract_dir)
        
        # Clean up
        shutil.rmtree(extract_dir, ignore_errors=True)
        
        # Add metadata to results
        results['user_name'] = user_name
        results['user_id'] = user_id
        
        # Save results to file for record keeping
        results_file = os.path.join(user_folder, 'latest_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Evaluation error: {str(e)}'
        }), 500
    
    finally:
        # Clean up the uploaded ZIP file
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    gt_dir = get_ground_truth_dir()
    gt_exists = gt_dir is not None and os.path.exists(gt_dir)
    
    cache_size = storage.cache_size() if ENABLE_CACHE else "N/A"
    
    return jsonify({
        'status': 'ok' if gt_exists else 'error',
        'gt_directory_exists': gt_exists,
        'gt_path': gt_dir or 'unavailable',
        'storage_type': STORAGE_CONFIG['type'],
        'cache_size': cache_size,
        'cache_enabled': ENABLE_CACHE
    }), 200


@app.route('/api/cache/info', methods=['GET'])
def cache_info():
    """Get cache information."""
    if not ENABLE_CACHE:
        return jsonify({
            'cache_enabled': False,
            'message': 'Cache is disabled'
        }), 200
    
    cache_size = storage.cache_size()
    
    return jsonify({
        'cache_enabled': True,
        'cache_size': cache_size,
        'cache_directory': str(storage.cache_dir)
    }), 200


@app.route('/api/cache/clear', methods=['POST'])
def cache_clear():
    """Clear cache (admin endpoint)."""
    try:
        storage.clear_cache()
        return jsonify({
            'status': 'success',
            'message': 'Cache cleared successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'status': 'error',
        'message': 'File too large. Maximum size is 500 MB.'
    }), 413


if __name__ == '__main__':
    # Development server
    # For production, use a production WSGI server like gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
