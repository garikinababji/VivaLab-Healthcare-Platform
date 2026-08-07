from vivalab.utils.gcs_helper import GCSHelper
from vivalab.config.config import BUCKETS

gcs = GCSHelper()

local_file = "sample_data/patient/patient_20260717.json"

destination_blob = "patient_raw/patient_20260717.json"

gcs.upload_file(
    BUCKETS["raw"],
    local_file,
    destination_blob
)