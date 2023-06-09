from typing import List, TextIO, Dict
import csv
import re

from dictionaries import Dictionary, Entry, get_dojg_dict, get_hjgp_dict, get_dojp_dict
from crossreference import crossreference_entry


DOJG_COLUMNS = {
    "Concept": "concept",
    "Sub-entry": "sub_entry",
    #"Forms": lambda entry: ', '.join(entry.all_forms),
    #"Book": "book",
    "Volume": "volume",
    "Page": "page",
    #"Page Count": "page_count",
    #"Usage": "usage",
    "English": "english",
}

HJGP_COLUMNS = {
    "Concept": "concept",
    "Sub-entry": "sub_entry",
    #"Forms": lambda entry: ', '.join(entry.all_forms),
    #"Book": "book",
    #"Volume": "volume",
    "Page": "page",
    "Page Count": "page_count",
    #"Usage": "usage",
    #"English": "english",
}

DOJP_COLUMNS = {
    "Concept": "concept",
    #"Sub-entry": "sub_entry",
    #"Forms": lambda entry: ', '.join(entry.all_forms),
    #"Book": "book",
    #"Volume": "volume",
    "Page": "page",
    #"Page Count": "page_count",
    #"Usage": "usage",
    #"English": "english",
}

def generate_csv(dictionary: Dictionary, out_file: TextIO, crossref_dicts: Dict[str, Dictionary], columns):
    writer = csv.writer(out_file)

    # Header
    header = list(columns.keys())
    for dict_name in crossref_dicts:
        if dict_name != dictionary.name:
            header.append(dict_name)
    writer.writerow(header)

    for entry in dictionary.entries:
        row = []
        for column_getter in columns.values():

            if isinstance(column_getter, str):
                row.append(getattr(entry, column_getter))
            else:
                row.append(column_getter(entry))

        for dict_name, d in crossref_dicts.items():
            if dict_name != dictionary.name:
                references = crossreference_entry(entry, [d])
                pages = set(reference.page for reference in references)
                row.append(", ".join(alphanum_sort(pages)))

        writer.writerow(row)

def alphanum_sort(xs):
    """https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python#2669120"""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(xs, key = alphanum_key)

def main():
    all_dicts = {
        "dojg": get_dojg_dict(),
        "hjgp": get_hjgp_dict(),
        "dojp": get_dojp_dict(),
    }

    with open("dojg.csv", "w", newline="") as f:
        generate_csv(all_dicts["dojg"], f, all_dicts, DOJG_COLUMNS)

    with open("hjgp.csv", "w", newline="") as f:
        generate_csv(all_dicts["hjgp"], f, all_dicts, HJGP_COLUMNS)

    with open("dojp.csv", "w", newline="") as f:
        generate_csv(all_dicts["dojp"], f, all_dicts, DOJP_COLUMNS)


if __name__ == "__main__":
    main()
