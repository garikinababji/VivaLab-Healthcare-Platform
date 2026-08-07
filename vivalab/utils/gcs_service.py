import os

from vivalab.config.config import BUCKETS
from vivalab.utils.gcs_helper import GCSHelper


class GCSService:

    def __init__(self):

        self.gcs = GCSHelper()

        self.raw_bucket = BUCKETS["raw"]
        self.processed_bucket = BUCKETS["processed"]
        self.archive_bucket = BUCKETS["archive"]
        self.invalid_bucket = BUCKETS["invalid"]

    def upload_processed(self, entity_name, source_blob, ndjson):

        file_name = os.path.basename(source_blob)
        file_name = file_name.replace(".json", ".ndjson")

        destination_blob = (
            f"{entity_name}_processed/{file_name}"
        )

        self.gcs.upload_text(
            self.processed_bucket,
            destination_blob,
            ndjson
        )

        return destination_blob

    def upload_invalid(self, entity_name, source_blob, ndjson):

        file_name = os.path.basename(source_blob)
        file_name = file_name.replace(".json", ".ndjson")

        destination_blob = (
            f"{entity_name}_invalid/{file_name}"
        )

        self.gcs.upload_text(
            self.invalid_bucket,
            destination_blob,
            ndjson
        )

        return destination_blob

    def archive_file(self, source_blob):

        self.gcs.move_file(
            self.raw_bucket,
            source_blob,
            self.archive_bucket,
            source_blob
        )

    # NEW
    def move_failed_file(self, source_blob):

        self.gcs.move_file(
            self.raw_bucket,
            source_blob,
            self.invalid_bucket,
            source_blob
        )