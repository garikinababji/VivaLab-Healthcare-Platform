from vivalab.utils.gcs_helper import GCSHelper
from vivalab.config.config import BUCKETS

gcs = GCSHelper()

files = gcs.list_files(BUCKETS["raw"])

print(files)
