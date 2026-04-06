import random
from pathlib import Path

import pandas


class FlashCard:
    """Pure logic: word list management, progress persistence."""

    _SAVED_FILE = "words_to_learn.csv"
    _ORIG_FILE = "french_words.csv"

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._saved_path = data_dir / self._SAVED_FILE
        self._orig_path = data_dir / self._ORIG_FILE
        self._words: list[dict] = self._load()
        self._current: dict = {}

    def _load(self) -> list[dict]:
        try:
            df = pandas.read_csv(self._saved_path)
        except FileNotFoundError:
            df = pandas.read_csv(self._orig_path)
        return df.to_dict(orient="records")

    def next_word(self) -> dict | None:
        """Return a random word dict, or None if the deck is exhausted."""
        if not self._words:
            return None
        self._current = random.choice(self._words)
        return self._current

    def mark_known(self) -> None:
        """Remove the current word from the deck and persist progress."""
        try:
            self._words.remove(self._current)
        except ValueError:
            pass
        pandas.DataFrame(self._words).to_csv(self._saved_path, index=False)

    @property
    def remaining(self) -> int:
        return len(self._words)
