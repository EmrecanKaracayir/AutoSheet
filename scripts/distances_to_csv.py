import csv
import json
from pathlib import Path

# Load the JSON file
with open(Path("data/distances.json"), "r") as json_file:
    data = json.load(json_file)

    # Open the CSV file for writing
with open(Path("data/distances.csv"), "w", newline="") as csv_file:
    fieldnames = ["char1", "char2", "distance"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write CSV Header
    writer.writeheader()

    # Process each JSON key-value pair
    for key, distance in data.items():
        # Expect keys in the format "A_B"
        try:
            char1, char2 = key.split("_")
        except ValueError:
            print(f"Skipping invalid key: {key}")
            continue

        # Write the primary pair
        writer.writerow({"char1": char1, "char2": char2, "distance": distance})

        # Write the reversed pair if characters are different
        if char1 != char2:
            writer.writerow({"char1": char2, "char2": char1, "distance": distance})
