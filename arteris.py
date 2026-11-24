import requests

from configuracao import CABECALHOS_ARTERIS, TIMEOUT
from modelos import Ocorrencia, para_numero


def coletar_trecho(nome: str, url: str) -> list[Ocorrencia]:
    resp = requests.get(url, headers=CABECALHOS_ARTERIS, timeout=TIMEOUT)
    resp.raise_for_status()

    return [
        Ocorrencia(
            concessionaria="Arteris",
            rodovia=nome,
            sentido=item.get("sentido"),
            tipo=item.get("tipo_ocorrencia"),
            descricao=(item.get("descricao") or "").strip(),
            latitude=para_numero(item.get("latitude")),
            longitude=para_numero(item.get("longitude")),
        )
        for item in resp.json().get("trafego") or []
    ]