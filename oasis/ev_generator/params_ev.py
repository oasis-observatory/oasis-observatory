# oasis/ev_generator/params_ev.py
"""
Adjust base scenario parameters based on precursor signals (flat structure).
"""

from typing import Dict, List, Any
import random
from oasis.s_generator.params_s import sample_parameters


class SignalInfluenceModel:
    """
    Applies precursor-signal-derived influence to flat ASI scenario parameters.
    """

    def __init__(self, strength: float = 0.35):
        self.strength = max(0.0, min(1.0, strength))

    def extract_features(self, signals: List[Dict[str, Any]]) -> Dict[str, float]:
        features = {
            "modular": 0,
            "decentralized": 0,
            "embodied": 0,
            "agentic": 0,
            "alignment": 0,
            "risk": 0,
            "power": 0,
            "safety": 0,
        }

        for sig in signals:
            text = " ".join([
                (sig.get("title") or "").lower(),
                (sig.get("description") or "").lower(),
                " ".join([t.lower() for t in sig.get("tags") or []])
            ])

            if "modular" in text:
                features["modular"] += 1
            if "distributed" in text or "decentral" in text:
                features["decentralized"] += 1
            if "robot" in text or "embodied" in text:
                features["embodied"] += 1
            if "agent" in text or "autonomous" in text:
                features["agentic"] += 1
            if "align" in text:
                features["alignment"] += 1
            if "risk" in text or "threat" in text:
                features["risk"] += 1
            if "power" in text or "control" in text:
                features["power"] += 1
            if "safety" in text or "guardrail" in text:
                features["safety"] += 1

        if signals:
            for k in features:
                features[k] = features[k] / len(signals)

        return features

    def transform_parameters(self, base: Dict[str, Any], feats: Dict[str, float]) -> Dict[str, Any]:
        influenced = dict(base)

        # Architecture influence
        if feats["modular"] > 0.3:
            influenced["architecture"] = self._blend_choice(base.get("architecture", "monolithic"), "modular", feats["modular"])

        if feats["decentralized"] > 0.3:
            influenced["deployment_topology"] = self._blend_choice(base.get("deployment_topology", "centralized"), "decentralized", feats["decentralized"])

        # Substrate influence
        if feats["embodied"] > 0.3:
            influenced["deployment_medium"] = self._blend_choice(base.get("deployment_medium", "edge"), "embodied", feats["embodied"])

        # Agency & risk
        if feats["agentic"] > 0:
            influenced["agency_level"] = self._blend_float(base.get("agency_level", 0.5), min(1.0, 0.3 + feats["agentic"]), self.strength)

        if feats["risk"] > 0:
            influenced["deceptiveness"] = self._blend_float(base.get("deceptiveness", 0.5), min(1.0, 0.5 + feats["risk"]), self.strength)

        # Alignment & safety
        if feats["alignment"] > 0 or feats["safety"] > 0:
            influenced["alignment_score"] = self._blend_float(base.get("alignment_score", 0.5), max(0.3, feats["alignment"] + feats["safety"]), self.strength)

        # Power goals
        if feats["power"] > 0.2:
            influenced["stated_goal"] = self._blend_choice(base.get("stated_goal", "default"), "power", feats["power"])

        return influenced

    # ===== Utility functions =====
    def _blend_float(self, original: float, target: float, w: float) -> float:
        return (1 - w) * original + w * target

    def _blend_choice(self, original: str, target: str, w: float) -> str:
        if random.random() < w * self.strength:
            return target
        return original


# ==== Public API ====
def generate_ev_parameters(signals: List[Dict[str, Any]], influence_strength: float = 0.35) -> Dict[str, Any]:
    """
    Main entrypoint used by EV generator.
    """
    base = sample_parameters()
    model = SignalInfluenceModel(strength=influence_strength)
    feats = model.extract_features(signals)
    influenced = model.transform_parameters(base, feats)
    return influenced
