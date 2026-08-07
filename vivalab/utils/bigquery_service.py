from vivalab.utils.bigquery_helper import BigQueryHelper


class BigQueryService:

    def __init__(self):

        self.bq = BigQueryHelper()

    def load_processed_file(self, processed_blob):

        self.bq.load_to_bigquery(processed_blob)