import unicodedata

from modelos import Ocorrencia


def _normalizar(texto) -> str:
    if not texto:
        return ""
    base = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in base if not unicodedata.combining(c)).lower()


def classificar(o: Ocorrencia) -> tuple[int, str]:
    """Devolve (prioridade, categoria). Menor prioridade = mais urgente."""
    texto = f"{_normalizar(o.tipo)} {_normalizar(o.descricao)}"
    if "acidente" in texto:
        return 1, "acidente"
    if "obras" in texto:
        return 2, "obras"
    return 3, "normal"