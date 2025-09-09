from src.logger import setup_logging
from src.utils import duckdb_con_init, ducklake_init, ducklake_attach_gcp, schema_creation
import os
from dotenv import load_dotenv
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, ".."))
logger = setup_logging()
load_dotenv()

def setup():
    logger.info("Starting Orbital data lakehouse setup")
    gcp_bucket = os.getenv('GCP_BUCKET_NAME')
    data_path = f"gs://{gcp_bucket}/deployed_ducklake_data_snapshots"
    catalog_path = f"gs://{gcp_bucket}/catalog.ducklake"
    con = duckdb_con_init()
    ducklake_init(con, data_path, catalog_path)
    ducklake_attach_gcp(con)
    schema_creation(con)
    con.close()
    logger.info("Setup completed successfully")

if __name__ == "__main__":
    setup()