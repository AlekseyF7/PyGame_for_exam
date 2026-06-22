"""Сохранение рекорда и настроек (в JSON-файл)."""

import json
from pathlib import Path


class SaveService:
    def __init__(self, save_path: str) -> None:
        self._path = Path(save_path)

    def load_best_score(self) -> int:
        data = self._read()
        return int(data.get("best_score", 0))

    def save_best_score(self, score: int) -> None:
        data = self._read()
        if score > int(data.get("best_score", 0)):
            data["best_score"] = score
            self._write(data)

    def load_total_coins(self) -> int:
        data = self._read()
        return int(data.get("total_coins", 0))

    def add_coins(self, amount: int) -> int:
        data = self._read()
        total = int(data.get("total_coins", 0)) + max(0, amount)
        data["total_coins"] = total
        self._write(data)
        return total

    def load_volume(self, default: float) -> float:
        data = self._read()
        return float(data.get("volume", default))

    def save_volume(self, volume: float) -> None:
        data = self._read()
        data["volume"] = volume
        self._write(data)

    def _read(self) -> dict:
        if not self._path.exists():
            return {}
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _write(self, data: dict) -> None:
        self._path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
