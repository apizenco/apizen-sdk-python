import io
import json
import unittest
import urllib.error
from unittest import mock

from apizen import Apizen, ApizenError, clean_cnpj, is_valid_cnpj, mask_cnpj


class Cnpj(unittest.TestCase):
    def test_check_digits(self):
        self.assertTrue(is_valid_cnpj("33.000.167/0001-01"))
        self.assertFalse(is_valid_cnpj("33.000.167/0001-02"))
        self.assertTrue(is_valid_cnpj("12.ABC.345/01DE-35"))
        self.assertFalse(is_valid_cnpj("11.111.111/1111-11"))
        self.assertEqual(clean_cnpj("12.abc.345/01de-35"), "12ABC34501DE35")
        self.assertEqual(mask_cnpj("33000167000101"), "33.000.167/0001-01")


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def http_error(code, body):
    return urllib.error.HTTPError("u", code, "x", {}, io.BytesIO(json.dumps(body).encode()))


class Client(unittest.TestCase):
    def test_cnpj(self):
        with mock.patch("urllib.request.urlopen", return_value=Response(b'{"cnpj": "33000167000101"}')) as m:
            r = Apizen(cnpj_key="sk_cnpj_x").cnpj("33.000.167/0001-01")
        self.assertEqual(r["cnpj"], "33000167000101")
        req = m.call_args[0][0]
        self.assertEqual(req.full_url, "https://cnpj.apizen.com.br/v1/cnpj/33000167000101")
        self.assertEqual(req.get_header("Authorization"), "Bearer sk_cnpj_x")

    def test_not_found_and_errors(self):
        with mock.patch("urllib.request.urlopen", side_effect=http_error(404, {"error": "cep not found"})):
            self.assertIsNone(Apizen(cep_key="k").cep("01001-000"))
        with mock.patch("urllib.request.urlopen", side_effect=http_error(401, {"error": "invalid or revoked key"})):
            with self.assertRaises(ApizenError) as e:
                Apizen(cnpj_key="k").cnpj_nome("33000167000101")
            self.assertEqual(e.exception.status, 401)
        with self.assertRaises(ApizenError):
            Apizen().cep("01001000")


if __name__ == "__main__":
    unittest.main()
