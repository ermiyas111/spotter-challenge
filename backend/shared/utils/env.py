import os
from typing import Iterable


def get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value


def get_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def get_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    return float(raw)


def get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    return int(raw)


def get_list(name: str, default: Iterable[str]) -> list[str]:
    raw = os.getenv(name)
    if raw is None:
        return list(default)
    return [item.strip() for item in raw.split(",") if item.strip()]
