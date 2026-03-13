# Cloud Storage Configuration Guide

This guide explains how to configure the evaluation server to use Google Drive, OneDrive, or local storage for ground truth data.

## 🎯 Quick Configuration

### 1. Local Storage (Default - No Setup Needed)
```python
# In evaluate_app.py, STORAGE_CONFIG section:

STORAGE_CONFIG = {
    'type': STORAGE_LOCAL,
    'path': os.path.abspath('IDDAW_ICPR/test/gt_labels'),
}
```

✅ Best for: Server with sufficient disk space (>30GB)

---

### 2. Google Drive Storage

#### Step 1: Create Shareable Folder
1. Upload `IDDAW_ICPR/test/gt_labels` to Google Drive
2. Right-click folder → **Share**
3. Allow "Anyone with the link" → Copy link

Example link: `https://drive.google.com/drive/folders/1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9`

#### Step 2: Extract Folder ID
From the link above, the folder ID is: `1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9`

#### Step 3: Update Configuration
```python
# In evaluate_app.py, STORAGE_CONFIG section:
from cloud_storage import STORAGE_GOOGLE_DRIVE

STORAGE_CONFIG = {
    'type': STORAGE_GOOGLE_DRIVE,
    'folder_id': '1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9',  # Your folder ID
}
```

✅ Benefits:
- No local disk space needed
- Automatic caching (first download: 10-15 min, subsequent: instant)
- Easy to update labels

---

### 3. OneDrive Storage

#### Step 1: Upload Folder
1. Upload `IDDAW_ICPR/test/gt_labels` to OneDrive
2. Right-click folder → **Share** → **Copy link**

Example link: `https://onedrive.live.com/?resid=...`

#### Step 2: Get Download URL
1. Open shared folder
2. Right-click → **Download** or copy the downloadable link
3. Should end with `?download=1`

#### Step 3: Update Configuration
```python
# In evaluate_app.py, STORAGE_CONFIG section:

STORAGE_CONFIG = {
    'type': 'onedrive',
    'share_url': 'https://onedrive.live.com/?resid=ABC123...&download=1',
}
```

---

## 🚀 Installation & Testing

### Step 1: Install Updated Dependencies
```bash
pip install -r requirements.txt
```

New packages: `gdown`, `requests`, `tqdm`

### Step 2: Update Configuration
Edit `evaluate_app.py` and set your storage configuration (see above)

### Step 3: Test Server
```bash
python evaluate_app.py
```

Visit: `http://localhost:5000/api/health`

Expected response (Google Drive):
```json
{
  "status": "ok",
  "gt_directory_exists": true,
  "storage_type": "gdrive",
  "cache_size": "2.45 GB",
  "cache_enabled": true
}
```

---

## 💾 Caching Behavior

### First Run (E.g., Google Drive)
1. Server detects missing ground truth
2. Starts downloading from Google Drive (~10-15 min for 2-3 GB)
3. Caches to `.gt_cache/gdrive_<folder_id>/`
4. Subsequent runs use cache (instant)

### Disable Cache (Not Recommended)
```python
# In evaluate_app.py:
ENABLE_CACHE = False
```

### Clear Cache
```bash
# Via API
curl -X POST http://localhost:5000/api/cache/clear

# Or programmatically
# Storage will automatically delete .gt_cache/ on startup if disabled
```

---

## 📊 Performance Comparison

| Storage | First Run | Subsequent Runs | Disk Space | Setup Complexity |
|---------|-----------|-----------------|------------|------------------|
| Local | Instant | Instant | 20-30 GB | ⭐ Easy |
| Google Drive | 10-15 min | Instant | 20-30 GB | ⭐⭐ Medium |
| OneDrive | 10-15 min | Instant | 20-30 GB | ⭐⭐ Medium |

---

## 🔧 Advanced Configuration

### Disable Caching
```python
ENABLE_CACHE = False
```
⚠️ Warning: Server will redownload ~2-3 GB on every evaluation!

### Custom Cache Location
Edit `cloud_storage.py` line 19:
```python
CACHE_DIR = '/var/cache/gt_data'  # Or any path
```

### Environment Variables (Optional)
Create `.env` file:
```bash
STORAGE_TYPE=gdrive
GDRIVE_FOLDER_ID=1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9
ENABLE_CACHE=true
```

Then in `evaluate_app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()
STORAGE_CONFIG = {
    'type': os.getenv('STORAGE_TYPE', STORAGE_LOCAL),
    'folder_id': os.getenv('GDRIVE_FOLDER_ID'),
}
```

---

## 🐛 Troubleshooting

### "Permission denied" (Google Drive)
- Ensure folder is shared publicly or with link
- Check folder ID is correct
- Try re-generating share link

### "Download failed" (OneDrive)
- Verify download URL ends with `?download=1`
- OneDrive share links may expire; refresh sharing
- Alternative: Use Google Drive instead

### "Timeout" on First Run
- Normal for first download (~10-15 min)
- Check internet connection
- Server is still running; check logs with verbose output:
  ```bash
  python -u evaluate_app.py  # Unbuffered output
  ```

### Cache Takes Too Much Space
- Use OnDemand mode: Set `ENABLE_CACHE = False` (not recommended)
- Or periodically clear: `curl -X POST http://localhost:5000/api/cache/clear`
- Or increase server storage

### "No PNG files found"
- This is user error (prediction ZIP format)
- Not related to ground truth storage
- Check user's uploaded ZIP file structure

---

## 🌐 Deployment Recommendation

### For Small Deployments (< 100 evaluations/month)
**Use Local Storage** - Simplest, fastest

### For Medium Deployments (100-1000 evaluations/month)
**Use Google Drive** with caching
- Cost: Free (Google Drive storage)
- Performance: Good
- Reliability: Excellent

### For Large Deployments (> 1000 evaluations/month)
**Use Local Storage** on cloud server
- Cost: Cloud storage (AWS S3, Azure, GCP)
- Performance: Fastest
- Reliability: Excellent

---

## 📝 Configuration Checklist

- [ ] Download/upload ground truth to chosen storage
- [ ] Get folder ID / share URL
- [ ] Update `STORAGE_CONFIG` in `evaluate_app.py`
- [ ] Run `pip install -r requirements.txt`
- [ ] Test: `python evaluate_app.py`
- [ ] Check health: `curl http://localhost:5000/api/health`
- [ ] Deploy to production

---

## 🔐 Security Notes

1. **Sharing:** Use organization/private links if possible
2. **Cache:** Cache files stored locally; ensure disk is secure
3. **Credentials:** Never hardcode API keys; use environment variables
4. **Access:** Only share links with authorized users

---

For questions or issues, see main README or contact administrators.
