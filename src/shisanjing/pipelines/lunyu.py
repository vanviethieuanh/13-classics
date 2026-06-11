from shisanjing.pipelines.base import BasePipeline


class LunyuPipeline(BasePipeline):
    book_id = "lunyu"

    def extract_text(self) -> str:
        from shisanjing.extractors.pdf import extract_text

        return extract_text(self.raw_path)

    def parse_structure(self, text: str) -> list[dict]:
        return []

    def annotate(self, structured: list[dict]) -> list[dict]:
        return structured
