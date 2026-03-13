# Test Data Evaluation Server

A web application for evaluating semantic segmentation predictions on the IDDAW test set. Users can upload their predictions in a ZIP file and receive mIoU and Safe mIoU scores.

## ✨ Features

- 🚀 Easy-to-use web interface
- ☁️ **NEW:** Cloud storage support (Google Drive, OneDrive, Local)
- 📊 Real-time evaluation results
- 🎯 Per-class performance metrics
- 🛡️ Safety-critical class highlighting
- 📈 Support for Safe mIoU metric
- 💾 Result archival and tracking
- 🔄 Automatic intelligent caching

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Ground Truth Storage

The system supports three storage options:

**Option A: Local Storage (Default)**
```python
# In evaluate_app.py
STORAGE_CONFIG = {
    'type': STORAGE_LOCAL,
    'path': os.path.abspath('IDDAW_ICPR/test/gt_labels'),
}
```

**Option B: Google Drive (Recommended for Cloud)**
```python
from cloud_storage import STORAGE_GOOGLE_DRIVE

STORAGE_CONFIG = {
    'type': STORAGE_GOOGLE_DRIVE,
    'folder_id': 'YOUR_GOOGLE_DRIVE_FOLDER_ID',
}
```

**Option C: OneDrive**
```python
STORAGE_CONFIG = {
    'type': 'onedrive',
    'share_url': 'https://onedrive.live.com/?resid=...',
}
```

See [CLOUD_STORAGE_CONFIG.md](CLOUD_STORAGE_CONFIG.md) for detailed setup instructions.

### 3. Run the Server

**Development Mode:**
```bash
python evaluate_app.py
```

The server will start at `http://localhost:5000`

**Production Mode (using Gunicorn):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 evaluate_app.py
```

### 4. Access the Web Interface

Navigate to:
- Local: `http://localhost:5000`
- Remote: `http://<server-ip>:5000`

## File Structure

```
├── evaluate_app.py              # Flask application
├── evaluation_backend.py        # Core evaluation logic
├── requirements.txt             # Python dependencies
├── templates/
│   └── evaluate.html           # Web interface template
└── uploads/                    # Uploaded files storage (auto-created)
```

## Usage

### For Participants

1. Navigate to the Test Evaluation page
2. (Optional) Enter your team name and email
3. Select your predictions ZIP file
4. Click "Evaluate Predictions"
5. View your results instantly

### ZIP File Format

```
predictions.zip
├── 0001_pred.png
├── 0002_pred.png
├── ...
└── 1095_pred.png
```

**Requirements:**
- All files must be PNG format
- Image dimensions must match ground truth
- Pixel values should be class IDs (0-25)
- Filenames should match ground truth naming or use `*_pred.png` pattern

## API Endpoints

### POST `/api/evaluate`
Submit predictions for evaluation.

**Parameters:**
- `file` (required): ZIP file containing predictions
- `user_name` (optional): Team or participant name
- `user_id` (optional): Unique identifier (email, etc.)

**Response:**
```json
{
  "status": "success",
  "processed_images": 1095,
  "skipped_images": 0,
  "overall_miou": 65.43,
  "overall_safe_miou": 58.21,
  "important_miou": 72.15,
  "important_safe_miou": 68.42,
  "class_results": [
    {
      "class_id": 0,
      "class_name": "road",
      "miou": 87.65,
      "safe_miou": 82.34,
      "is_important": false
    },
    ...
  ]
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "gt_directory_exists": true,
  "gt_path": "/path/to/IDDAW_ICPR/test/gt_labels",
  "storage_type": "gdrive",
  "cache_size": "2.45 GB",
  "cache_enabled": true
}
```

### GET `/api/cache/info`
Get information about the ground truth cache.

**Response:**
```json
{
  "cache_enabled": true,
  "cache_size": "2.45 GB",
  "cache_directory": ".gt_cache"
}
```

### POST `/api/cache/clear`
Clear the ground truth cache (admin endpoint).

**Response:**
```json
{
  "status": "success",
  "message": "Cache cleared successfully"
}
```

## Configuration

### Ground Truth Storage
Choose one of three storage options:

**Option 1: Local Storage** (Default)
```python
STORAGE_CONFIG = {
    'type': STORAGE_LOCAL,
    'path': os.path.abspath('IDDAW_ICPR/test/gt_labels'),
}
```

**Option 2: Google Drive** (Recommended for cloud deployment)
```python
from cloud_storage import STORAGE_GOOGLE_DRIVE

STORAGE_CONFIG = {
    'type': STORAGE_GOOGLE_DRIVE,
    'folder_id': 'YOUR_GOOGLE_DRIVE_FOLDER_ID',
}
```

**Option 3: OneDrive**
```python
STORAGE_CONFIG = {
    'type': 'onedrive',
    'share_url': 'https://onedrive.live.com/?resid=...',
}
```

See [CLOUD_STORAGE_CONFIG.md](CLOUD_STORAGE_CONFIG.md) for detailed setup.

### Maximum Upload Size
Edit `evaluate_app.py`:
```python
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # Change 500 to desired MB
```

### Cache Settings
```python
ENABLE_CACHE = True  # Cache downloaded ground truth (recommended)
```

### Upload Storage Location
```python
UPLOAD_FOLDER = 'uploads'  # Change to desired path
```

## Evaluation Metrics

### mIoU (mean Intersection over Union)
Standard metric computed across all 26 classes.

### Safe mIoU
Safety-aware metric that penalizes misclassifications of safety-critical classes:
- **Safety-Critical Classes:** person, rider, motorcycle, bicycle, autorickshaw, car, truck, bus
- **Penalty Levels:**
  - N1 neighbors (most similar): 1/3 penalty
  - N2 neighbors (related): 2/3 penalty
  - N3 neighbors (distant): 3/3 penalty

## Troubleshooting

### "Ground truth directory not found"
- Verify `GT_DIR` path in `evaluate_app.py`
- Ensure the path exists on your server

### "No PNG files found in ZIP"
- Check ZIP file structure
- Ensure PNG files are in root or single subdirectory
- Verify file extensions are lowercase `.png`

### File too large error
- Increase `MAX_CONTENT_LENGTH` in `evaluate_app.py`
- Compress predictions or split into multiple submissions

### Slow evaluation
- Evaluation time depends on:
  - Number of images (1095 test images)
  - Server resources
  - Typical time: 30-60 seconds

## Integration with Website

To add the evaluation link to your main website:

1. Update `index.html` navigation:
```html
<a href="templates/evaluate.html">Test Evaluation</a>
```

2. Ensure Flask server is running alongside your static website
3. Update API endpoints if serving from different domain/port

## Security Considerations

1. **File Upload Validation:**
   - Only ZIP files are accepted
   - File size limited to 500 MB
   - Temporary files cleaned after processing

2. **Path Traversal Protection:**
   - All filenames passed through `secure_filename()`
   - ZIP extraction to isolated temp directory

3. **Input Validation:**
   - File type checking
   - ZIP structure validation
   - Image dimension verification

## Performance Notes

- Evaluation of 1095 images typically takes 30-60 seconds
- Temporary files are automatically cleaned up
- Results are saved to `uploads/<user_id>/latest_results.json`

## Production Deployment

For production use:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Add SSL/TLS certificate
3. Set up reverse proxy (Nginx, Apache)
4. Configure proper logging
5. Set up database for result persistence
6. Add authentication if needed

Example Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Contact & Support

For issues or questions about the evaluation server, please contact the competition organizers.

---

**Safe-Segmentation Competition | ICPR 2024**
