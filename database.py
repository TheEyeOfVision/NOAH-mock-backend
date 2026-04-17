import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'hazard_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# --- FUNCTION 1: FOR THE MAP (Re-named to avoid collision) ---
def get_hazard_layers(table_name, hazard_type=None):
    """Fetches GeoJSON-ready polygon data from PostGIS for the frontend."""
    conn = get_db_connection()
    if not conn: return []
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = f"SELECT hazard_type, hazard_level, ST_AsGeoJSON(geometry)::json as geometry FROM {table_name}"
        params = ()

        if hazard_type:
            query += " WHERE hazard_type ILIKE %s"
            params = (f"%{hazard_type}%",)

        cur.execute(query + ";", params)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error fetching map layers: {e}")
        return []

# --- FUNCTION 2: FOR THE ML RISK ASSESSMENT (New) ---
def get_spatial_features(lat, lon):
    """Calculates distance to nearest hazard and number of overlapping hazards for a specific point."""
    conn = get_db_connection()
    if not conn: 
        return 0.0, 0
    
    try:
        cur = conn.cursor()
        
        # PostGIS uses ST_MakePoint(longitude, latitude)
        point_sql = "ST_SetSRID(ST_MakePoint(%s, %s), 4326)"
        
        # 1. Count how many hazards overlap this point
        # I am assuming your table is named 'hazard_layers' based on your previous traceback
        overlap_query = f"""
            SELECT COUNT(*) 
            FROM hazard_layers 
            WHERE ST_Intersects(geometry, {point_sql});
        """
        cur.execute(overlap_query, (lon, lat))
        overlaps = cur.fetchone()[0]
        
        # 2. Calculate distance to nearest hazard in meters
        if overlaps > 0:
            # If it's already inside a hazard, distance is 0
            dist = 0.0 
        else:
            # Cast to ::geography to get the distance in actual meters, not degrees
            dist_query = f"""
    SELECT ST_Distance(geometry::geography, {point_sql}::geography) 
    FROM hazard_layers 
    ORDER BY geometry::geography <-> {point_sql}::geography 
    LIMIT 1;
"""
            # We pass lon, lat twice because the point_sql appears twice in the query
            cur.execute(dist_query, (lon, lat, lon, lat))
            result = cur.fetchone()
            dist = result[0] if result else -1.0
            
        cur.close()
        conn.close()
        return dist, overlaps
        
    except Exception as e:
        print(f"Error in spatial calculation: {e}")
        return 0.0, 0