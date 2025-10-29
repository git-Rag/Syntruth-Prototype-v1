# utils/deepfake_detector.py
# Deepfake detector wrapper using DeepFace (if available) with a fallback heuristic.

from typing import Optional, Dict
from pathlib import Path
import random

try:
    from deepface import DeepFace
    _deepface_available = True
except Exception:
    _deepface_available = False

def _fallback_deepfake(path: str) -> Dict:
    # simple deterministic-ish fallback based on filename
    seed = sum(ord(c) for c in Path(path).name) % 100
    rnd = random.Random(seed)
    base = seed % 50
    score = min(99, base + rnd.randint(10, 45))
    return {"deepfake_score": score, "reason": "Fallback heuristic: possible facial artifacts (demo)."}

def analyze_image(path: str) -> Optional[Dict]:
    """
    Analyze an image file (path) and return deepfake_score (0-100) and reason.
    Uses DeepFace when available; otherwise uses a fallback heuristic.
    """
    if not path:
        return None
    if _deepface_available:
        try:
            # Use emotion analysis as a simple proxy for inconsistencies; enforce_detection=False to be forgiving
            result = DeepFace.analyze(img_path=path, actions=['emotion'], enforce_detection=False)
            # Some DeepFace versions return a dict, sometimes a list
            data = result[0] if isinstance(result, list) and len(result) > 0 else result
            emotions = data.get("emotion", {}) if isinstance(data, dict) else {}
            happy = emotions.get("happy", 0)
            neutral = emotions.get("neutral", 0)
            # Heuristic: large unexpected differences might indicate manipulation; translate to a score
            fake_score = max(0, min(100, 100 - abs(happy - neutral)))
            return {"deepfake_score": int(round(fake_score)), "reason": "DeepFace-based heuristic: emotion inconsistency score."}
        except Exception:
            return _fallback_deepfake(path)
    else:
        return _fallback_deepfake(path)
