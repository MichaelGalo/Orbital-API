import os
from src.logger import setup_logging
from src.utils import duckdb_con_init, ducklake_init, connection_gcp_credentials
from dotenv import load_dotenv

logger = setup_logging()
load_dotenv()

def setup():
    logger.info("Starting Orbital data lakehouse setup")
    gcp_bucket = os.getenv('GCP_BUCKET_NAME')
    catalog_path = f"gs://{gcp_bucket}/catalog.ducklake"
    data_path = f"gs://{gcp_bucket}/CATALOG_DATA_SNAPSHOTS"

    con = duckdb_con_init()
    ducklake_init(con, data_path, catalog_path)
    connection_gcp_credentials(con)
    con.close()
    logger.info("Remote DuckLake catalog connection established")

if __name__ == "__main__":
    setup()


#TODO: Store the pipeline catalog in GCS and simply access it from here.