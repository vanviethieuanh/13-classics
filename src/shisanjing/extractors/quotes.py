import re

QUOTE_PATTERNS: list[re.Pattern] = [
    re.compile(r"「[^」]+」"),
    re.compile(r"『[^』]+』"),
    re.compile(r"《[^》]+》"),
]

SPEECH_TAG = re.compile(r"(?P<speaker>[^曰]+)曰")


def extract_quotes(text: str) -> list[dict]:
    """Extract quoted passages and their speakers."""
    results: list[dict] = []
    for pattern in QUOTE_PATTERNS:
        for match in pattern.finditer(text):
            results.append(
                {
                    "text": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                }
            )
    return results


def find_speakers(text: str) -> list[dict]:
    """Find speaker attribution patterns (e.g., 子曰, 孟子曰)."""
    results: list[dict] = []
    for match in SPEECH_TAG.finditer(text):
        results.append(
            {
                "speaker": match.group("speaker"),
                "start": match.start(),
                "end": match.end(),
            }
        )
    return results
