"""
Refactored evaluation code for Safe-Segmentation competition.
Can be used both as a standalone script and imported by the Flask app.
"""

import numpy as np
import json
from PIL import Image
from pathlib import Path
from typing import Tuple, Dict, List
import os

L3_CLASSES = ['road', 'drivable fallback', 'sidewalk', 'non drivable fallback', 'person', 'rider', 'motorcycle', 'bicycle',
                'autorickshaw', 'car', 'truck', 'bus', 'vehicle fallback', 'curb', 'wall', 'fence', 'guard rail', 'billboard',
                'traffic sign', 'traffic light', 'pole', 'obs-str-bar-fallback', 'building', 'bridge', 'vegetation', 'sky']

IMP_CLASSES = ['person', 'rider', 'motorcycle', 'bicycle', 'autorickshaw', 'car', 'truck', 'bus']


class SemanticHierarchy:
    def __init__(self):
        self.d = {}

    def add_class(self, class_name, N1=[], N2=[], N3=[]):
        self.d[class_name] = {'N1': N1, 'N2': N2, 'N3': N3}

    def initialize_hierarchy(self):
        self.add_class('road', N2=['drivable fallback'])
        self.add_class('drivable fallback', N2=['road'])
        self.add_class('sidewalk', N2=['non drivable fallback'])
        self.add_class('non drivable fallback', N2=['sidewalk'])
        self.add_class('person', N2=['rider'])
        self.add_class('rider', N2=['person'])
        self.add_class('motorcycle', N1=['bicycle'], N2=['autorickshaw', 'car', 'truck', 'bus', 'vehicle fallback'])
        self.add_class('bicycle', N1=['motorcycle'], N2=['autorickshaw', 'car', 'truck', 'bus', 'vehicle fallback'])
        self.add_class('autorickshaw', N1=['car'], N2=['bicycle', 'motorcycle', 'truck', 'bus', 'vehicle fallback'])
        self.add_class('car', N1=['autorickshaw'], N2=['bicycle', 'motorcycle', 'truck', 'bus', 'vehicle fallback'])
        self.add_class('truck', N1=['bus', 'vehicle fallback'], N2=['motorcycle', 'bicycle', 'autorickshaw', 'car'])
        self.add_class('bus', N1=['truck', 'vehicle fallback'], N2=['motorcycle', 'bicycle', 'autorickshaw', 'car'])
        self.add_class('vehicle fallback', N1=['truck', 'bus'], N2=['motorcycle', 'bicycle', 'autorickshaw', 'car'])
        self.add_class('curb', N1=['wall'], N2=['fence', 'guard rail', 'billboard', 'traffic sign', 'traffic light'])
        self.add_class('wall', N1=['curb'], N2=['fence', 'guard rail', 'billboard', 'traffic sign', 'traffic light'])
        self.add_class('fence', N1=['guard rail'], N2=['curb', 'wall', 'billboard', 'traffic sign', 'traffic light'])
        self.add_class('guard rail', N1=['fence'], N2=['curb', 'wall', 'billboard', 'traffic sign', 'traffic light'])
        self.add_class('billboard', N1=['traffic sign', 'traffic light'], N2=['curb', 'wall', 'fence', 'guard rail'])
        self.add_class('traffic sign', N1=['billboard', 'traffic light'], N2=['curb', 'wall', 'fence', 'guard rail'])
        self.add_class('traffic light', N1=['billboard', 'traffic sign'], N2=['curb', 'wall', 'fence', 'guard rail'])
        self.add_class('pole', N1=['obs-str-bar-fallback'], N2=['curb', 'wall', 'fence', 'guard rail', 'billboard', 'traffic light', 'traffic sign'])
        self.add_class('obs-str-bar-fallback', N1=['pole'], N2=['curb', 'wall', 'fence', 'guard rail', 'billboard', 'traffic light', 'traffic sign'])
        self.add_class('building', N1=['bridge'], N2=['vegetation'])
        self.add_class('bridge', N1=['building'], N2=['vegetation'])
        self.add_class('vegetation', N2=['bridge', 'building'])
        self.add_class('sky')

    def generate_N3_classes(self, L3_CLASSES):
        for class_name in L3_CLASSES:
            cu_classes = [class_name] + self.d[class_name]['N1'] + self.d[class_name]['N2']
            self.d[class_name]['N3'] = [x for x in L3_CLASSES if x not in cu_classes]

    def get_important_classes(self, IMP_CLASSES, L3_CLASSES):
        ind_of_imp_classes = [i for i, class_name in enumerate(L3_CLASSES) if class_name in IMP_CLASSES]
        return ind_of_imp_classes

    def class_to_id_mapping(self, L3_CLASSES):
        return {class_name: i for i, class_name in enumerate(L3_CLASSES)}


def fast_hist(a, b, n):
    """Compute confusion matrix histogram."""
    k = (a >= 0) & (a < n)
    return np.bincount(n * a[k].astype(int) + b[k], minlength=n ** 2).reshape(n, n)


def per_class_iu(hist, class_mapping, IMP_CLASSES, ind_of_imp_classes, num_classes=len(L3_CLASSES)):
    """Compute IoU and Safe-IoU for each class."""
    ious = []
    safe_ious = []
    den = hist.sum(1) + hist.sum(0) - np.diag(hist)

    hierarchy = SemanticHierarchy()
    hierarchy.initialize_hierarchy()

    for i in range(num_classes):
        current_class = L3_CLASSES[i]
        D = den[i]
        N = hist[i][i]

        T1 = T2 = T3 = penality = 0
        if current_class in IMP_CLASSES:
            for c in [class_mapping[x] for x in hierarchy.d[current_class]['N1']]:
                T1 += hist[i][c]

            for c in [class_mapping[x] for x in hierarchy.d[current_class]['N2']]:
                T2 += hist[i][c]

            for c in [class_mapping[x] for x in hierarchy.d[current_class]['N3']]:
                T3 += hist[i][c]

            W = [1/3, 2/3, 3/3]
            penality = (W[0] * T1) + (W[1] * T2) + (W[2] * T3)
        else:
            for c in [class_mapping[x] for x in hierarchy.d[current_class]['N1']]:
                if c in ind_of_imp_classes:
                    T1 += hist[i][c]

            for c in [class_mapping[x] for x in hierarchy.d[current_class]['N2']]:
                if c in ind_of_imp_classes:
                    T2 += hist[i][c]

            for c in [class_mapping[x] for x in hierarchy.d[current_class]['N3']]:
                if c in ind_of_imp_classes:
                    T3 += hist[i][c]

            W = [1/3, 2/3, 3/3]
            penality = (W[0] * T1) + (W[1] * T2) + (W[2] * T3)

        iou = N / D if D > 0 else 0
        safe_iou = (N - penality) / D if D > 0 else 0

        ious.append(iou)
        safe_ious.append(safe_iou)

    return ious, safe_ious


def evaluate_predictions(gt_dir: str, pred_dir: str) -> Dict:
    """
    Evaluate predictions against ground truth.
    
    Args:
        gt_dir: Directory containing ground truth labels
        pred_dir: Directory containing predictions
        
    Returns:
        Dictionary with evaluation results
    """
    # Initialize hierarchy
    hierarchy = SemanticHierarchy()
    hierarchy.initialize_hierarchy()
    hierarchy.generate_N3_classes(L3_CLASSES)
    
    ind_of_imp_classes = hierarchy.get_important_classes(IMP_CLASSES, L3_CLASSES)
    class_mapping = hierarchy.class_to_id_mapping(L3_CLASSES)
    
    num_classes = len(L3_CLASSES)
    hist = np.zeros((num_classes, num_classes))
    
    # Find all ground truth files
    gt_files = sorted(Path(gt_dir).glob('**/*.png'))
    
    if not gt_files:
        return {
            'status': 'error',
            'message': f'No ground truth PNG files found in {gt_dir}'
        }
    
    # Process each ground truth file
    processed = 0
    skipped = 0
    
    for gt_file in gt_files:
        # Construct prediction filename (assuming same structure)
        # GT filename format: *_labellevel3Ids.png -> prediction: *_pred.png or similar
        relative_path = gt_file.relative_to(gt_dir)
        
        # Try to find matching prediction file
        pred_file = Path(pred_dir) / relative_path.name
        
        if not pred_file.exists():
            # Try alternative naming convention
            base_name = gt_file.stem.replace('_labellevel3Ids', '')
            pred_file = Path(pred_dir) / f'{base_name}_pred.png'
            
            if not pred_file.exists():
                skipped += 1
                continue
        
        try:
            # Load images
            gt = np.array(Image.open(str(gt_file)))
            pred = np.array(Image.open(str(pred_file)))
            
            # Ensure same shape
            if gt.shape != pred.shape:
                skipped += 1
                continue
            
            # Compute histogram
            hist += fast_hist(gt.flatten(), pred.flatten(), num_classes)
            processed += 1
            
        except Exception as e:
            skipped += 1
            continue
    
    if processed == 0:
        return {
            'status': 'error',
            'message': 'No valid prediction-ground truth pairs found'
        }
    
    # Compute metrics
    mIoUs, SmIoUs = per_class_iu(hist, class_mapping, IMP_CLASSES, ind_of_imp_classes, num_classes)
    
    # Prepare results
    class_results = []
    for i in range(num_classes):
        class_results.append({
            'class_id': i,
            'class_name': L3_CLASSES[i],
            'miou': round(mIoUs[i] * 100, 2),
            'safe_miou': round(SmIoUs[i] * 100, 2),
            'is_important': L3_CLASSES[i] in IMP_CLASSES
        })
    
    # Overall metrics
    overall_miou = np.nanmean(mIoUs) * 100
    overall_safe_miou = np.nanmean(SmIoUs) * 100
    important_miou = np.nanmean([mIoUs[i] for i in ind_of_imp_classes]) * 100
    important_safe_miou = np.nanmean([SmIoUs[i] for i in ind_of_imp_classes]) * 100
    
    return {
        'status': 'success',
        'processed_images': processed,
        'skipped_images': skipped,
        'overall_miou': round(overall_miou, 2),
        'overall_safe_miou': round(overall_safe_miou, 2),
        'important_miou': round(important_miou, 2),
        'important_safe_miou': round(important_safe_miou, 2),
        'class_results': class_results
    }
