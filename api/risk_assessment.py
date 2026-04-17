from flask import Blueprint, request, jsonify
from database import get_spatial_features
from ml_model import predict_risk

risk_bp = Blueprint('risk_assessment', __name__)

# Cebu Bounds validation
def is_cebu(lat, lon):
    return (9.4 <= lat <= 11.3) and (123.2 <= lon <= 124.1)

@risk_bp.route('/risk-assessment', methods=['POST'])
def assess():
    data = request.json
    lat, lon = data.get('latitude'), data.get('longitude')
    if not lat or not lon or not is_cebu(lat, lon):
        return jsonify({"success": False, "error": "Invalid or non-Cebu coordinates"}), 400
    
    dist, overlaps = get_spatial_features(lat, lon)
    level, score = predict_risk(dist, overlaps)
    
    return jsonify({
        "success": True, 
        "data": {
            "risk_level": level, 
            "features": {"distance_to_nearest_hazard": dist, "overlapping_hazards": overlaps}
        }
    })
