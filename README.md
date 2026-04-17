# HazardWatch Backend API

A geospatial backend service that serves hazard data (flood, landslide, storm surge) and determines location-based risk levels — inspired by the NOAH hazard mapping platform.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Setup Instructions](#setup-instructions)
4. [Database Schema](#database-schema)
5. [ML Approach](#ml-approach)
6. [API Documentation](#api-documentation)
7. [Sample Requests & Responses](#sample-requests--responses)
8. [Project Structure](#project-structure)

---

## Project Overview

HazardWatch exposes REST APIs to:
- Serve hazard polygon layers (flood, landslide, storm surge) stored in PostGIS
- Filter layers by hazard type
- Assess risk for a given coordinate using spatial analysis and an ML model

The dataset is sourced from [NOAH Downloads](https://noah.up.edu.ph/) covering Cebu province.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask 2.3.2 |
| Database | PostgreSQL + PostGIS |
| Spatial ORM | GeoAlchemy2, psycopg2 |
| Data Processing | GeoPandas, Shapely |
| Machine Learning | scikit-learn, XGBoost, joblib |
| Environment Config | python-dotenv |

---

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL with PostGIS extension enabled
- A `Cebu.gpkg` GeoPackage file placed in the `data/` folder

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hazardwatch-backend.git
cd hazardwatch-backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hazard_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 4. Set Up the Database

Enable PostGIS in your PostgreSQL database:

```sql
CREATE DATABASE hazard_db;
\c hazard_db
CREATE EXTENSION postgis;
```

### 5. Ingest Hazard Data

Place your `Cebu.gpkg` file in the `data/` folder, then run:

```bash
python scripts/ingest_data.py
```

This will read the GeoPackage, normalize the columns, reproject geometries to EPSG:4326, and upload to the `hazard_layers` table.

### 6. Train the ML Model (Optional)

If pre-trained models are not present in `ml_models/`, train them before starting the server. If no model is found, the system falls back to a rule-based engine automatically.

### 7. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

---

## Database Schema

### Table: `hazard_layers`

| Column | Type | Description |
|---|---|---|
| `hazard_type` | TEXT | Type of hazard: `flood`, `landslide`, or `storm_surge` |
| `hazard_level` | TEXT | Severity level: `1` (low), `2` (medium), `3` (high) |
| `geometry` | GEOMETRY(MultiPolygon, 4326) | Hazard polygon in WGS84 |

> The table is created automatically by `ingest.py` using `gdf.to_postgis()`. The `if_exists='replace'` flag ensures a clean upload each time ingestion is run.

### Key PostGIS Queries Used

**Overlap check** — counts how many hazard polygons contain a given point:

```sql
SELECT COUNT(*)
FROM hazard_layers
WHERE ST_Intersects(geometry, ST_SetSRID(ST_MakePoint(<lon>, <lat>), 4326));
```

**Distance to nearest hazard** — returns distance in meters using geography cast:

```sql
SELECT ST_Distance(geometry::geography, ST_SetSRID(ST_MakePoint(<lon>, <lat>), 4326)::geography)
FROM hazard_layers
ORDER BY geometry::geography <-> ST_SetSRID(ST_MakePoint(<lon>, <lat>), 4326)::geography
LIMIT 1;
```

---

## ML Approach

### Input Features

For every risk assessment request, two spatial features are computed from PostGIS:

| Feature | Description |
|---|---|
| `distance_to_nearest_hazard` | Distance in meters from the input point to the nearest hazard polygon. Returns `0.0` if the point is already inside a hazard zone. |
| `overlapping_hazards` | Count of hazard polygons that spatially intersect the input point. |

### Model Selection

Three classifiers were trained and evaluated on a dataset of **2,308 labeled samples** (80/20 train-test split):

| Model | Accuracy |
|---|---|
| Decision Tree | **1.0000** |
| Random Forest | 1.0000 |
| XGBoost | 0.9978 |

**🏆 Winner: Decision Tree (Accuracy: 1.0000)**

### Classification Report (Decision Tree on Test Set, n=462)

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| `high` | 1.00 | 1.00 | 1.00 | 162 |
| `low` | 1.00 | 1.00 | 1.00 | 5 |
| `none` | 1.00 | 1.00 | 1.00 | 295 |
| **accuracy** | | | **1.00** | **462** |
| macro avg | 1.00 | 1.00 | 1.00 | 462 |
| weighted avg | 1.00 | 1.00 | 1.00 | 462 |

### Justification for Decision Tree

Although Random Forest achieved the same accuracy, **Decision Tree was selected as the final model** for the following reasons:

**1. Interpretability for Future NOAH Iterations**
NOAH is a public-facing disaster risk platform where decisions can directly affect evacuation planning, land use policy, and community safety. A Decision Tree produces human-readable rules (e.g., *"if overlapping_hazards >= 1 AND distance = 0, classify as high"*) that domain experts, GIS analysts, and government stakeholders can inspect, validate, and challenge without needing ML expertise. This transparency is critical for building institutional trust and for auditing the model's behavior when edge cases arise.

**2. Ease of Maintenance and Iteration**
Future NOAH development teams can retrain, prune, or extend the Decision Tree as new hazard layers (e.g., earthquake, tsunami) or additional features (e.g., elevation, proximity to waterways) are added — without the black-box complexity of ensemble methods. The tree structure also makes it straightforward to document decision logic in technical reports or regulatory submissions.

**3. Equivalent Performance on This Feature Set**
Given that the two input features (`distance_to_nearest_hazard`, `overlapping_hazards`) are already strong spatial signals derived directly from PostGIS, a single Decision Tree is sufficient to learn clean decision boundaries. The complexity of Random Forest or XGBoost provides no measurable benefit here, while adding inference overhead and reducing explainability.

**4. Perfect Score Caveat**
A 1.0 accuracy on both Decision Tree and Random Forest indicates that the two spatial features are highly deterministic for this dataset — risk labels map cleanly from geometry. This is expected behavior when labels are themselves derived from spatial rules (e.g., hazard level thresholds from NOAH's source data). The model is effectively learning and confirming those spatial relationships, which is the correct and intended behavior for this use case.

### Fallback Rule Engine

If no trained model file is found at `ml_models/risk_model.pkl`, the system automatically falls back to a deterministic rule engine:

| Condition | Risk Level |
|---|---|
| `overlapping_hazards >= 2` | `high` |
| `overlapping_hazards == 1` | `medium` |
| `overlapping_hazards == 0` and `distance <= 100m` | `low` |
| `overlapping_hazards == 0` and `distance > 100m` | `none` |

---

## API Documentation

### Base URL

```
http://localhost:5000/api
```

---

### GET `/api/hazards`

Returns all hazard layers as a GeoJSON FeatureCollection.

**Query Parameters**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `type` | string | No | Filter by hazard type: `flood`, `landslide`, `storm_surge` |

**Response**

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": { "type": "MultiPolygon", "coordinates": [...] },
      "properties": {
        "hazard_type": "flood",
        "hazard_level": "3"
      }
    }
  ],
  "status": "success",
  "count": 1
}
```

---

### POST `/api/risk-assessment`

Assesses the risk level of a given geographic coordinate.

**Validation:** Coordinates must fall within Cebu's bounding box (lat: 9.4–11.3, lon: 123.2–124.1).

**Request Body**

```json
{
  "latitude": 10.3157,
  "longitude": 123.8854
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "risk_level": "medium",
    "features": {
      "distance_to_nearest_hazard": 0.0,
      "overlapping_hazards": 1
    }
  }
}
```

**Error Response (invalid coordinates)**

```json
{
  "success": false,
  "error": "Invalid or non-Cebu coordinates"
}
```

---

## Sample Requests & Responses

### 1. Get All Hazard Layers

```bash
curl -X GET http://localhost:5000/api/hazards
```

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[123.89, 10.31], [123.90, 10.31], [123.90, 10.32], [123.89, 10.32], [123.89, 10.31]]]
      },
      "properties": {
        "hazard_type": "flood",
        "hazard_level": "2"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[123.85, 10.28], [123.86, 10.28], [123.86, 10.29], [123.85, 10.29], [123.85, 10.28]]]
      },
      "properties": {
        "hazard_type": "landslide",
        "hazard_level": "3"
      }
    }
  ],
  "status": "success",
  "count": 2
}
```

---

### 2. Filter by Hazard Type

```bash
curl -X GET "http://localhost:5000/api/hazards?type=flood"
```

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[123.89, 10.31], [123.90, 10.31], [123.90, 10.32], [123.89, 10.32], [123.89, 10.31]]]
      },
      "properties": {
        "hazard_type": "flood",
        "hazard_level": "2"
      }
    }
  ],
  "status": "success",
  "count": 1
}
```

---

### 3. Risk Assessment — Point Inside a Hazard Zone

```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3157, "longitude": 123.8854}'
```

```json
{
  "success": true,
  "data": {
    "risk_level": "high",
    "features": {
      "distance_to_nearest_hazard": 0.0,
      "overlapping_hazards": 2
    }
  }
}
```

---

### 4. Risk Assessment — Point Near but Outside a Hazard Zone

```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.2500, "longitude": 123.7800}'
```

```json
{
  "success": true,
  "data": {
    "risk_level": "low",
    "features": {
      "distance_to_nearest_hazard": 87.3,
      "overlapping_hazards": 0
    }
  }
}
```

---

### 5. Risk Assessment — Point Far from Hazards

```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.8000, "longitude": 123.4000}'
```

```json
{
  "success": true,
  "data": {
    "risk_level": "none",
    "features": {
      "distance_to_nearest_hazard": 4523.1,
      "overlapping_hazards": 0
    }
  }
}
```

---

### 6. Risk Assessment — Invalid Coordinates (Outside Cebu)

```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 14.5995, "longitude": 120.9842}'
```

```json
{
  "success": false,
  "error": "Invalid or non-Cebu coordinates"
}
```

---

## Project Structure

```
NOAH-MOCK-BACKEND/
├── app.py                      # Flask application entry point
├── database.py                 # DB connection and spatial query functions
├── ml_model.py                 # ML model loader and predict_risk function
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not committed)
├── api/
│   ├── hazards.py              # GET /api/hazards endpoint
│   └── risk_assessment.py      # POST /api/risk-assessment endpoint
├── data/
│   └── Cebu.gpkg               # Source GeoPackage (not committed)
├── ml_models/
│   └── risk_model.pkl          # Trained classifier
└── scripts/
    └── ingest_data.py          # GeoPackage to PostGIS ingestion script
```
