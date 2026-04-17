from flask import Blueprint, jsonify, request
from database import get_hazard_layers # <-- Updated import name

hazards_bp = Blueprint('hazards_bp', __name__)

@hazards_bp.route('/hazards', methods=['GET'])
def get_hazards():
    hazard_query_type = request.args.get('type')

    # <-- Updated function call
    results = get_hazard_layers(
        table_name='hazard_layers', 
        hazard_type=hazard_query_type
    )

    features = []
    for row in results:
        features.append({
            "type": "Feature",
            "geometry": row['geometry'], 
            "properties": {
                "hazard_type": row['hazard_type'],
                "hazard_level": row['hazard_level']
            }
        })

    return jsonify({
        "type": "FeatureCollection",
        "features": features,
        "status": "success",
        "count": len(features)
    })