import requests

from configuracao import CABECALHOS_MOTIVA, TIMEOUT
from modelos import Ocorrencia, para_numero


def coletar_trecho(nome: str, url: str) -> list[Ocorrencia]:
    rodovia, _, sentido = nome.partition(" - Sentido ")

    resp = requests.get(url, headers=CABECALHOS_MOTIVA, timeout=TIMEOUT)
    resp.raise_for_status()
    itens = resp.json().get("data", {}).get("trafficOccurrences") or []

    resultado = []
    for item in itens:
        coords = item.get("coordinates") or item.get("centralizedCoordinates") or {}
        resultado.append(Ocorrencia(
            concessionaria="Motiva",
            rodovia=rodovia,
            sentido=sentido or None,
            tipo=item.get("reason") or item.get("type"),
            descricao=(item.get("description") or "").strip(),
            latitude=para_numero(coords.get("latitude")),
            longitude=para_numero(coords.get("longitude")),
        ))
    return resultado