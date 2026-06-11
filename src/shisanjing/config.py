from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
STRUCTURED_DIR = DATA_DIR / "structured"

REFERENCE_DIR = Path(__file__).parent / "reference"

BOOK_IDS = [
    "lunyu",
    "xiaojing",
    "mengzi",
    "shijing",
    "yijing",
    "erya",
    "shangshu",
    "zhouli",
    "yili",
    "liji",
    "zuozhuan",
    "gongyang",
    "guliang",
]

BOOK_NAMES: dict[str, str] = {
    "lunyu": "论语",
    "xiaojing": "孝经",
    "mengzi": "孟子",
    "shijing": "诗经",
    "yijing": "周易",
    "erya": "尔雅",
    "shangshu": "尚书",
    "zhouli": "周礼",
    "yili": "仪礼",
    "liji": "礼记",
    "zuozhuan": "左传",
    "gongyang": "公羊传",
    "guliang": "谷梁传",
}

PHASES: dict[str, list[str]] = {
    "1": ["lunyu", "xiaojing"],
    "2": ["mengzi"],
    "3": ["shijing"],
    "4": ["yijing", "erya"],
    "5": ["shangshu"],
    "6": ["zhouli", "yili", "liji"],
    "7": ["zuozhuan", "gongyang", "guliang"],
}
