from shisanjing.extractors.quotes import extract_quotes, find_speakers


def test_extract_quotes_finds_nothing_in_empty_text():
    assert extract_quotes("") == []


def test_find_speakers_detects_ziyue():
    text = "子曰：学而时习之。"
    speakers = find_speakers(text)
    assert len(speakers) == 1
    assert speakers[0]["speaker"] == "子"
