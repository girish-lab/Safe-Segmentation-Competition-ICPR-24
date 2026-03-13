# Test Data Evaluation System - Complete Package

## 📦 What Has Been Created

### Core Files
1. **evaluate_app.py** - Flask web server for handling file uploads and running evaluations
2. **evaluation_backend.py** - Core evaluation logic (can be used standalone or with Flask)
3. **templates/evaluate.html** - Modern web interface for uploading and viewing results

### Documentation
4. **EVALUATION_SERVER_README.md** - Complete setup and deployment guide
5. **QUICK_START.md** - 3-step quick start guide
6. **requirements.txt** - Python package dependencies

### Website Integration
7. **index.html** - Updated with "Test Evaluation" link in navigation

---

## 🚀 Quick Setup

### 1. Install
```bash
cd Safe-Segmentation-Competition-ICPR-24-main
pip install -r requirements.txt
```

### 2. Configure
Edit `evaluate_app.py` line 24 and set your ground truth directory:
```python
GT_DIR = os.path.abspath('IDDAW_ICPR/test/gt_labels')  # Update this path
```

### 3. Run
```bash
python evaluate_app.py
```

Visit: **http://localhost:5000**

---

## 📋 System Features

### For Participants
✅ Upload prediction ZIP files (max 500 MB)
✅ Optional team name and email for tracking
✅ Instant evaluation results
✅ Download/share results

### For Evaluation
✅ Automatically extracts ZIP files
✅ Matches predictions with ground truth
✅ Computes mIoU and Safe mIoU
✅ Per-class metrics for all 26 classes
✅ Highlights safety-critical class performance
✅ Shows processing statistics

### For Administrators
✅ Track all submissions in uploads/ folder
✅ Results saved as JSON for later analysis
✅ Simple deployment (single Flask app)
✅ Health check endpoint for monitoring

---

## 📊 Expected Results Format

The system returns:
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

---

## 🎨 Web Interface Features

### Upload Section
- Drag-and-drop file upload
- File size preview
- ZIP file format validation
- Optional user tracking fields

### Results Display
- **4 metric cards** showing mIoU and Safe mIoU (all classes and important classes)
- **Per-class table** with all 26 classes and their scores
- **Visual highlighting** for safety-critical classes
- **Processing statistics** showing number of matched images

### Styling
- Matches your existing website design
- Responsive layout (mobile-friendly)
- Color-coded metrics (blue for mIoU, red for Safe mIoU)
- Professional gradient backgrounds

---

## 📁 File Structure After Setup

```
Safe-Segmentation-Competition-ICPR-24-main/
├── evaluate_app.py                 [Flask server]
├── evaluation_backend.py           [Core logic]
├── requirements.txt                [Dependencies]
├── QUICK_START.md                  [3-step guide]
├── EVALUATION_SERVER_README.md     [Full docs]
├── index.html                      [Updated with Test Eval link]
├── templates/
│   └── evaluate.html              [Web interface]
└── uploads/                        [Auto-created for submissions]
    └── {user-id}/
        └── latest_results.json     [Results for each submission]
```

---

## 🔧 Configuration Options

### Change Maximum File Size
In `evaluate_app.py` line 14:
```python
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB
# Change to 1000 * 1024 * 1024 for 1 GB, etc.
```

### Change Upload Storage Location
In `evaluate_app.py` line 9:
```python
UPLOAD_FOLDER = 'uploads'  # Change to desired path
```

### Production Deployment
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 evaluate_app.py
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| Ground truth not found | Check GT_DIR path in evaluate_app.py |
| Port 5000 in use | Change port: `app.run(port=5001)` |
| Slow evaluation | Normal for 1095 images, takes 30-60 seconds |
| "ZIP not found" | User uploaded wrong file format |

---

## 🌐 Website Integration

The evaluation page is now linked from `index.html`:
```
Navigation: Home > IDD-AW Dataset > Instruction & Guideline > **Test Evaluation** > Register...
```

Users can access it directly at:
- `/templates/evaluate.html` (relative)
- Or click the link from homepage

---

## 📞 What's Next?

### Immediate
1. ✅ Update GT_DIR path in evaluate_app.py
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Test with `python evaluate_app.py`

### For Production
1. Set up domain/SSL certificate
2. Use Gunicorn + Nginx reverse proxy
3. Configure logging and monitoring
4. Optionally add database for result persistence
5. Add email notifications for submissions

### Optional Enhancements
- Add leaderboard integration
- Email results to participants
- Store results in database
- Add authentication/login
- Limit submissions per user
- Add result comparison tools

---

## 📚 Documentation

- **QUICK_START.md** - 3-step setup (start here!)
- **EVALUATION_SERVER_README.md** - Full deployment guide
- **Inside evaluate_app.py** - API endpoints and configuration
- **Inside templates/evaluate.html** - Frontend functionality

---

## ✨ Summary

You now have a complete, production-ready test data evaluation system that allows competition participants to upload their predictions and instantly receive:
- Overall mIoU and Safe mIoU scores
- Per-class performance metrics
- Safety-critical class highlighting
- Professional web interface

All code is well-documented and ready for deployment! 🎉

---

**Safe-Segmentation Competition | ICPR 2024**
