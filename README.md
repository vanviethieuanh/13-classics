# 13 Classics (十三经)

Extract structured, semantically-annotated data from the **Thirteen Chinese Classics** (十三经) through rule-based NLP pipelines.

## Project Direction

**Goal:** Convert PDF source texts into well-structured JSON datasets, one per classic, enabling research, search, and downstream translation work.

**Scope — the 13 Classics:**

| #   | Classic           | Type                      | Phase |
| --- | ----------------- | ------------------------- | ----- |
| 1   | 周易 (Yijing)     | Divination                | 4     |
| 2   | 尚书 (Shangshu)   | Historical documents      | 5     |
| 3   | 诗经 (Shijing)    | Poetry                    | 3     |
| 4   | 周礼 (Zhouli)     | Ritual / government       | 6     |
| 5   | 仪礼 (Yili)       | Ritual / ceremony         | 6     |
| 6   | 礼记 (Liji)       | Ritual / philosophy       | 6     |
| 7   | 左传 (Zuozhuan)   | Historical narrative      | 7     |
| 8   | 公羊传 (Gongyang) | Commentary / history      | 7     |
| 9   | 谷梁传 (Guliang)  | Commentary / history      | 7     |
| 10  | 论语 (Lunyu)      | Philosophical dialogues   | 1     |
| 11  | 孝经 (Xiaojing)   | Philosophical dialogue    | 1     |
| 12  | 尔雅 (Erya)       | Dictionary / encyclopedia | 4     |
| 13  | 孟子 (Mengzi)     | Philosophical dialogues   | 2     |

**Approach:**

- **Rule-based + classical NLP** — Chinese segmentation via jieba (with custom classical dictionary) + HanLP, combined with hand-crafted extraction rules
- **Per-book pipelines** — each classic has its own pipeline tailored to its text structure
- **Phased delivery** — easiest books first (论语, 孝经), hardest last (三传, 三礼)
- **Unified base schema** — common annotation model (entities, quotes, speakers) with per-book specializations

**Output:** 13 JSON files under `data/structured/`, validated against Pydantic models.

**Tech stack:** Python 3.12, uv, go-task, PyMuPDF, opencc, jieba, HanLP, Pydantic

## Quick Start

```bash
# Install dependencies
uv sync
uv sync --group dev

# Process the first phase (论语 + 孝经)
task phase-1

# Run tests
task test
```

## Project Structure

```
src/
├── cli.py              # Typer CLI entry point
├── config.py           # Global config (paths, settings)
├── extractors/         # Shared utilities (PDF, tokenizer, NER, quotes)
├── models/             # Pydantic output schemas
├── pipelines/          # One pipeline module per classic
└── reference/          # Curated knowledge bases (persons, places, terms)
```

## Task Reference

```bash
task setup              # Install dependencies
task phase-1            # Process phase 1 books
task process-lunyu      # Process single book
task process-all        # Process all 13 books
task validate-all       # Validate outputs
task test               # Run tests
task lint               # Lint code
```
