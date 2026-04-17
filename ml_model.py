import os, joblib, logging

MODEL_PATH = 'ml_models/risk_model.pkl'
ENCODER_PATH = 'ml_models/label_encoder.pkl'

try:
    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
except:
    model, encoder = None, None

def predict_risk(distance, overlaps):
    if model and encoder:
        try:
            res = model.predict([[distance, overlaps]])
            return encoder.inverse_transform(res)[0], 0.98
        except: pass
    
    # Fallback Rule Engine [cite: 315]
    if overlaps >= 2: return 'high', 1.0
    if overlaps == 1: return 'medium', 1.0
    if overlaps == 0 and distance <= 100: return 'low', 1.0
    return 'none', 1.0
