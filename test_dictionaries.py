from typing import List

from dictionaries import Dictionary, get_dojg_dict, get_hjgp_dict

def assert_entry_pages(d: Dictionary, concept: str, expected_pages: List[str]):
    entries = d.find(concept)
    pages = [entry.page for entry in entries]
    assert pages == expected_pages

def test_dojg():
    d = get_dojg_dict()

    # Straight-forward entries
    assert_entry_pages(d, "のだ", ["B. 325"])
    assert_entry_pages(d, "より", ["B. 564", "B. 567"])
    assert_entry_pages(d, "ずつ", ["B. 572"])

    # Concepts with more than one entry differentiated by "(1)", "(2)", etc.
    # あげる (1)
    # あげる (2)
    assert_entry_pages(d, "あげる", ["B. 63", "B. 65"])

    # Dot separating different forms
    # 方・かた
    assert_entry_pages(d, "方", ["B. 183"])
    assert_entry_pages(d, "かた", ["B. 183"])

    # Optional parts in parenthesis
    # か(どうか)
    assert_entry_pages(d, "か", ["B. 164", "B. 166", "B. 168"])
    assert_entry_pages(d, "かどうか", ["B. 168"])

    # Both dot and multiple entries
    # 欲しい・ほしい (1)
    # 欲しい・ほしい (2)
    assert_entry_pages(d, "ほしい", ["B. 144", "B. 146"])
    assert_entry_pages(d, "欲しい", ["B. 144", "B. 146"])

    # Both dot and parenthesis
    # 間・あいだ(に)
    assert_entry_pages(d, "間", ["B. 67"])
    assert_entry_pages(d, "あいだ", ["B. 67"])
    assert_entry_pages(d, "あいだに", ["B. 67"])
    # 為（に）・ため（に）
    assert_entry_pages(d, "為", ["B. 447"])
    assert_entry_pages(d, "為に", ["B. 447"])
    assert_entry_pages(d, "ため", ["B. 447"])
    assert_entry_pages(d, "ために", ["B. 447"])

    # Weird exceptions
    # ことが出来る・できる
    assert_entry_pages(d, "ことが出来る", ["B. 200"])
    assert_entry_pages(d, "ことができる", ["B. 200"])
    # も
    # も~も
    # (this might be debatable, but I figure も should also point ot も~も
    assert_entry_pages(d, "も", ["B. 247", "B. 250", "B. 255"])


def test_hjgp():
    d = get_hjgp_dict()

    # Straight-forward entries
    assert_entry_pages(d, "あえて", ["2"])

    # Furigana
    assert_entry_pages(d, "間", ["1"])
    assert_entry_pages(d, "あいだ", ["1"])
    assert_entry_pages(d, "上げる", ["6"])
    assert_entry_pages(d, "あげる", ["6"])

    # Subscript for multiple entries per concept
    assert_entry_pages(d, "あと", ["7", "9"])
    assert_entry_pages(d, "あと", ["7", "9"])

    # Elipsis
    #TODO

    # Optional parts in parenthesis
    # おいそれと（は）…ない
    #TODO
