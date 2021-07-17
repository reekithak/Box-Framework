import argparse
import os
import sys
import re


def process(filename):
    """Removes empty lines and lines that contain only whitespace, and
    lines with comments"""

    with open(filename) as in_file, open(filename, "r+") as out_file:
        for line in in_file:
            if re.match("# In\[[0-9\\d+\]]", line):
                out_file.write("\n")
            else:
                out_file.writelines(line)


if __name__ == "__main__":

    my_parser = argparse.ArgumentParser(
        description="Removing the In#\[[0-9\d+\]] in notebook to script conversion"
    )

    my_parser.add_argument(
        "script_path",
        metavar="path",
        type=str,
        help="path to script that requires a conversion",
    )

    args = my_parser.parse_args()
    script_path = args.script_path

    file_format = script_path.split(".")[1]
    if file_format != "py":
        print("File is not a py file")
        sys.exit()

    try:
        print(f"processing : {script_path}")
        process(script_path)
    except FileNotFoundError:
        print("Please provide path correctly")