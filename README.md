# apizen

SDK oficial das APIs da [Apizen](https://www.apizen.com.br) para Python: CNPJ (Receita Federal, inclusive o CNPJ alfanumérico) e CEP (com código IBGE e coordenadas). Só a biblioteca padrão; Python 3.10+.

```bash
pip install apizen
```

```python
import os
from apizen import Apizen, is_valid_cnpj

apizen = Apizen(cnpj_key=os.environ["CNPJ_API_KEY"], cep_key=os.environ["CEPS_API_KEY"])

is_valid_cnpj("12.ABC.345/01DE-35")  # True: só os dígitos verificadores, sem rede

empresa = apizen.cnpj("33.000.167/0001-01")  # None quando o CNPJ não existe
print(empresa["razao_social"], empresa["ativa"])

nome = apizen.cnpj_nome("33000167000101")  # só os nomes, mais leve

cep = apizen.cep("01001-000")
print(cep["municipio"]["codigo_ibge"], cep["localizacao"])
```

- `cnpj`, `cnpj_nome`, `cep`: o recurso (um `dict`), ou `None` quando não existe (404).
- Outros erros (chave inválida, formato errado) levantam `ApizenError`, com `status`.
- `is_valid_cnpj`, `clean_cnpj`, `mask_cnpj`: CNPJ numérico e alfanumérico, sem rede.

Crie as suas chaves grátis em [apizen.com.br/entrar](https://www.apizen.com.br/entrar). Documentação: [apizen.com.br/docs](https://www.apizen.com.br/docs/inicio).

## Publicar uma versão

Mude `version` no `pyproject.toml` (e `__version__` em `src/apizen/__init__.py`), faça o commit e crie a tag `v<versão>` (`git tag v0.1.1 && git push origin v0.1.1`): o workflow `publish` testa, monta e publica no PyPI.
