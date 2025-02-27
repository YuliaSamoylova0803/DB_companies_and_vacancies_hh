from pathlib import Path

BASE_DIR = Path(__file__).parent

json_filename = Path(BASE_DIR, "data", "employers_data.json").parent

database_path = Path(BASE_DIR, "src", "database.ini").parent

print(database_path)
print(json_filename)