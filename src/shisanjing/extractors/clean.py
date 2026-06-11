import unicodedata

from opencc import OpenCC

_t2s = OpenCC("t2s")

VN_CHAR_FIX = str.maketrans(
    {
        "\u01a2": "\u01af",  # Ƣ → Ư (capital)
        "\u01a3": "\u01b0",  # ƣ → ư (lowercase)
    }
)

TEXT_FIELDS = ("text", "sino_text", "translation", "commentary")


def normalize_entry(entry: dict) -> dict:
    for field in TEXT_FIELDS:
        val = entry.get(field)
        if not val:
            continue
        val = unicodedata.normalize("NFKC", val)
        val = val.translate(VN_CHAR_FIX)
        if field == "text" or field == "sino_text":
            val = _t2s.convert(val)
        entry[field] = val
    return entry


def normalize_entries(entries: list[dict]) -> list[dict]:
    return [normalize_entry(e) for e in entries]
