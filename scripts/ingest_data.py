import os
import geopandas as gpd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_ingestion():
    # 1. Database Configuration
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'hazard_db')
    
    db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    engine = create_engine(db_url)

    # 2. File Path
    gpkg_path = os.path.join('data', 'Cebu.gpkg')
    
    try:
        if not os.path.exists(gpkg_path):
            logger.error(f"File not found: {gpkg_path}. Ensure you moved Cebu.gpkg to the data/ folder.")
            return

        logger.info(f"Reading GeoPackage file: {gpkg_path}...")
        gdf = gpd.read_file(gpkg_path)
        
        logger.info(f"Columns found in GPKG: {list(gdf.columns)}")

        # --- 3. MAPPING LOGIC (Updated for Colab fixes) ---
        
        # Mapping Hazard Type
        if 'hazard_type' in gdf.columns:
            logger.info("Found 'hazard_type' column.")
            # Column is already named correctly from Colab
        elif 'power_set_class' in gdf.columns:
            gdf['hazard_type'] = gdf['power_set_class']
        else:
            logger.warning("No type column found. Defaulting to 'unclassified'.")
            gdf['hazard_type'] = 'unclassified'
            
        # Mapping Hazard Level (Checking the new name first!)
        if 'hazard_level' in gdf.columns:
            logger.info("Found 'hazard_level' column.")
            # Ensure it is a clean string for the API/Database
            gdf['hazard_level'] = gdf['hazard_level'].fillna('1').astype(str)
        elif 'HAZ' in gdf.columns:
            gdf['hazard_level'] = gdf['HAZ'].fillna(1).astype(int).astype(str)
        elif 'HAZ_numerical' in gdf.columns:
            gdf['hazard_level'] = gdf['HAZ_numerical'].fillna(1).astype(int).astype(str)
        else:
            logger.info("No level data found. Assigning default '1'.")
            gdf['hazard_level'] = '1'

        # --- 4. DATA CLEANUP & PROJECTION ---

        # Subset only the required columns
        gdf_final = gdf[['hazard_type', 'hazard_level', 'geometry']].copy()
        
        # Ensure we are using WGS84 (lat/long) for the web map
        if gdf_final.crs is None or gdf_final.crs.to_epsg() != 4326:
            logger.info("Reprojecting geometries to EPSG:4326...")
            gdf_final = gdf_final.to_crs("EPSG:4326")

        # --- 5. POSTGIS UPLOAD ---

        logger.info(f"Uploading {len(gdf_final)} records to table 'hazard_layers'...")
        
        # 'replace' ensures your DB doesn't get cluttered with old versions
        gdf_final.to_postgis("hazard_layers", engine, if_exists='replace', index=False)
        
        logger.info("✅ Ingestion complete! The database is now updated with the newest levels.")

    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")

if __name__ == '__main__':
    start_ingestion()