# ☁️ Cloud-Enabled Evaluation Server - Complete Setup

Your Safe-Segmentation evaluation system now supports cloud storage! Here's what's been added.

## 📦 New Files Created

1. **cloud_storage.py** - Cloud storage backend (Google Drive, OneDrive, Local)
2. **CLOUD_STORAGE_CONFIG.md** - Detailed cloud configuration guide
3. **CLOUD_CONFIG_EXAMPLES.py** - Ready-to-use configuration examples

## ✨ Updated Files

- **evaluate_app.py** - Now supports cloud storage + new API endpoints
- **requirements.txt** - Added: gdown, requests, tqdm
- **EVALUATION_SERVER_README.md** - Updated with cloud options

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Choose Your Storage

**For Local Storage** (No configuration needed):
```python
# evaluate_app.py already defaults to this
STORAGE_CONFIG = {
    'type': STORAGE_LOCAL,
    'path': os.path.abspath('IDDAW_ICPR/test/gt_labels'),
}
```

**For Google Drive** (Recommended for online servers):
```python
# In evaluate_app.py, replace STORAGE_CONFIG with:
from cloud_storage import STORAGE_GOOGLE_DRIVE

STORAGE_CONFIG = {
    'type': STORAGE_GOOGLE_DRIVE,
    'folder_id': '1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9',  # Your folder ID
}
```

**For OneDrive**:
```python
STORAGE_CONFIG = {
    'type': 'onedrive',
    'share_url': 'https://onedrive.live.com/?resid=...&download=1',
}
```

### Step 3: Run Server
```bash
python evaluate_app.py
```

Visit: **http://localhost:5000**

---

## 🌐 Which Storage Should You Use?

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| **Local server with disk space** | Local Storage | Fastest, no setup |
| **Cloud server (AWS, Azure, GCP)** | Google Drive | Free, automatic caching |
| **Need to save server storage** | Google Drive | No local disk needed |
| **Frequent updates to GT labels** | Google Drive | Easy to update |
| **Prefer Microsoft ecosystem** | OneDrive | Works with OneDrive setup |

---

## 🔧 Detailed Setup Instructions

### For Google Drive (most popular)

1. **Upload folder to Google Drive:**
   - Right-click IDDAW_ICPR/test/gt_labels
   - Google Drive → Upload folder
   - Wait for upload (~5-10 min)

2. **Get Share Link:**
   - Right-click uploaded folder in Drive
   - Share → Anyone with link can view
   - Copy the link

3. **Extract Folder ID:**
   From: `https://drive.google.com/drive/folders/1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9`
   Extract: `1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9`

4. **Update evaluate_app.py:**
   ```python
   from cloud_storage import STORAGE_GOOGLE_DRIVE
   
   STORAGE_CONFIG = {
       'type': STORAGE_GOOGLE_DRIVE,
       'folder_id': '1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9',
   }
   ```

5. **Test:**
   ```bash
   python evaluate_app.py
   # First run: Downloads ~2-3 GB (10-15 min)
   # Subsequent runs: Use cache (instant)
   ```

### For OneDrive

Follow similar steps but use OneDrive share URL instead.

---

## ⏱️ Performance Timeline

### First Evaluation with Google Drive
```
1. Server starts → checks for cached GT
2. Not found → downloads from Google Drive
3. Downloads ~2-3 GB → takes 10-15 minutes
4. Saves to .gt_cache/ folder
5. Evaluates prediction ZIP
6. Returns results
```

### Subsequent Evaluations
```
1. Server finds cached GT in .gt_cache/
2. Uses cached files (no download)
3. Evaluation completes in 30-60 seconds
4. Very fast!
```

---

## 🆕 New API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

Response shows:
- Storage type (local, gdrive, onedrive)
- Cache size
- Whether GT is available

### Cache Info
```bash
curl http://localhost:5000/api/cache/info
```

### Clear Cache (Admin)
```bash
curl -X POST http://localhost:5000/api/cache/clear
```

---

## 📋 File Structure After Setup

```
Safe-Segmentation-Competition-ICPR-24-main/
├── evaluate_app.py                    [Flask server - EDIT THIS]
├── evaluation_backend.py              [Evaluation logic]
├── cloud_storage.py                   [Cloud storage module - NEW]
├── requirements.txt                   [Dependencies - UPDATED]
├── CLOUD_STORAGE_CONFIG.md            [Setup guide - NEW]
├── CLOUD_CONFIG_EXAMPLES.py           [Config examples - NEW]
├── templates/
│   └── evaluate.html                 [Web interface]
├── uploads/                          [User submissions]
│   └── {user-id}/
│       └── latest_results.json       [Results]
└── .gt_cache/                        [Cached GT (auto-created)]
    ├── gdrive_{folder_id}/           [Google Drive cache]
    └── onedrive_{hash}/              [OneDrive cache]
```

---

## 🔐 Security Notes

- **Public Sharing:** Only share GT folder with authorized users
- **On-Demand Cache:** Files cached locally; ensure server disk is secure
- **API Keys:** Never hardcode in source; use environment variables
- **Access Control:** Restrict /api/cache/clear endpoint in production

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError: gdown" | Run `pip install -r requirements.txt` |
| "Permission denied (Google Drive)" | Verify folder is shared publicly |
| "First run taking a long time" | Normal! 10-15 min for first download |
| "Cache too large" | Run `curl -X POST http://localhost:5000/api/cache/clear` |
| "Connection refused" | Ensure Flask server is running |

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **CLOUD_STORAGE_CONFIG.md** | Detailed setup instructions (start here!) |
| **CLOUD_CONFIG_EXAMPLES.py** | Code examples for each storage type |
| **EVALUATION_SERVER_README.md** | Complete server documentation |
| **templates/evaluate.html** | Web interface code |
| **cloud_storage.py** | Storage backend implementation |

---

## ✅ Checklist Before Deployment

- [ ] Choose storage type (local, Google Drive, OneDrive)
- [ ] If cloud: Upload GT folder and get share link/folder ID
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Update STORAGE_CONFIG in evaluate_app.py
- [ ] Test locally: `python evaluate_app.py`
- [ ] Check health: `curl http://localhost:5000/api/health`
- [ ] Deploy to production
- [ ] Monitor first evaluation (will download GT)

---

## 🎉 What You Can Now Do

✅ Host evaluation server with **no local GT storage** (Google Drive)
✅ **Automatic caching** for fast subsequent evaluations  
✅ **Easy to update** GT labels (just re-upload to Drive)
✅ **Cost-effective** (free Google Drive storage)
✅ **Professional** cloud-enabled competition platform

---

## 🆘 Need Help?

1. Read **CLOUD_STORAGE_CONFIG.md** for detailed setup
2. Check **CLOUD_CONFIG_EXAMPLES.py** for code examples
3. Run `curl http://localhost:5000/api/health` to diagnose issues
4. Check Flask logs for detailed error messages

---

**Safe-Segmentation Competition | ICPR 2024**

Your evaluation server is now ready for production! 🚀
