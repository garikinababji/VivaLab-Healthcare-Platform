from google.cloud import bigquery

from vivalab.config.config import PROJECT_ID, DATASETS


class AuditBigQueryService:

    def __init__(self):

        self.client = bigquery.Client(project=PROJECT_ID)

        self.table_id = (
            f"{PROJECT_ID}."
            f"{DATASETS['metadata']}."
            "pipeline_audit"
        )

    def insert(self, audit_record):

        print("\n========== AUDIT RECORD ==========")
        print(audit_record)

        errors = self.client.insert_rows_json(
            self.table_id,
            [audit_record]
        )

        if errors:

            print("INSERT FAILED")
            print(errors)

            raise Exception(errors)

        print("AUDIT INSERT SUCCESS")