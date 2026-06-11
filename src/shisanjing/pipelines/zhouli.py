from shisanjing.pipelines.base import BasePipeline


class ZhouliPipeline(BasePipeline):
    book_id = "zhouli"

    def extract_text(self) -> str:
        from shisanjing.extractors.pdf import extract_text

        return extract_text(self.raw_path)

    def parse_structure(self, text: str) -> list[dict]:
        return []

    def annotate(self, structured: list[dict]) -> list[dict]:
        return structured
