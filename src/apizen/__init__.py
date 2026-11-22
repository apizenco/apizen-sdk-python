"""SDK oficial das APIs da Apizen: CNPJ e CEP. Só a biblioteca padrão; Python 3.10+.

    from apizen import Apizen
    apizen = Apizen(cnpj_key="sk_cnpj_…")
    empresa = apizen.cnpj("33.000.167/0001-01")  # None when there is none
"""

from .client import Apizen, ApizenError
from .cnpj import clean_cnpj, is_valid_cnpj, mask_cnpj

__all__ = ["Apizen", "ApizenError", "clean_cnpj", "is_valid_cnpj", "mask_cnpj"]
__version__ = "0.1.1"
