import json
import os
from dataclasses import asdict
from datetime import datetime

from classificacao import classificar
from modelos import Ocorrencia
from datetime import datetime, timedelta, timezone

BRASILIA = timezone(timedelta(hours=-3))

def gravar_json(ocorrencias: list[Ocorrencia], caminho: str) -> None:
    itens = []
    for o in ocorrencias:
        prioridade, categoria = classificar(o)
        itens.append({**asdict(o), "prioridade": prioridade, "categoria": categoria})
    itens.sort(key=lambda i: i["prioridade"])

    conteudo = {
        "atualizado_em": datetime.now(BRASILIA).strftime("%Y-%m-%d %H:%M:%S"),
        "ocorrencias": itens,
    }

    # grava num arquivo temporário e troca: a página nunca lê o JSON pela metade
    temporario = caminho + ".tmp"
    with open(temporario, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, ensure_ascii=False)
    os.replace(temporario, caminho)
