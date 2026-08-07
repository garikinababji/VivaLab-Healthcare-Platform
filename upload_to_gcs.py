from pathlib import Path
from google.cloud import storage

# -----------------------------
# Configuration
# -----------------------------
PROJECT_ID = "vivalab-healthcare"
BUCKET_NAME = "vivalab-healthcare-dev-raw"
GCS_FOLDER = "patient_raw"

LOCAL_FILE = Path(
    r"D:\GCP_2026\Hospital Server\Exports\patient_20260718.json"
)

# -----------------------------
# Upload Function
# -----------------------------
def upload_file():

    print("=" * 60)
    print(" VivaLab Hospital File Upload")
    print("=" * 60)

    # Check local file
    if not LOCAL_FILE.exists():
        print("❌ File not found")
        return

    print(f"Local File : {LOCAL_FILE}")

    # Create Storage Client
    client = storage.Client(project=PROJECT_ID)

    bucket = client.bucket(BUCKET_NAME)

    destination_blob = f"{GCS_FOLDER}/{LOCAL_FILE.name}"

    blob = bucket.blob(destination_blob)

    print("\nUploading to GCS...")
    print(f"Bucket : {BUCKET_NAME}")
    print(f"Destination : {destination_blob}")

    blob.upload_from_filename(str(LOCAL_FILE))

    print("\n✅ Upload Successful")
    print(
        f"gs://{BUCKET_NAME}/{destination_blob}"
    )


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    upload_file()