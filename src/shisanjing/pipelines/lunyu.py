import re

from shisanjing.pipelines.base import BasePipeline

RE_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
RE_SECNUM = re.compile(r"^(\d+)[\.\u00b7](\d+)\s*$")
RE_PAGE_HDR = re.compile(
    r"^(Luận Ngữ|www\.vietnamvanhien|MỤC LỤC|LỜI NÓI ĐẦU"
    r"|BÀI TẬP|PHỤ LỤC|TÀI LIỆU|TÀI LIỆU THAM KHẢO)"
)
RE_SECTION_FOOTER = re.compile(r"Hết thiên")
RE_CHAP_ORD = re.compile(r"第([一二三四五六七八九十亓]+)篇")

CN_ORD: dict[str, int] = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "亓": 5,
}

CHAPTER_NAMES: list[str] = [
    "学而",
    "为政",
    "八佾",
    "里仁",
    "公冶长",
    "雍也",
    "述而",
    "泰伯",
    "子罕",
    "乡党",
    "先进",
    "颜渊",
    "子路",
    "宪问",
    "卫灵公",
    "季氏",
    "阳货",
    "微子",
    "子张",
    "尧曰",
]

SPEAKER_MAP: dict[str, str] = {
    "子": "孔子",
    "孔子": "孔子",
    "有子": "有子",
    "曾子": "曾子",
    "子夏": "子夏",
    "子贡": "子贡",
    "子张": "子张",
    "子游": "子游",
    "哀公": "鲁哀公",
    "季康子": "季康子",
    "宪": "原宪",
}
_SPEAKERS_PAT = re.compile("^(" + "|".join(re.escape(s) for s in SPEAKER_MAP) + r")曰[：:]?")


def _is_chinese(text: str) -> bool:
    stripped = text.strip().replace(" ", "").replace("　", "")
    if not stripped:
        return False
    cjk = sum(1 for c in stripped if RE_CJK.match(c))
    return cjk / len(stripped) > 0.4


def _is_vietnamese(text: str) -> bool:
    stripped = text.strip()
    if not stripped or stripped.isdigit():
        return False
    if _is_chinese(stripped):
        return False
    # Has Vietnamese diacritics or Latin + Vietnamese-specific chars
    vn = sum(1 for c in stripped if ord(c) > 127 and not RE_CJK.match(c))
    latin = sum(1 for c in stripped if c.isascii() and c.isalpha())
    return vn > 0 or latin > 0


def _has_vietnamese_header(text: str) -> bool:
    return bool(RE_PAGE_HDR.search(text)) or text.strip().isdigit()


def _classify_vn_line(line: str, prev_type: str | None = None) -> str | None:
    if not _is_vietnamese(line):
        return None
    if line.startswith("(Chú thích:") or line.startswith("(Lời bàn:"):
        return "notes"
    if " viết:" in line or line.startswith("Tử viết:") or "viết:" in line[:20]:
        return "sino"
    if " nói:" in line or line.startswith("Tử nói:") or "nói:" in line[:20]:
        return "trans"
    return prev_type


def _clean_chinese_text(text: str) -> str:
    text = re.sub(r"\b[A-Z]{2,}\b", "", text)
    text = re.sub(r"\s+", "", text)
    text = text.replace("?", "？").replace(":", "：").replace(",", "，")
    text = text.replace(";", "；")
    return text.strip()


def _extract_speaker(text: str) -> str | None:
    m = _SPEAKERS_PAT.match(text.strip())
    if m:
        raw = m.group(1).strip()
        return SPEAKER_MAP.get(raw, raw)
    return None


def _strip_speaker_prefix(text: str) -> str:
    m = _SPEAKERS_PAT.match(text.strip())
    if m:
        return text.strip()[m.end() :].strip()
    return text.strip()


def _parse_ordinal(ord_str: str) -> int | None:
    if ord_str in CN_ORD:
        return CN_ORD[ord_str]
    if ord_str.startswith("十"):
        rest = ord_str[1:]
        if rest in CN_ORD:
            return 10 + CN_ORD[rest]
        return 10
    if len(ord_str) == 2 and ord_str[1] == "十":
        tens = CN_ORD.get(ord_str[0], 0)
        return tens * 10 if tens else None
    return None


class LunyuPipeline(BasePipeline):
    book_id = "lunyu"

    def extract_text(self) -> str:
        from shisanjing.extractors.pdf import extract_text

        return extract_text(self.raw_path)

    def parse_structure(self, text: str) -> list[dict]:
        lines = text.split("\n")
        chapters: list[dict] = []
        current_chapter: dict | None = None
        current_section: dict | None = None
        zh_buffer: list[str] = []
        vn_scratch: list[str] = []

        def flush_section():
            nonlocal current_section, zh_buffer, vn_scratch
            if current_section is None:
                return
            zh_raw = "".join(zh_buffer)
            zh_text = _clean_chinese_text(zh_raw)
            if len(zh_text) > 5:
                zh_text = _strip_speaker_prefix(zh_text)
                current_section["text"] = zh_text
                current_section["speaker"] = _extract_speaker(zh_raw)
                # Classify Vietnamese lines
                sino = []
                trans = []
                notes = []
                prev = None
                for ln in vn_scratch:
                    t = _classify_vn_line(ln, prev)
                    if t == "sino":
                        sino.append(ln)
                    elif t == "trans":
                        trans.append(ln)
                    elif t == "notes":
                        notes.append(ln)
                    prev = t
                if sino:
                    current_section["sino_text"] = " ".join(sino)
                if trans:
                    current_section["translation"] = " ".join(trans)
                if notes:
                    current_section["commentary"] = " ".join(notes)
                if current_chapter is not None:
                    current_chapter["sections"].append(current_section)
            current_section = None
            zh_buffer = []
            vn_scratch = []

        for line in lines:
            stripped = line.strip()
            if not stripped or _has_vietnamese_header(stripped):
                continue
            if RE_SECTION_FOOTER.search(stripped):
                flush_section()
                current_chapter = None
                continue

            m = RE_CHAP_ORD.search(stripped)
            if m:
                flush_section()
                ch_num = _parse_ordinal(m.group(1))
                if ch_num and 1 <= ch_num <= 20:
                    ch_name = (
                        CHAPTER_NAMES[ch_num - 1] if ch_num <= len(CHAPTER_NAMES) else f"篇{ch_num}"
                    )
                    current_chapter = {
                        "chapter_number": ch_num,
                        "chapter_name": ch_name,
                        "sections": [],
                    }
                    chapters.append(current_chapter)
                    continue

            m = RE_SECNUM.match(stripped)
            if m:
                flush_section()
                current_section = {
                    "section": stripped,
                    "text": "",
                    "speaker": None,
                    "sino_text": None,
                    "translation": None,
                    "commentary": None,
                }
                zh_buffer = []
                vn_scratch = []
                continue

            if current_section is None and current_chapter is not None:
                if _is_chinese(stripped):
                    current_section = {
                        "section": None,
                        "text": "",
                        "speaker": None,
                        "sino_text": None,
                        "translation": None,
                        "commentary": None,
                    }
                    zh_buffer = []
                    vn_scratch = []

            if current_section is not None:
                if _is_chinese(stripped):
                    zh_buffer.append(stripped)
                elif _is_vietnamese(stripped):
                    vn_scratch.append(stripped)

        flush_section()
        return chapters

    def annotate(self, structured: list[dict]) -> list[dict]:
        from shisanjing.extractors.clean import normalize_entries

        results: list[dict] = []
        for ch in structured:
            for sec in ch.get("sections", []):
                if not sec.get("text"):
                    continue
                entry = {
                    "book": self.book_id,
                    "chapter": f"{ch['chapter_number']:02d} {ch['chapter_name']}",
                    "section": sec.get("section"),
                    "text": sec["text"],
                    "speaker": sec.get("speaker"),
                    "sino_text": sec.get("sino_text"),
                    "translation": sec.get("translation"),
                    "commentary": sec.get("commentary"),
                    "entities": [],
                    "quotes": [],
                    "tokens": [],
                    "notes": [],
                }
                results.append(entry)
        return normalize_entries(results)
