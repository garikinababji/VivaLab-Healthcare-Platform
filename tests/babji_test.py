from pathlib import Path

file_path = Path(r"D:\GCP_2026\Hospital Server\Exports\patient_20260718.json")

print("Checking hospital export...")

if file_path.exists():
    print("✅ File Found")
    print(f"File Name : {file_path.name}")
    print(f"Location  : {file_path.parent}")
else:
    print("❌ File Not Found")