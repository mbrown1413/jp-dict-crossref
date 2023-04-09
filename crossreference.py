from typing import List

from dictionaries import Dictionary, Entry, get_dojg_dict, get_hjgp_dict


def crossreference_entry(entry: Entry, dictionaries: List[Dictionary]) -> List[Entry]:
    found_entries = []

    for d in dictionaries:
        if d.name == entry.book:
            continue

        for form in entry.all_forms:
            for found_entry in d.find(form):
                if found_entry not in found_entries:
                    found_entries.append(found_entry)

    return found_entries
