"""The Apizen APIs over HTTPS. Secret keys: use this on a server."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Any, Dict, Optional
from urllib.parse import quote

CNPJ_URL = "https://cnpj.apizen.com.br"
CEP_URL = "https://ceps.apizen.com.br"


class ApizenError(Exception):
    """An answer other than 200 or 404: 400 (bad input), 401 (the key), 5xx."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


class Apizen:
    def __init__(
        self,
        cnpj_key: Optional[str] = None,
        cep_key: Optional[str] = None,
        timeout: float = 15.0,
        cnpj_url: str = CNPJ_URL,
        cep_url: str = CEP_URL,
    ):
        self.cnpj_key, self.cep_key, self.timeout = cnpj_key, cep_key, timeout
        self.cnpj_url, self.cep_url = cnpj_url.rstrip("/"), cep_url.rstrip("/")

    def cnpj(self, cnpj: str) -> Optional[Dict[str, Any]]:
        """An establishment's record, or None when the CNPJ is not in the Receita's data."""
        return self._get(self.cnpj_url, self.cnpj_key, "cnpj_key", f"/v1/cnpj/{self._cnpj(cnpj)}")

    def cnpj_nome(self, cnpj: str) -> Optional[Dict[str, Any]]:
        """Only the company's names: lighter, to check whose a CNPJ is."""
        return self._get(self.cnpj_url, self.cnpj_key, "cnpj_key", f"/v1/cnpj/{self._cnpj(cnpj)}/nome")

    def cep(self, cep: str) -> Optional[Dict[str, Any]]:
        """A CEP's address, with the town's IBGE code and a point; None when there is none."""
        digits = quote(re.sub(r"\D", "", cep))
        return self._get(self.cep_url, self.cep_key, "cep_key", f"/v1/cep/{digits}")

    @staticmethod
    def _cnpj(cnpj: str) -> str:
        return quote(re.sub(r"[./\s-]", "", cnpj).upper())

    def _get(self, base: str, key: Optional[str], name: str, path: str) -> Optional[Dict[str, Any]]:
        if not key:
            raise ApizenError(401, f"Apizen: set {name}")
        req = urllib.request.Request(
            base + path, headers={"Authorization": f"Bearer {key}", "Accept": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            try:
                message = json.loads(e.read().decode("utf-8")).get("error", f"HTTP {e.code}")
            except (ValueError, AttributeError):
                message = f"HTTP {e.code}"
            raise ApizenError(e.code, message) from None
