# Quick Start Guide: Test Data Evaluation Server

## In 3 Steps

### Step 1: Install Dependencies
```bash
cd Safe-Segmentation-Competition-ICPR-24-main
pip install -r requirements.txt
```

### Step 2: Update Ground Truth Path
Edit `evaluate_app.py` line 24:
```python
GT_DIR = os.path.abspath('IDDAW_ICPR/test/gt_labels')
```
Replace with your actual ground truth directory path.

### Step 3: Start the Server
```bash
python evaluate_app.py
```

Then open: **http://localhost:5000**

## What You Get

✅ **Web Interface** - Clean, intuitive UI for uploading predictions
✅ **Instant Results** - mIoU and Safe mIoU scores computed in real-time
✅ **Per-Class Metrics** - Detailed performance for all 26 classes
✅ **Safety Metrics** - Special highlighting for safety-critical classes
✅ **Result History** - All evaluations saved to `uploads/` folder

## File Format Expected

Users should upload a ZIP file containing PNG predictions:

```
predictions.zip
├── 0001_labellevel3Ids.png (or 0001_pred.png)
├── 0002_labellevel3Ids.png
└── ... (all 1095 test images)
```

**Image Requirements:**
- PNG format
- Same dimensions as ground truth
- Pixel values = class IDs (0-25)

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **mIoU** | Standard mean Intersection over Union across all 26 classes |
| **Safe mIoU** | Safety-aware version penalizing misclassifications of critical objects (person, car, etc.) |
| **Important Classes** | person, rider, motorcycle, bicycle, autorickshaw, car, truck, bus |

## API Usage (for Advanced Users)

```bash
# Submit predictions
curl -X POST http://localhost:5000/api/evaluate \
  -F "file=@predictions.zip" \
  -F "user_name=MyTeam" \
  -F "user_id=myteam@email.com"

# Health check
curl http://localhost:5000/api/health
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "Ground truth not found" | Check GT_DIR path in evaluate_app.py |
| "Connection refused" | Make sure Flask server is running |
| "File too large" | Increase MAX_CONTENT_LENGTH in evaluate_app.py |

## File Structure

```
Safe-Segmentation-Competition-ICPR-24-main/
├── evaluate_app.py                 ← Flask server (main)
├── evaluation_backend.py           ← Core evaluation logic
├── requirements.txt                ← Dependencies
├── templates/
│   └── evaluate.html              ← Web interface
├── EVALUATION_SERVER_README.md     ← Full documentation
└── QUICK_START.md                 ← This file
```

## Next Steps

1. **For Local Testing:** Run `python evaluate_app.py` and open http://localhost:5000
2. **For Production:** Use Gunicorn or similar WSGI server
3. **For Integration:** Update index.html navigation to link to evaluation page
4. **For Customization:** Edit evaluate.html to match your website styling

## Questions?

See `EVALUATION_SERVER_README.md` for detailed documentation and deployment guides.

---
**Safe-Segmentation Competition | ICPR 2024**
