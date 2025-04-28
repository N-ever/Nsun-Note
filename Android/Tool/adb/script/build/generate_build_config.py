import os
import sys
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from build import BuildConfig, TMP_DIR

parser = argparse.ArgumentParser(description='This is a script for generate config.')
parser.add_argument('--name', help='Project name.')

def ensure_dir():
    print("Ensure tmp dir:", TMP_DIR)
    os.makedirs(TMP_DIR, exist_ok=True)

def generate_config(name):
    config = BuildConfig()
    config.dir = os.getcwd()
    file_name = os.path.join(TMP_DIR, "{}.json".format(name))
    with open(file_name, "w") as f:
        f.write(config.to_json())


def main(args):
    ensure_dir()
    generate_config(args.name)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
