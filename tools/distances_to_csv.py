import csv
import json
from pathlib import Path

# Load the JSON file
with open(Path("data/cache/distances.json"), "r") as json_file:
    data = json.load(json_file)

# Convert the JSON data to a list of rows
rows = []
for subject, candidates in data.items():
    for candidate in candidates:
        row = (subject, candidate["target"], candidate["distance"])
        rows.append(row)

# Add the symmetric pairs
extra_rows = []
for subject, candidate, distance in rows:
    if subject != candidate and (candidate, subject):
        extra_rows.append((candidate, subject, distance))

# Combine the original rows with the new symmetric ones.
all_rows = rows + extra_rows

# Write the rows to a CSV file.
with open(Path("data/cache/distances.csv"), mode="w", newline="") as f:
    writer = csv.writer(f)
    # Write headers.
    writer.writerow(["Subject", "Candidate", "Distance"])
    # Write each row.
    for row in all_rows:
        writer.writerow(row)
