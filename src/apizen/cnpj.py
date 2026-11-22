"""CNPJ helpers that need no network: numeric and alphanumeric (letters in the first twelve
characters since July 2026; a character counts as its ASCII code minus 48)."""

from __future__ import annotations

import re

_FULL = re.compile(r"^[0-9A-Z]{12}[0-9]{2}$")


def clean_cnpj(value: str) -> str:
    """Upper-cases and keeps what a CNPJ may hold: A-Z only in the first 12 places."""
    out = []
    for c in value.upper():
        if len(out) >= 14:
            break
        if c.isdigit() and c.isascii() or ("A" <= c <= "Z" and len(out) < 12):
            out.append(c)
    return "".join(out)


def mask_cnpj(value: str) -> str:
    """00.000.000/0000-00, as far as the value goes."""
    v = clean_cnpj(value)
    parts = [(0, 2, ""), (2, 5, "."), (5, 8, "."), (8, 12, "/"), (12, 14, "-")]
    return "".join(sep + v[a:b] for a, b, sep in parts if len(v) > a).lstrip("./-")


def _check_digit(body: str) -> int:
    total, weight = 0, 2
    for c in reversed(body):
        total += (ord(c) - 48) * weight
        weight = 2 if weight == 9 else weight + 1
    r = total % 11
    return 0 if r < 2 else 11 - r


def is_valid_cnpj(value: str) -> bool:
    """Whether the check digits are right (not whether the company exists: ask the API)."""
    v = clean_cnpj(value)
    if not _FULL.match(v) or len(set(v)) == 1:
        return False
    d1 = _check_digit(v[:12])
    d2 = _check_digit(v[:12] + str(d1))
    return v[12:] == f"{d1}{d2}"
