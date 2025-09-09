from src.logger import setup_logging
from fastapi import HTTPException
import duckdb
import os
from dotenv import load_dotenv
logger = setup_logging()
load_dotenv()

def duckdb_con_init():
    logger.info("Installing and loading DuckDB extensions")
    duckdb.install_extension("ducklake")
    duckdb.install_extension("httpfs")
    duckdb.load_extension("ducklake")
    duckdb.load_extension("httpfs")
    logger.info("DuckDB extensions loaded successfully")

    con = duckdb.connect(':memory:')
    logger.info("Connected to in-memory DuckDB database")
    return con

def ducklake_init(con, data_path, catalog_path):
    logger.info(f"Attaching DuckLake with data path: {data_path}")
    con.execute(f"ATTACH 'ducklake:{catalog_path}' AS my_ducklake (DATA_PATH '{data_path}')")
    con.execute("USE my_ducklake")
    logger.info("DuckLake attached and activated successfully")

def ducklake_attach_gcp(con):
    logger.info("Configuring GCP settings")
    con.execute(f"SET s3_access_key_id = '{os.getenv('GCP_ACCESS_KEY')}'")
    con.execute(f"SET s3_secret_access_key = '{os.getenv('GCP_SECRET_KEY')}'")
    con.execute(f"SET s3_endpoint = '{os.getenv('GCP_ENDPOINT_URL')}'")
    con.execute("SET s3_use_ssl = true")
    con.execute("SET s3_url_style = 'path'")
    logger.info("GCP configuration completed")

def schema_creation(con):
    logger.info("Creating database schemas")
    con.execute("CREATE SCHEMA IF NOT EXISTS RAW_DATA")
    con.execute("CREATE SCHEMA IF NOT EXISTS RAW")
    con.execute("CREATE SCHEMA IF NOT EXISTS STAGED")
    con.execute("CREATE SCHEMA IF NOT EXISTS CLEANED")
    logger.info("Database schemas created successfully")

DATASET_CONFIG = {
    1: {
        "table_name": "CLEANED.ASTRONAUTS"
    },
    2: {
        "table_name": "CLEANED.NASA_APOD"
    },
    3: {
        "table_name": "CLEANED.NASA_DONKI"
    },
    4: {
        "table_name": "CLEANED.NASA_EXOPLANETS"
    }
}

def fetch_single_dataset(dataset_id, offset, limit):
    try:
        dataset_id = int(dataset_id)
        offset = int(offset)
        limit = int(limit)
        logger.info(f"Fetching dataset {dataset_id} with offset={offset}, limit={limit}")
        
        if dataset_id not in DATASET_CONFIG:
            raise ValueError(f"Invalid dataset_id: {dataset_id}")
        
        dataset = DATASET_CONFIG[dataset_id]
        logger.info(f"Using dataset: {dataset['table_name']}")

        gcp_bucket = os.getenv('GCP_BUCKET_NAME')
        data_path = f"gs://{gcp_bucket}/deployed_ducklake_data_snapshots"
        catalog_path = f"gs://{gcp_bucket}/catalog.ducklake"
        
        con = duckdb_con_init()
        ducklake_init(con, data_path, catalog_path)
        ducklake_attach_gcp(con)

        # Use a fully parameterized query
        query = f"""
            SELECT * FROM {dataset['table_name']}
            OFFSET ?
            LIMIT ?
        """
        logger.info(f"Executing parameterized query on table: {dataset['table_name']}")
        result = con.execute(query, [offset, limit]).fetchall()
        columns = [desc[0] for desc in con.description]

        data = [dict(zip(columns, row)) for row in result]

        logger.info(f"Retrieved {len(data)} records")
        return data
        
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError as ke:
        logger.error(f"KeyError: {ke}")
        raise HTTPException(status_code=404, detail="Dataset not found")
    except Exception as e:
        logger.error(f"Error fetching dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        con.close()


def get_datasets_list():
    result = []
    for dataset_id, config in DATASET_CONFIG.items():
        # Extract the table name and strip the 'CLEANED.' prefix
        stripped_table_name = config["table_name"].split("CLEANED.")[-1]
        
        result.append({
            "id": dataset_id,
            "dataset": stripped_table_name
        })
    return result