import re
import csv
from dataclasses import dataclass
from typing import Optional, List, Iterable, Tuple
import unicodedata

from bs4 import BeautifulSoup
from bs4.element import Tag

@dataclass
class Entry:
    concept: str
    all_forms: List[str]
    sub_entry: Optional[int]
    usage: Optional[str]
    english: Optional[str]
    book: str
    volume: Optional[str]
    page: str
    page_count: Optional[int]

    def matches_concept(self, concept: str) -> bool:
        return concept in self.all_forms

class Dictionary:

    def __init__(self, name: str, entries: Iterable[Entry]):
        self.name = name
        self.entries = list(entries)

    def find(self, concept: str) -> List[Entry]:
        return list(filter(
            lambda entry: entry.matches_concept(concept),
            self.entries
        ))

    def on_page(self, page: str) -> List[Entry]:
        return list(filter(
            lambda entry: entry.page == page,
            self.entries
        ))


########## Dictionary of Japanese Grammar ##########

def get_dojg_dict():
    soup = BeautifulSoup(
        unicodedata.normalize(
            "NFKC",
            open("data/dojg.html").read()
        ),
        "html.parser"
    )
    rows = soup.find(id="tablebody").find_all("tr")
    entries = map(extract_dojg_entry, rows)

    #TODO: For now I've only tested the basic volume. Later volumes have other
    #      weird parsing excpetions to manually verify.
    basic_entries = filter(lambda e: e.volume == "basic", entries)

    return Dictionary("dojg", basic_entries)

def extract_dojg_entry(row):
    cells = row.find_all("td")

    # Separate "concept (sub-entry)" from full name
    full_name = row.find("th").text
    match = re.match(r"(.*) \((\d+)\)", full_name)
    if match:
        concept = match.group(1)
        sub_entry = int(match.group(2))
    else:
        concept = full_name
        sub_entry = None

    # English counterpart appears in the last part of the usage text in the div with the "equiv" class.
    english = cells[0].find("div", {"class": "equiv"}).text.replace("\n", "")

    # Get full usage, then subtract english counterpart
    usage = cells[0].text.replace("\n", "")
    assert usage.endswith(english)
    usage = usage[:-len(english)]

    volume = {
        "B": "basic",
        "I": "intermediate",
        "A": "Advanced",
    }[cells[1].text[0]]

    return Entry(
        concept=concept,
        all_forms=parse_dojg_entry_name(concept),
        sub_entry=sub_entry,
        usage=usage,
        english=english,
        book="dojg",
        volume=volume,
        page=cells[1].text,
        page_count=None,
    )

def parse_dojg_entry_name(concept: str) -> List[str]:

    # Exceptions
    #TODO: Exceptions for intermediate and advanced volumes
    if concept == "ことが出来る・できる":
        return [
            "ことが出来る",
            "ことができる"
        ]
    if concept == "も~も":
        return [
            "も~も",
            "も"
        ]

    all_forms = []

    # Split different forms by dot
    for form in concept.split("・"):

        # Consider parts in parethesis optional
        match = re.match(r"(.+)\((.+)\)", form)
        if match:
            all_forms.append(match.group(1))
            all_forms.append(match.group(1)+match.group(2))
        else:
            all_forms.append(form)

    return all_forms


########## Handbook of Japanese Grammar Patterns ##########

def get_hjgp_dict():
    soup = BeautifulSoup(
        unicodedata.normalize(
            "NFKC",
            open("data/hjgp.html").read()
        ),
        "html.parser"
    )
    rows = soup.find(id="tablebody").find_all("tr")
    return Dictionary(
        "hjgp",
        map(extract_hjgp_entry, rows)
    )

def extract_hjgp_entry(row):
    cells = row.find_all("td")

    # Extract page and page count
    match = re.match(r"(\d*) \((\d+)\)", cells[1].text)
    assert match is not None
    page = match.group(1)
    page_count = int(match.group(2))

    sub_entry, all_forms = parse_hjgp_entry_name(row.find("th"))

    return Entry(
        concept=all_forms[0],
        all_forms=all_forms,
        sub_entry=sub_entry,
        usage=None,
        english=None,
        book="hjgp",
        volume=None,
        page=page,
        page_count=page_count,
    )

def parse_hjgp_entry_name(concept_cell: Tag) -> Tuple[Optional[int], List[str]]:
    """
    Returns (sub-entry #, [forms])
    """

    # Cells come in two forms, without and with ruby text:
    #
    #     <a class="form links" data-concept="[kana]" data-id="[entry #]" href="https://core6000.neocities.org/hjgp/entries/[entry #].htm">[kana]</a>
    #
    #     <ruby>
    #         <a class="form links" data-concept="[kanji]" data-id="[entry #]" href="https://core6000.neocities.org/hjgp/entries/[entry #].htm">[kanji]</a>
    #         <rt class="form" data-concept="[kana]" data-id="[entry #]">[kana]</rt>
    #     </ruby>

    all_forms = []

    # Gets the ruby-text if there is ruby
    ruby_tags = concept_cell.find_all("ruby")
    if ruby_tags:
        assert len(ruby_tags) == 1
        all_forms.append(ruby_tags[0].find("rt").text)

    anchor_tag = concept_cell.find("a")

    sub_tag = anchor_tag.find("sub")
    if sub_tag:
        sub_entry = int(sub_tag.text)
        sub_length = len(sub_tag.text)
    else:
        sub_entry = None
        sub_length = 0

    # Gets either kanji if there are ruby tags, or kana if there are none.
    # Here we get the full text then subtract the text in <sub> if we found any
    if sub_length:
        all_forms.append(anchor_tag.text[:-sub_length])
    else:
        all_forms.append(anchor_tag.text)

    return sub_entry, all_forms



########## Dictionary of Japanese Particles ##########

def get_dojp_dict():
    entries = []
    with open("data/dojp.csv", newline="") as f:
        reader = csv.reader(f, skipinitialspace=True)
        assert next(reader) == ["page", "entry"]
        for row in reader:
            page = row[0].strip()

            entry = row[1].strip()
            all_forms = []

            # Split different forms by dot
            for form in entry.split(","):

                # Consider parts in parethesis optional
                match = re.match(r"(.+)\((.+)\)", form)
                if match:
                    all_forms.append(match.group(1))
                    all_forms.append(match.group(1)+match.group(2))
                else:
                    all_forms.append(form)

            entries.append(Entry(
                concept=entry,
                all_forms=all_forms,
                sub_entry=None,
                usage=None,
                english=None,
                book="dojp",
                volume=None,
                page=row[0],
                page_count=None,
            ))

    return Dictionary("dojp", entries)
