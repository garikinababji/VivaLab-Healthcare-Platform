from google.cloud import bigquery

from vivalab.config.config import (
    PROJECT_ID,
    DATASETS,
    TABLES,
    BUCKETS
)


class BigQueryHelper:

    def __init__(self):

        self.client = bigquery.Client(project=PROJECT_ID)

        self.project_id = PROJECT_ID
        self.dataset = DATASETS["raw"]
        self.table = TABLES["patient"]

        self.processed_bucket = BUCKETS["processed"]

    def get_table_id(self):

        return (
            f"{self.project_id}."
            f"{self.dataset}."
            f"{self.table}"
        )

    def get_gcs_uri(self, blob_name):

        return (
            f"gs://{self.processed_bucket}/{blob_name}"
        )

    def load_to_bigquery(self, blob_name):

        table_id = self.get_table_id()

        gcs_uri = self.get_gcs_uri(blob_name)

        job_config = bigquery.LoadJobConfig(

            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,

            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )

        load_job = self.client.load_table_from_uri(
            gcs_uri,
            table_id,
            job_config=job_config
        )

        load_job.result()

        print(f"Loaded into BigQuery : {table_id}")