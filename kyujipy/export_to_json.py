import cson
import json
import os
import sys

DATA_FILES = [
    "kyujitai_simplified",
    "kyujitai_variants",
    "kakikae_simplified",
    "kakikae_variants",
]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Please give output path as parameter.")

    for data_file in DATA_FILES:
        # Parse database files as CSON
        current_path = os.path.abspath(os.path.dirname(__file__))
        input_cson_path = os.path.join(current_path, "data", data_file + ".cson")

        with open(input_cson_path, "r", encoding="utf-8") as input_cson_file:
            data = cson.load(input_cson_file)

        output_path = os.path.normpath(sys.argv[1])
        output_json_path = os.path.join(output_path, data_file + ".json")

        with open(output_json_path, "w", encoding="utf-8") as output_json_file:
            json.dump(data, output_json_file, ensure_ascii=False)
