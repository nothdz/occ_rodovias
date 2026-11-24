import json

import requests

from configuracao import CABECALHOS_ECOVIAS, TIMEOUT
from modelos import Ocorrencia, para_numero

CONCESSIONARIA = "Ecovias das Gerais"


def _primeiro(item: dict, *chaves):
    """Devolve o primeiro campo preenchido entre os nomes possíveis."""
    for chave in chaves:
        valor = item.get(chave)
        if valor not in (None, ""):
            return valor
    return None


def _converter(rodovia: str, item) -> Ocorrencia:
    if not isinstance(item, dict):  # caso a lista traga só texto
        return Ocorrencia(CONCESSIONARIA, rodovia, None, "Congestionamento",
                          str(item).strip(), None, None)

    descricao = _primeiro(item, "descricao", "descrição", "observacao", "mensagem", "texto")
    if not descricao:
        # ainda não conhecemos o formato: guarda o item inteiro para não perder informação
        descricao = json.dumps(item, ensure_ascii=False)

    km = _primeiro(item, "km", "kmInicial", "marco")
    if km is not None:
        descricao = f"km {km} - {descricao}"

    return Ocorrencia(
        concessionaria=CONCESSIONARIA,
        rodovia=rodovia,
        sentido=_primeiro(item, "sentido"),
        tipo=_primeiro(item, "tipo", "tipoOcorrencia") or "Congestionamento",
        descricao=str(descricao).strip(),
        latitude=para_numero(_primeiro(item, "latitude", "lat")),
        longitude=para_numero(_primeiro(item, "longitude", "lng", "lon")),
    )


def coletar_trecho(nome: str, url: str) -> list[Ocorrencia]:
    resp = requests.get(url, headers=CABECALHOS_ECOVIAS, timeout=TIMEOUT)
    resp.raise_for_status()

    dados = resp.json()
    if isinstance(dados, dict):
        dados = [dados]

    resultado = []
    for rodovia in dados:
        nome_rodovia = rodovia.get("rodovia") or nome
        for item in rodovia.get("listaCongestionamentos") or []:
            resultado.append(_converter(nome_rodovia, item))
    return resultado