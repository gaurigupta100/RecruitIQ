import numpy as np
import joblib

from config import CLASSIFIER_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH


class ResumePredictor:
    """Load trained ML artifacts and predict resume categories."""

    def __init__(self):
        self.classifier = joblib.load(CLASSIFIER_PATH)
        self.vectorizer = joblib.load(VECTORIZER_PATH)
        self.label_encoder = joblib.load(LABEL_ENCODER_PATH)

    def predict(self, cleaned_text):
        features = self.vectorizer.transform([cleaned_text])
        prediction_idx = self.classifier.predict(features)[0]
        category = self.label_encoder.inverse_transform([prediction_idx])[0]

        decision_scores = self.classifier.decision_function(features)
        if decision_scores.ndim == 1:
            confidence = self._normalize_binary(decision_scores[0])
        else:
            confidence = self._normalize_multiclass(decision_scores[0])

        return category, round(confidence, 2)

    @staticmethod
    def _normalize_multiclass(scores):
        exp_scores = np.exp(scores - np.max(scores))
        probabilities = exp_scores / exp_scores.sum()
        return float(np.max(probabilities) * 100)

    @staticmethod
    def _normalize_binary(score):
        probability = 1 / (1 + np.exp(-score))
        confidence = max(probability, 1 - probability)
        return float(confidence * 100)


_predictor = None


def get_predictor():
    global _predictor
    if _predictor is None:
        _predictor = ResumePredictor()
    return _predictor
