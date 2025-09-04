# gcp_exporter.py (v1.0 - The Imperial Exporter)

import os
import logging
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

# --- साम्राज्यको मस्तिष्कसँग जडान ---
from database_manager import get_db_connection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ImperialExporter")

# --- सम्राटको तयारी ---
# कृपया सुनिश्चित गर्नुहोस् कि तपाईंले 'gcp_secrets.json' फाइल डाउनलोड गर्नुभएको छ
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_secrets.json"

# --- तपाईंको GCP कन्फिगरेसन ---
# कृपया तलको जानकारीलाई आफ्नो GCP प्रोजेक्ट अनुसार बदल्नुहोस्
GCP_PROJECT_ID = "your-gcp-project-id-here"
BIGQUERY_DATASET_NAME = "omega_prime_archives"
BIGQUERY_LOCATION = "US" # e.g., "US", "EU", "asia-east1"

def export_to_bigquery():
    """
    स्थानीय SQLite डाटाबेसबाट सम्पूर्ण ज्ञानलाई Google BigQuery मा सार्छ।
    """
    logger.info(f"👑 साम्राज्यको स्वर्गारोहण सुरु हुँदैछ... BigQuery मा ज्ञान सार्दै।")
    
    # BigQuery क्लाइन्ट प्रारम्भ गर्ने
    try:
        client = bigquery.Client(project=GCP_PROJECT_ID)
    except Exception as e:
        logger.critical(f"FATAL: BigQuery मा जडान हुन सकेन। के तपाईंले 'gcloud auth application-default login' चलाउनुभयो? त्रुटि: {e}")
        return

    # डाटासेट बनाउने (यदि पहिले नै छैन भने)
    dataset_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET_NAME}"
    try:
        client.get_dataset(dataset_id)
        logger.info(f"डाटासेट '{BIGQUERY_DATASET_NAME}' पहिले नै अवस्थित छ।")
    except NotFound:
        logger.info(f"डाटासेट '{BIGQUERY_DATASET_NAME}' बनाउँदै...")
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = BIGQUERY_LOCATION
        client.create_dataset(dataset, timeout=30)
        logger.info("डाटासेट सफलतापूर्वक बनाइयो।")

    # स्थानीय डाटाबेसबाट डाटा पढ्ने
    conn = get_db_connection()
    if not conn: return
    
    tables_to_export = ["coins", "signals", "historical_data"]
    logger.info(f"यी तालिकाहरू निर्यात गरिँदैछ: {tables_to_export}")

    try:
        for table_name in tables_to_export:
            logger.info(f"    - तालिका '{table_name}' को लागि डाटा पढ्दै...")
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            
            if df.empty:
                logger.warning(f"तालिका '{table_name}' खाली छ, छोडिँदैछ।")
                continue

            # BigQuery मा टेबल ID
            table_id = f"{dataset_id}.{table_name}"
            
            logger.info(f"    - '{table_name}' लाई BigQuery मा अपलोड गर्दै...")
            job_config = bigquery.LoadJobConfig(
                # यदि टेबल पहिले नै छ भने, त्यसलाई बदल्ने
                write_disposition="WRITE_TRUNCATE",
            )
            
            job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
            job.result() # काम पूरा हुनको लागि पर्खने
            logger.info(f"    ✅ तालिका '{table_name}' सफलतापूर्वक BigQuery मा सारियो।")

        logger.info("👑👑👑 महान् कार्य सम्पन्न भयो! साम्राज्यको सम्पूर्ण ज्ञान अब Google Cloud मा सुरक्षित छ।")
    
    except Exception as e:
        logger.critical(f"निर्यात प्रक्रियामा एक गम्भीर त्रुटि भयो: {e}", exc_info=True)
    finally:
        conn.close()

if __name__ == "__main__":
    export_to_bigquery()
