"""
Cloud Storage Support for IDDAW Ground Truth
Supports: Google Drive, OneDrive, or Local Storage
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional, Tuple
import gdown
import zipfile

logger = logging.getLogger(__name__)

# Storage type constants
STORAGE_LOCAL = 'local'
STORAGE_GOOGLE_DRIVE = 'gdrive'
STORAGE_ONEDRIVE = 'onedrive'

# Cache directory for downloaded files
CACHE_DIR = '.gt_cache'


class GroundTruthStorage:
    """Manages ground truth retrieval from various storage backends."""
    
    def __init__(self, storage_type: str = STORAGE_LOCAL, cache_enabled: bool = True):
        """
        Initialize storage backend.
        
        Args:
            storage_type: Type of storage (local, gdrive, onedrive)
            cache_enabled: Whether to cache downloaded files
        """
        self.storage_type = storage_type
        self.cache_enabled = cache_enabled
        self.cache_dir = Path(CACHE_DIR)
        
        if cache_enabled:
            self.cache_dir.mkdir(exist_ok=True)
    
    def get_ground_truth_dir(self, config: dict) -> Tuple[str, Optional[str]]:
        """
        Get ground truth directory path.
        
        Args:
            config: Configuration dict with storage details
                   - For local: {'path': '/path/to/gt_labels'}
                   - For gdrive: {'folder_id': 'GOOGLE_FOLDER_ID'}
                   - For onedrive: {'share_url': 'onedrive_share_url'}
        
        Returns:
            Tuple of (path_to_gt_dir, error_message)
        """
        if self.storage_type == STORAGE_LOCAL:
            return self._get_local(config)
        elif self.storage_type == STORAGE_GOOGLE_DRIVE:
            return self._get_gdrive(config)
        elif self.storage_type == STORAGE_ONEDRIVE:
            return self._get_onedrive(config)
        else:
            return None, f"Unknown storage type: {self.storage_type}"
    
    def _get_local(self, config: dict) -> Tuple[Optional[str], Optional[str]]:
        """Get ground truth from local filesystem."""
        path = config.get('path')
        
        if not path:
            return None, "Local path not specified in config"
        
        if not os.path.exists(path):
            return None, f"Local path does not exist: {path}"
        
        return path, None
    
    def _get_gdrive(self, config: dict) -> Tuple[Optional[str], Optional[str]]:
        """
        Download ground truth from Google Drive.
        
        Config should have:
            folder_id: Google Drive folder ID (from share link)
        """
        folder_id = config.get('folder_id')
        
        if not folder_id:
            return None, "Google Drive folder_id not specified"
        
        # Check cache first
        cache_path = self.cache_dir / f"gdrive_{folder_id}"
        if self.cache_enabled and cache_path.exists():
            logger.info(f"Using cached Google Drive data from {cache_path}")
            return str(cache_path), None
        
        try:
            logger.info(f"Downloading from Google Drive folder: {folder_id}")
            
            # Create download directory
            cache_path.mkdir(parents=True, exist_ok=True)
            
            # Download folder
            gdown.download_folder(
                f"https://drive.google.com/drive/folders/{folder_id}",
                output=str(cache_path),
                quiet=False,
                use_cookies=False
            )
            
            logger.info(f"Successfully downloaded to {cache_path}")
            return str(cache_path), None
            
        except Exception as e:
            error_msg = f"Failed to download from Google Drive: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    def _get_onedrive(self, config: dict) -> Tuple[Optional[str], Optional[str]]:
        """
        Download ground truth from OneDrive.
        
        Config should have:
            share_url: OneDrive share URL (shareable link)
        """
        share_url = config.get('share_url')
        
        if not share_url:
            return None, "OneDrive share_url not specified"
        
        try:
            # Extract folder name from share_url for caching
            folder_hash = abs(hash(share_url)) % (10 ** 8)
            cache_path = self.cache_dir / f"onedrive_{folder_hash}"
            
            # Check cache first
            if self.cache_enabled and cache_path.exists():
                logger.info(f"Using cached OneDrive data from {cache_path}")
                return str(cache_path), None
            
            logger.info(f"Downloading from OneDrive")
            
            # Convert share URL to download URL
            download_url = self._convert_onedrive_url(share_url)
            
            # Create download directory
            cache_path.mkdir(parents=True, exist_ok=True)
            
            # Download using gdown (works with OneDrive URLs too)
            gdown.download(
                download_url,
                str(cache_path / "gt_labels.zip"),
                quiet=False
            )
            
            # Extract if ZIP
            zip_path = cache_path / "gt_labels.zip"
            if zip_path.exists():
                logger.info("Extracting downloaded archive...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(cache_path)
                zip_path.unlink()
            
            logger.info(f"Successfully downloaded to {cache_path}")
            return str(cache_path), None
            
        except Exception as e:
            error_msg = f"Failed to download from OneDrive: {str(e)}"
            logger.error(error_msg)
            return None, error_msg
    
    @staticmethod
    def _convert_onedrive_url(share_url: str) -> str:
        """Convert OneDrive share URL to download URL."""
        # Remove query parameters and convert to download format
        base_url = share_url.split('?')[0]
        
        # If it's already a download URL, return as is
        if 'download=1' in share_url:
            return share_url
        
        # Convert share URL to download URL
        if 'redir' in base_url:
            base_url = base_url.replace('redir', 'download')
        else:
            base_url += '?download=1'
        
        return base_url
    
    def clear_cache(self):
        """Clear all cached ground truth data."""
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            logger.info(f"Cleared cache directory: {self.cache_dir}")
    
    def cache_size(self) -> str:
        """Get total cache size as human-readable string."""
        if not self.cache_dir.exists():
            return "0 B"
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.cache_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        
        # Convert to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total_size < 1024:
                return f"{total_size:.2f} {unit}"
            total_size /= 1024
        
        return f"{total_size:.2f} TB"
