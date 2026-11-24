from concurrent.futures import ThreadPoolExecutor, as_completed

import arteris
import ecovias
import ecovias_norteminas
import motiva
from configuracao import (
    MAX_THREADS,
    TRECHOS_ARTERIS,
    TRECHOS_ECOVIAS,
    TRECHOS_ECOVIAS_NORTEMINAS,
    TRECHOS_MOTIVA,
)
from modelos import Ocorrencia


def coletar_tudo() -> list[Ocorrencia]:
    tarefas = (
        [(motiva.coletar_trecho, n, u) for n, u in TRECHOS_MOTIVA.items()]
        + [(arteris.coletar_trecho, n, u) for n, u in TRECHOS_ARTERIS.items()]
        + [(ecovias.coletar_trecho, n, u) for n, u in TRECHOS_ECOVIAS.items()]
        + [(ecovias_norteminas.coletar_trecho, n, u) for n, u in TRECHOS_ECOVIAS_NORTEMINAS.items()]
    )

    ocorrencias: list[Ocorrencia] = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futuros = {executor.submit(f, n, u): n for f, n, u in tarefas}
        for futuro in as_completed(futuros):
            try:
                ocorrencias.extend(futuro.result())
            except Exception as erro:  # um trecho falhar não derruba os outros
                print(f"[{futuros[futuro]}] falhou: {erro}")

    return list(dict.fromkeys(ocorrencias))  # remove duplicados mantendo a ordem