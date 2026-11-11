# CIS-117 Lab3
# Read countries and save a CSV for each region.
# Han Bhone Hset and Leslie Fong
# Group: 3
# Leslie handled reading. Han handled writing.

from pathlib import Path
from csv_reader import readCountryCSV
from csv_writer import writeRegionCSV


def main():
    # folder = Path(__file__).resolve().parent
    folder = Path() # more portable than resolve()
    database = readCountryCSV(str(folder / "country_full.csv"))
    return writeRegionCSV(database, folder / "region_files")


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
