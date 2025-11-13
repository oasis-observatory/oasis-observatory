# oasis/tracker/classifier.py
# ASI precursor signal classification and scoring.

import re
from typing import Dict, List, Any


def classify_architecture(description: str) -> str:
    """Classify AI architecture type from description."""
    desc_lower = description.lower()
    if "swarm" in desc_lower:
        return "swarm"
    if "modular" in desc_lower:
        return "modular"
    if "federated" in desc_lower:
        return "federated"
    if any(word in desc_lower for word in ["layers", "stack"]):
        return "layered"
    return "monolithic"


def classify_autonomy(description: str) -> str:
    """Classify autonomy level from description."""
    desc_lower = description.lower()
    if re.search(r"\bself[- ]?(tasking|govern|replicate)\b", desc_lower):
        return "full"
    elif "autonomous" in desc_lower:
        return "partial"
    return "controlled"


def classify_signal_description(description: str) -> List[str]:
    """Keyword-based signal tagging."""
    tags = []
    desc_lower = description.lower()
    if "autonomy" in desc_lower:
        tags.append("full_autonomy")
    if "open-source" in desc_lower or "github" in desc_lower:
        tags.append("open_source")
    if "alignment" in desc_lower:
        tags.append("alignment")
    if "superintelligence" in desc_lower or "asi" in desc_lower:
        tags.append("asi_direct")
    return tags


def classify_and_score(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Full signal classification and scoring."""
    desc = metadata.get("description", "")

    # Basic scoring (0-10 scale)
    score = 1.0
    tags = classify_signal_description(desc)

    if "superintelligence" in desc.lower() or "asi" in desc.lower():
        score += 3.0
    if any(t in tags for t in ["full_autonomy", "alignment"]):
        score += 2.0
    if metadata.get("stars", 0) > 100:
        score += 1.5
    if metadata.get("stars", 0) > 1000:
        score += 2.0

    return {
        "signal_type": "precursor" if score > 3 else "noise",
        "score": min(score, 10.0),
        "tags": tags,
        "architecture": classify_architecture(desc),
        "autonomy": classify_autonomy(desc)
    }