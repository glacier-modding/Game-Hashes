import json
import os
import argparse

parser = argparse.ArgumentParser(description="Merge pins JSON files and generates pins.json.", allow_abbrev=False)
parser.add_argument('-o', '--output', type=str, default="pins.json", help="Output file name. Defaults to pins.json.")
args = parser.parse_args()

repositories = [
    "Hitman-Hashes",
    "Bond-Hashes"
]

merged_data = []

for repo in repositories:
    json_file = os.path.join(repo, "pins.json")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

        merged_data.extend(data)

with open(args.output, "w", newline='\n') as f:
    json.dump(list(merged_data), f, indent=2) 