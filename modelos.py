from dataclasses import dataclass


@dataclass(frozen=True)  # frozen = hashable, facilita remover duplicados
class Ocorrencia:
    concessionaria: str
    rodovia: str
    sentido: str | None
    tipo: str | None
    descricao: str
    latitude: float | None
    longitude: float | None


def para_numero(valor) -> float | None:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None