# Example Cloud Storage Configurations
# Copy and paste these configurations into evaluate_app.py STORAGE_CONFIG

# ==============================================================================
# EXAMPLE 1: LOCAL STORAGE (Default - No downloads needed)
# ==============================================================================
"""
STORAGE_CONFIG = {
    'type': STORAGE_LOCAL,
    'path': os.path.abspath('IDDAW_ICPR/test/gt_labels'),
}

Best for: Server with disk space available
Setup time: None (if files already on server)
First run: Instant
Subsequent runs: Instant
"""


# ==============================================================================
# EXAMPLE 2: GOOGLE DRIVE STORAGE (Free, automated caching)
# ==============================================================================
"""
from cloud_storage import STORAGE_GOOGLE_DRIVE

STORAGE_CONFIG = {
    'type': STORAGE_GOOGLE_DRIVE,
    'folder_id': '1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9',  # ← Replace with your folder ID
}

How to get folder ID:
1. Upload IDDAW_ICPR/test/gt_labels to Google Drive
2. Right-click folder → Share → Copy link
3. Extract from: https://drive.google.com/drive/folders/[FOLDER_ID]

Setup time: 5 minutes
First run: 10-15 minutes (downloads ~2-3 GB)
Subsequent runs: Few seconds (uses cache)
Cache location: .gt_cache/gdrive_<folder_id>/

Note: First evaluation will take longer due to download.
      After first run, all subsequent evaluations are fast due to caching.
"""


# ==============================================================================
# EXAMPLE 3: ONEDRIVE STORAGE (Alternative to Google Drive)
# ==============================================================================
"""
STORAGE_CONFIG = {
    'type': 'onedrive',
    'share_url': 'https://onedrive.live.com/?resid=ABC123...&download=1',  # ← Replace
}

How to get share URL:
1. Upload IDDAW_ICPR/test/gt_labels to OneDrive
2. Right-click folder → Share → Copy download link
3. Paste the link (should end with ?download=1)

Setup time: 5 minutes
First run: 10-15 minutes (downloads ~2-3 GB)
Subsequent runs: Few seconds (uses cache)
Cache location: .gt_cache/onedrive_<hash>/
"""


# ==============================================================================
# EXAMPLE 4: LOCAL STORAGE WITH CUSTOM PATH
# ==============================================================================
"""
STORAGE_CONFIG = {
    'type': STORAGE_LOCAL,
    'path': '/var/data/iddaw/test/gt_labels',  # Absolute path
}

Best for: Server with mounted network drive or custom storage location
"""


# ==============================================================================
# COMMON MISTAKES TO AVOID
# ==============================================================================
"""
❌ WRONG - Missing import:
STORAGE_CONFIG = {
    'type': STORAGE_GOOGLE_DRIVE,  # NameError: STORAGE_GOOGLE_DRIVE not defined
    'folder_id': '...',
}

✅ CORRECT - Import the constant:
from cloud_storage import STORAGE_GOOGLE_DRIVE

STORAGE_CONFIG = {
    'type': STORAGE_GOOGLE_DRIVE,
    'folder_id': '...',
}


❌ WRONG - Invalid folder ID:
'folder_id': 'https://drive.google.com/drive/folders/1ABC...'  # Full URL

✅ CORRECT - Just the ID part:
'folder_id': '1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9'  # Just the ID


❌ WRONG - Local path doesn't exist:
'path': 'IDDAW_ICPR/test/gt_labels'  # Relative path might not exist

✅ CORRECT - Use absolute path or verify relative path:
'path': os.path.abspath('IDDAW_ICPR/test/gt_labels')
"""


# ==============================================================================
# TESTING YOUR CONFIGURATION
# ==============================================================================
"""
After updating STORAGE_CONFIG, test with:

1. Start server:
   python evaluate_app.py

2. Check health in another terminal:
   curl http://localhost:5000/api/health

3. Expected response for Google Drive:
{
  "status": "ok",
  "gt_directory_exists": true,
  "gt_path": ".gt_cache/gdrive_1ABC2DEF3GHI4JKL5MNO6PQR7STU8VWX9/...",
  "storage_type": "gdrive",
  "cache_size": "2.45 GB",
  "cache_enabled": true
}

   If status is "error", check:
   - Folder ID is correct
   - Share link is publicly accessible
   - Internet connection is working
   - Ground truth files are in the folder
"""


# ==============================================================================
# PERFORMANCE COMPARISON
# ==============================================================================
"""
Storage Type | Setup | First Run | After | Disk Space | Cost
-------------|-------|-----------|-------|------------|------
Local        | None  | Instant   | Fast  | 20-30 GB   | Free*
Google Drive | 5 min | 10-15 min | Fast  | 20-30 GB   | Free
OneDrive     | 5 min | 10-15 min | Fast  | 20-30 GB   | Free
Cloud (S3)   | 10min | 10-15 min | Fast  | 0 GB       | $$$

* Local requires server disk space
"""


# ==============================================================================
# CACHING DETAILS
# ==============================================================================
"""
When using Google Drive or OneDrive:

First Evaluation (no cache):
  1. Server detects missing ground truth
  2. Starts downloading from cloud
  3. Shows progress in terminal/logs
  4. Takes 10-15 minutes for 2-3 GB
  5. Saves to .gt_cache/ for reuse

Subsequent Evaluations (with cache):
  1. Server finds cached ground truth
  2. Loads instantly from local disk
  3. Evaluation completes in ~30-60 seconds
  4. Fast and reliable

To disable caching (not recommended):
  ENABLE_CACHE = False

To clear cache:
  curl -X POST http://localhost:5000/api/cache/clear
"""
