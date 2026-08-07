from google.cloud import storage
from vivalab.config.config import PROJECT_ID


class GCSHelper:

    def __init__(self):
        self.client = storage.Client(project=PROJECT_ID)

    def upload_file(self, bucket_name, source_file, destination_blob):

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob)

        blob.upload_from_filename(source_file)

        print(f"Uploaded {source_file} to gs://{bucket_name}/{destination_blob}")

    def upload_text(self, bucket_name, destination_blob, content):

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob)

        blob.upload_from_string(
            content,
            content_type="application/json"
        )

        print(f"Uploaded : gs://{bucket_name}/{destination_blob}")

    def download_file(self, bucket_name, source_blob, destination_file):

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob)

        blob.download_to_filename(destination_file)

        print(f"Downloaded {source_blob}")

    def delete_file(self, bucket_name, blob_name):

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()

        print(f"Deleted {blob_name}")

    def move_file(
        self,
        source_bucket,
        source_blob,
        destination_bucket,
        destination_blob
    ):

        source_bucket_obj = self.client.bucket(source_bucket)
        source_blob_obj = source_bucket_obj.blob(source_blob)

        destination_bucket_obj = self.client.bucket(destination_bucket)

        source_bucket_obj.copy_blob(
            source_blob_obj,
            destination_bucket_obj,
            destination_blob
        )

        source_blob_obj.delete()

        print("File moved successfully")

    def list_files(self, bucket_name, prefix=""):

        bucket = self.client.bucket(bucket_name)

        blobs = bucket.list_blobs(prefix=prefix)

        return [blob.name for blob in blobs]