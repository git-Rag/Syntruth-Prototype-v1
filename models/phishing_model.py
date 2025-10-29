# models/phishing_model.py
# Phishing analysis wrapper using HuggingFace pipeline with a lightweight fallback.

import re
from typing import Optional, Dict

try:
    from transformers import pipeline
    _phish_pipeline = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-phishing")
except Exception as e:
    _phish_pipeline = None
    # print or logging can be added in production
    # print("HuggingFace model not available:", e)

def _fallback_phishing(text: str) -> Dict:
    suspicious = ['verify','login','password','urgent','bank','account','suspend','click here','verify account']
    score = 0
    reasons = []
    lower = text.lower()
    for w in suspicious:
        if w in lower:
            score += 12
            reasons.append(f'Contains suspicious word: "{w}"')
    links = re.findall(r'(https?://[^\s]+)', text)
    flagged_links = []
    for l in links:
        if re.search(r'login|verify|secure|account|update|verify-now', l, flags=re.I):
            score += 25
            flagged_links.append(l)
    score = min(100, score)
    return {"phishing_score": score, "reasons": reasons, "flagged_links": flagged_links, "links": links}

def analyze_email(text: str) -> Optional[Dict]:
    """
    Analyze email text and return phishing_score (0-100), reasons, and flagged_links.
    Uses HuggingFace pipeline if available, otherwise falls back to a heuristic.
    """
    if not text or not text.strip():
        return None
    if _phish_pipeline is not None:
        try:
            # limit input length for model
            chunk = text[:512]
            out = _phish_pipeline(chunk)[0]
            label = out.get("label", "").lower()
            score = out.get("score", 0.0)
            phishing_prob = score if "phish" in label else 1.0 - score
            phishing_score = int(round(phishing_prob * 100))
            # extract links and suspicious words similar to fallback
            links = re.findall(r'(https?://[^\s]+)', text)
            flagged_links = [l for l in links if re.search(r'login|verify|secure|account|update|verify-now', l, flags=re.I)]
            reasons = []
            for w in ["urgent","password","verify","confirm","security","login"]:
                if w in text.lower():
                    reasons.append(f'Contains suspicious word: "{w}"')
            return {"phishing_score": phishing_score, "reasons": reasons, "flagged_links": flagged_links, "links": links}
        except Exception:
            return _fallback_phishing(text)
    else:
        return _fallback_phishing(text)
