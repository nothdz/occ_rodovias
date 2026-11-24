import html
import re
import time
import unicodedata

import requests

from configuracao import CABECALHOS_ECOVIAS_NORTEMINAS, TIMEOUT_ECOVIAS_NORTEMINAS
from modelos import Ocorrencia, para_numero

TENTATIVAS = 3

# Sem motivo (Reason) e com situação deste tipo = pista normal: não vira ocorrência.
PALAVRAS_NORMAIS = ("normal", "free", "open", "fluid", "livre", "fluido", "liberado")

# O site devolve a situação em inglês; aqui ficam as traduções já conhecidas.
# Valores novos aparecem em inglês até serem incluídos aqui.
SITUACOES = {
    "interdicted": "interditado",
}


def _texto(valor) -> str | None:
    """O campo pode vir como texto ou como objeto {ID, Name}; devolve sempre texto limpo."""
    if isinstance(valor, dict):
        valor = valor.get("Name") or valor.get("Description")
    if valor in (None, ""):
        return None
    limpo = html.unescape(re.sub(r"<[^>]+>", " ", str(valor)))
    return " ".join(limpo.split()) or None


def _sem_acento(texto: str) -> str:
    base = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in base if not unicodedata.combining(c)).lower()


def _parece_normal(situacao: str) -> bool:
    texto = _sem_acento(situacao)
    return any(palavra in texto for palavra in PALAVRAS_NORMAIS)


def _formatar_km(valor: float) -> str:
    return f"{valor:g}".replace(".", ",")


def _trecho_km(cond: dict) -> str | None:
    inicial = para_numero(cond.get("InitialKM"))
    final = para_numero(cond.get("FinalKM"))
    if inicial is None or final is None:
        return None
    if inicial == final:
        return f"Km {_formatar_km(inicial)}"
    return f"Km {_formatar_km(inicial)} ao {_formatar_km(final)}"


def _converter(concessionaria: str, rodovia: str, cond: dict) -> Ocorrencia | None:
    motivo = _texto(cond.get("Reason"))                 # ex.: ACIDENTE
    situacao_original = _texto(cond.get("ConditionText"))  # ex.: Interdicted
    situacao = SITUACOES.get((situacao_original or "").lower(), situacao_original)

    # condição geral da via (sem motivo e normal): não é ocorrência
    if not motivo and (not situacao_original or _parece_normal(situacao_original)):
        return None

    tipo = (motivo or situacao).capitalize()

    partes = []
    local = _texto(cond.get("Location"))                # ex.: PISTA
    if local:
        partes.append(f"Local: {local.lower()}.")
    if situacao:
        partes.append(f"Situação: {situacao.lower()}.")
    km = _trecho_km(cond)
    if km:
        partes.append(f"{km}.")

    return Ocorrencia(
        concessionaria=concessionaria,
        rodovia=rodovia,
        sentido=_texto(cond.get("Direction")),          # objeto -> pega o Name
        tipo=tipo,
        descricao=" ".join(partes) or "Sem detalhes.",
        latitude=None,
        longitude=None,
    )


def _baixar(url: str) -> dict:
    """Tenta algumas vezes se o site demorar ou a conexão cair."""
    ultimo_erro = None
    for _ in range(TENTATIVAS):
        try:
            resp = requests.get(url, headers=CABECALHOS_ECOVIAS_NORTEMINAS,
                                timeout=TIMEOUT_ECOVIAS_NORTEMINAS)
            resp.raise_for_status()
            return resp.json()
        except (requests.Timeout, requests.ConnectionError) as erro:
            ultimo_erro = erro
            time.sleep(2)
    raise ultimo_erro


def coletar_trecho(nome: str, url: str) -> list[Ocorrencia]:
    dados = _baixar(url)
    estradas = (dados.get("TrafficCondition") or {}).get("Roads") or []

    resultado = []
    for estrada in estradas:
        via = estrada.get("Road") or {}
        concessionaria = _texto((via.get("Concessionaire") or {}).get("Name")) or nome

        codigo = _texto(via.get("Name"))              # ex.: BR 135
        exibicao = _texto(via.get("DisplayName"))     # ex.: Rodovia Guimarães Rosa
        rodovia = f"{exibicao} ({codigo})" if codigo and exibicao else (exibicao or codigo or nome)

        for cond in estrada.get("Conditions") or []:
            ocorrencia = _converter(concessionaria, rodovia, cond)
            if ocorrencia:
                resultado.append(ocorrencia)
    return resultado