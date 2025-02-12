import csv
import json
from pathlib import Path

# Load the JSON file
with open(Path("data/cache/distances.json"), "r") as json_file:
    data = json.load(json_file)

# Open the CSV file for writing
with open(Path("data/cache/distances.csv"), "w", newline="") as csv_file:
    fieldnames = ["Subject", "Candidate", "Distance"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write CSV header
    writer.writeheader()

    # Process each subject and its list of distances
    for subject, distances_list in data.items():
        # For each distance record, write the primary and reversed pair (if different)
        for item in distances_list:
            target = item["target"]
            distance = item["distance"]
            writer.writerow({"Subject": subject, "Candidate": target, "Distance": distance})
            if subject != target:
                writer.writerow({"Subject": target, "Candidate": subject, "Distance": distance})
