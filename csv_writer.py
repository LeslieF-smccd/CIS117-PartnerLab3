# CIS-117 Lab3
# Save countries into separate CSV files by region.
# Han Bhone Hset
# Group:3
# Partner: Leslie Fong
# Leslie handled reading. I handled writing.

import csv
from pathlib import Path


def writeRegionCSV(database, output_folder="region_files"):
    if database is None:
        print("No country data available to write.")
        return False

    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)

        for region, countries in database.major_fields.items():
            filename = region if region else "Unknown"

            if any(character in filename for character in '/\\:*?"<>|'):
                print("Invalid region name. Check the reading code:", region)
                return False

            with open(
                folder / (filename + ".csv"),
                "w",
                newline="",
                encoding="utf-8"
            ) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(["name", "region"])

                for country in countries:
                    writer.writerow([country, region])

        print("Region files saved in:", folder)
        return True

    except PermissionError as error:
        print("Permission denied:", error)
    except FileNotFoundError as error:
        print("Output path not found:", error)
    except OSError as error:
        print("Unable to write output files:", error)

    return False
