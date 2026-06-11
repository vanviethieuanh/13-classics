# AGENTS.md — Guidelines for AI Agents

## Project Overview

- **Repo:** `13-classics` — Extract structured data from the 13 Chinese Classics
- **Package name:** `shisanjing` (imported as `shisanjing`)
- **Python:** 3.12+, managed with `uv`
- **Task runner:** `go-task` (Taskfile.yml), commands via `task <name>`
- **Entry point:** `shisanjing.cli:app` (Typer CLI)

## Key Conventions

### Dependencies

- Add via `uv add <package>`
- Dev dependencies via `uv add --dev <package>`
- Never edit `uv.lock` manually

### Code style

- Ruff linting + formatting (`task lint`, `task format`)
- Line length: 100
- Target: Python 3.12
- Use type hints everywhere
- Prefer Pydantic v2 models for all data schemas

### Project structure

- `src/shisangjing/` — main package
- `data/raw/` — input PDFs (one per classic)
- `data/interim/` — extracted plain text
- `data/structured/` — final JSON output
- `tests/fixtures/` — manually annotated golden samples

### Pipeline design

- Each classic has its own pipeline module under `pipelines/`
- Pipelines inherit from `pipelines.base.BasePipeline`
- Output schema per classic under `models/<book>.py`
- Shared extraction logic in `extractors/`

### Testing

- pytest in `tests/`
- Golden fixtures in `tests/fixtures/`
- Test each extraction rule against fixtures

## Classical Chinese NLP Notes

- jieba: use custom dictionary built from 13 Classics corpus
- opencc: always convert traditional → simplified
- HanLP (optional dep): classical Chinese models available
- Entity gazetteers in `reference/` (YAML)
- 干支 dates: 60-cycle lookup

## Per-book identifiers (used in CLI, filenames, task names)

```
lunyu, xiaojing, mengzi, shijing, yijing, erya,
shangshu, zhouli, yili, liji,
zuozhuan, gongyang, guliang
```

## Taskfile phases

| Phase | Task           | Books                       |
| ----- | -------------- | --------------------------- |
| 1     | `task phase-1` | lunyu, xiaojing             |
| 2     | `task phase-2` | mengzi                      |
| 3     | `task phase-3` | shijing                     |
| 4     | `task phase-4` | yijing, erya                |
| 5     | `task phase-5` | shangshu                    |
| 6     | `task phase-6` | zhouli, yili, liji          |
| 7     | `task phase-7` | zuozhuan, gongyang, guliang |
