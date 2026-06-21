import os
import json
import hashlib
from enum import Enum

GAME_FLAGS_HITMAN = {
    "alphaJuly2015": 0b00000001,
    "h1": 0b00000010,
    "h2": 0b00000100,
    "h3": 0b00001000,
    "beta": 0b00010000,
    "sa": 0b00100000,
    "unknown": 0b01000000,
    "alphaJan2015": 0b10000000
}

GAME_FLAGS_BOND = {
    "FirstLight": 0b00000001
}

COMBINED_FLAGS = {
    **GAME_FLAGS_HITMAN,
    "FirstLight": 0b100000000,
}

class PlatformTag(Enum):
    Undefined = 0
    Pc = 1
    Ps5 = 2
    Scarlett = 3 # Xbox series X/S
    Ounce = 4 # Nintendo Switch 2

def ioi_hash(string, platform: PlatformTag = PlatformTag.Undefined):
    md5Result = hashlib.md5(string.encode("utf-8").lower()).hexdigest().upper()
    return f"{platform.value:02x}{md5Result[2:16]}"

def infer_type(hash_with_type):
    parts = hash_with_type.split('.')
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], None

def find_type(hash_val, all_data):
    for hash_type, data in all_data.items():
        if hash_val in data:
            return hash_type
    return None

def read_json_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            entries = json.load(f)
            return {entry["hash"]: entry for entry in entries}
    return {}

def write_json_file(filename, data):
    with open(filename, 'w', newline='\n') as f:
        json.dump(list(data.values()), f, indent=2)