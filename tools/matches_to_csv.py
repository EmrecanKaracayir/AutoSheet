import csv
import json
from pathlib import Path

# Load the JSON file
with open(Path("data/cache/matches.json"), "r") as json_file:
    data = json.load(json_file)

# Extract the union of all target names.
all_targets = set()
for subject, candidate_list in data.items():
    for candidate in candidate_list:
        all_targets.add(candidate["target"])

# Option 1: sort alphabetically (you could also define a custom order if needed).
all_targets = sorted(all_targets)

# Create the CSV header row.
header = ["Subject"] + all_targets

# Prepare CSV rows.
rows = []
for subject, candidate_list in data.items():
    # Map each target to its corresponding distance for the current subject.
    distances = {item["target"]: item["distance"] for item in candidate_list}
    # Build a row starting with the subject, then add distances in the order specified by header.
    row = [subject]
    for target in all_targets:
        # Insert the distance if exists; otherwise, leave the cell empty.
        row.append(distances.get(target, ""))
    rows.append(row)

# Write rows to CSV.
with open("data/cache/matches.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)
  