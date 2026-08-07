from vivalab.utils.logger_messages import LogMessage
from vivalab.utils.constants import PipelineStatus
from vivalab.etl.base_etl import BaseETL
from vivalab.utils.audit_bigquery_service import AuditBigQueryService
from vivalab.utils.audit_service import AuditService
from vivalab.utils.bigquery_service import BigQueryService
from vivalab.utils.gcs_service import GCSService
from vivalab.utils.validator import Validator


class PatientETL(BaseETL):

    def __init__(self):

        super().__init__("patient")

        self.gcs_service = GCSService()
        self.bigquery_service = BigQueryService()

        self.audit = AuditService()
        self.audit_bq = AuditBigQueryService()

    def process_file(self, blob_name):

        self.audit.reset()
        self.audit.start()

        self.audit.pipeline_name = "Patient ETL"
        self.audit.entity_name = self.entity_name
        self.audit.file_name = blob_name

        self.logger.info(f"{LogMessage.FILE_PROCESSING} : {blob_name}")

        try:

            patients = self.read_json(blob_name)

            self.audit.records_read = len(patients)

            self.logger.info(f"{LogMessage.RECORDS_READ} : {len(patients)}")

            valid_records = []
            invalid_records = []

            for patient in patients:

                errors = Validator.validate(patient)

                if errors:
                    patient["errors"] = errors
                    invalid_records.append(patient)
                else:
                    valid_records.append(patient)

            self.audit.valid_records = len(valid_records)
            self.audit.invalid_records = len(invalid_records)

            self.logger.info(f"{LogMessage.VALID_RECORDS} : {len(valid_records)}")
            self.logger.info(f"{LogMessage.INVALID_RECORDS} : {len(invalid_records)}")

            if valid_records:

                valid_ndjson = self.convert_to_ndjson(valid_records)

                processed_blob = self.gcs_service.upload_processed(
                    self.entity_name,
                    blob_name,
                    valid_ndjson
                )

                self.bigquery_service.load_processed_file(
                    processed_blob
                )

            if invalid_records:

                invalid_ndjson = self.convert_to_ndjson(
                    invalid_records
                )

                self.gcs_service.upload_invalid(
                    self.entity_name,
                    blob_name,
                    invalid_ndjson
                )

            self.gcs_service.archive_file(blob_name)

            self.audit.status = PipelineStatus.SUCCESS

        except Exception as e:

            self.logger.error(f"Failed : {blob_name}")
            self.logger.error(str(e))

            self.audit.status = PipelineStatus.FAILED

            self.gcs_service.move_failed_file(blob_name)

        finally:

            self.audit.end()

            self.audit_bq.insert(
                self.audit.summary()
            )

        return self.audit.status == "SUCCESS"

    def run(self):

        files = self.list_files()

        if not files:
            self.logger.warning("No files found.")
            return

        success = 0
        failed = 0

        self.logger.info(f"Total Files : {len(files)}")

        for file in files:

            if self.process_file(file):
                success += 1
            else:
                failed += 1

        self.logger.info("========== PIPELINE SUMMARY ==========")
        self.logger.info(f"Success : {success}")
        self.logger.info(f"Failed  : {failed}")