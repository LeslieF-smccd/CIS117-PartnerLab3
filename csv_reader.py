# CIS-117 Lab3
# Read countries and save a CSV for each region.
# Han Bhone Hset and Leslie Fong
# Group: 3
# Leslie handled reading. Han handled writing.

import csv


class csvRow:

    def __init__(self):
        self.source = ''
        self.row_num = -1
        self.header = ''
        self.vals = []
        self.primary_index = -1
        self.secondary_index = -1
        self.fields = {}

    def __repr__(self):
        safe = self.secondary_index
        return f'csvRow: {self.row_num:3d}: {self.vals[safe:safe + 1]} => {self.source}\n'

class csvDataBase:

    def __init__(self, source=''):
        self.source = source
        self.header = None
        self.raw_header = ''
        self.primary_index = -1
        self.secondary_index = -1
        self.primary_field = ''
        self.secondary_field = ''
        self.csv_store = []
        self.major_fields = {}
        self.minor_dict = {}
        self.major_dict = {}

    def getFieldCSVSingle(self, header_value):
        fly = {}
        if header_value in self.header:
            for csv in self.csv_store:
                fval = csv.fields[header_value]
                if fval in fly:
                    print(f"Warning: duplicate entry found for for field '{header_value}'", csv)
                fly[fval] = csv
        return fly

    def getFieldCSVMulti(self, header_value):
        fly = {}
        if header_value in self.header:
            for csv in self.csv_store:
                fval = csv.fields[header_value]
                if fval not in fly:
                    fly[fval] = [csv]
                else:
                    fly[fval].append(csv)
        return fly

    def getMajorCSV(self, value):
        primary = self.primary_field
        if len(self.major_dict) == 0:
            upd = self.getFieldCSVMulti(primary)
            if len(upd) > 0:
                self.major_dict.update(upd)
        safe = self.major_dict.get(value, None)
        if safe == None or len(safe) < 1:
            return csvRow()
        return safe[-1]

    def __repr__(self):
        return f'csvDataBase for {self.source} holding\n{str(self.csv_store)}\n' + f'majors: {str(self.major_fields)}\nsecondary view: {str(self.minor_dict)}'


def readCountryCSV(file_path="country_full.csv", main_field="name", group_field="region"):
    try:
        with open(file_path, "r", newline="", encoding="utf-8-sig") as input_file:
            lines = input_file.readlines()

        reader = csv.reader(lines, strict=True)
        header = next(reader, None)
        if not header or main_field not in header or group_field not in header:
            raise ValueError("CSV must include the requested name and region columns.")

        database = csvDataBase(str(file_path))
        database.header = header
        database.raw_header = "".join(lines[:reader.line_num]).rstrip("\r\n")
        database.primary_field = main_field
        database.secondary_field = group_field
        database.primary_index = header.index(main_field)
        database.secondary_index = header.index(group_field)
        previous_line = reader.line_num

        for cells in reader:
            source = "".join(lines[previous_line:reader.line_num]).rstrip("\r\n")
            previous_line = reader.line_num
            if not cells:
                continue
            if len(cells) != len(header):
                raise ValueError(f"Wrong number of columns near line {reader.line_num}.")

            row = csvRow()
            row.source = source
            row.row_num = reader.line_num
            row.header = header
            row.vals = cells
            row.primary_index = database.primary_index
            row.secondary_index = database.secondary_index
            row.main_field = main_field
            row.group_field = group_field
            row.fields = dict(zip(header, cells))
            database.csv_store.append(row)

            country = row.fields[main_field]
            region = row.fields[group_field]
            database.major_fields.setdefault(region, []).append(country)
            database.minor_dict.setdefault(region, []).append(row)

        if not database.csv_store:
            raise ValueError("CSV has no country rows.")
        return database

    except FileNotFoundError as error:
        print("Input file not found:", error)
    except PermissionError as error:
        print("Permission denied:", error)
    except OSError as error:
        print("Unable to read input file:", error)
    except (csv.Error, UnicodeError, ValueError) as error:
        print("Invalid CSV data:", error)

    return None
