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


def main():
    dojg = get_dojg_dict()
    hjgp = get_hjgp_dict()

    main_dict = dojg
    other_dicts = [
        hjgp,
    ]

    for entry in dojg.entries:
        print(entry.concept)
        for ref in crossreference_entry(entry, other_dicts):
            print(f"    {entry.book}: {ref.concept} p.{ref.page}")

    print(hjgp.on_page("347"))
    print(dojg.find("時"))
    print(dojg.find("時"))
    print(list(crossreference_entry(dojg.find("時")[0], other_dicts)))


if __name__ == "__main__":
    main()
