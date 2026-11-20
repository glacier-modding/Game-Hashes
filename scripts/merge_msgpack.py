import json, os, argparse, brotli, time, msgpack
from newsmile import SmileEncoder
from compression import zstd
from common import GAME_FLAGS_BOND, COMBINED_FLAGS, repositories

parser = argparse.ArgumentParser(description="Merge JSON files and generate a hash list in MessagePack binary format.", allow_abbrev=False)
parser.add_argument('version', type=int, help="Current version number to be embedded in the hash list.")
parser.add_argument('-o', '--output', type=str, default="hash_list.msgpack", help="Output MessagePack binary file name. Defaults to hash_list.msgpack.")
args = parser.parse_args()

input_directory = "paths"

merged_data = {}

for repo in repositories:
    input_directory = os.path.join(repo, "paths")

    json_files = [
        os.path.join(input_directory, f)
        for f in sorted(os.listdir(input_directory))
        if f.endswith(".json")
    ]

    for json_file in json_files:
        with open(json_file, "r") as f:
            data = json.load(f)
            resource_type = os.path.basename(json_file).split('.')[0]

        for entry in data:
            if "Bond-Hashes" in repo:
                if entry["gameFlags"] & GAME_FLAGS_BOND["FirstLight"]:
                    entry["gameFlags"] = COMBINED_FLAGS["FirstLight"]
            merged_data[entry['hash']] = {
                'resourceType': resource_type,
                'path': entry.get('path', ''),
                'hint': entry.get('hint', ''),
                'gameFlags': entry['gameFlags']
            }

packed_data = msgpack.packb(merged_data)

with open(args.output, "wb") as f:
    f.write(zstd.compress(packed_data, level=9))

print(f"Hash list merged and written in MessagePack binary format successfully!")
