from datetime import datetime


class AuditService:

    def __init__(self):

        self.reset()

    def reset(self):

        self.pipeline_name = ""
        self.entity_name = ""
        self.file_name = ""

        self.records_read = 0
        self.valid_records = 0
        self.invalid_records = 0

        self.status = "SUCCESS"

        self.start_time = None
        self.end_time = None

    def start(self):

        self.start_time = datetime.utcnow()

    def end(self):

        self.end_time = datetime.utcnow()

    def execution_time(self):

        if self.start_time and self.end_time:
            return (
                self.end_time - self.start_time
            ).total_seconds()

        return 0

    def summary(self):

        return {

            "pipeline_name": self.pipeline_name,

            "entity_name": self.entity_name,

            "file_name": self.file_name,

            "records_read": self.records_read,

            "valid_records": self.valid_records,

            "invalid_records": self.invalid_records,

            "status": self.status,

            "start_time": self.start_time.isoformat(),

            "end_time": self.end_time.isoformat(),

            "execution_time": self.execution_time()
        }