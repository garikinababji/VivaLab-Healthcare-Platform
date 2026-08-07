import json

from vivalab.config.config import BUCKETS
from vivalab.utils.bigquery_helper import BigQueryHelper
from vivalab.utils.exceptions import EmptyFileError
from vivalab.utils.gcs_helper import GCSHelper
from vivalab.utils.pipeline_logger import PipelineLogger


class BaseETL:

    def __init__(self, entity_name):

        self.entity_name = entity_name

        self.gcs = GCSHelper()
        self.bq = BigQueryHelper()
        self.logger = PipelineLogger()

        self.raw_bucket = BUCKETS["raw"]
        self.processed_bucket = BUCKETS["processed"]

        self.raw_prefix = f"{entity_name}_raw/"
        self.processed_prefix = f"{entity_name}_processed/"

    def list_files(self):

        files = self.gcs.list_files(
            self.raw_bucket,
            prefix=self.raw_prefix
        )

        return [
            file
            for file in files
            if file.endswith(".json")
        ]

    def read_json(self, blob_name):

        bucket = self.gcs.client.bucket(self.raw_bucket)
        blob = bucket.blob(blob_name)

        data = blob.download_as_text().strip()

        if not data:
            raise EmptyFileError(f"{blob_name} is empty.")

        if data.startswith("["):
            return json.loads(data)

        return [
            json.loads(line)
            for line in data.splitlines()
            if line.strip()
        ]

    def convert_to_ndjson(self, records):

        return "\n".join(
            json.dumps(record)
            for record in records
        )