import os
import time
from datetime import datetime

import truststore

import servidor
from coleta import coletar_tudo
from configuracao import INTERVALO_SEGUNDOS, PORTA_PAINEL
from saida import gravar_json

truststore.inject_into_ssl()

PASTA_WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
ARQUIVO_DADOS = os.path.join(PASTA_WEB, "dados.json")


def agora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    servidor.iniciar(PASTA_WEB, PORTA_PAINEL)

    while True:
        print(f"[{agora()}] Coletando ocorrências...")
        try:
            ocorrencias = coletar_tudo()
            gravar_json(ocorrencias, ARQUIVO_DADOS)
            print(f"[{agora()}] {len(ocorrencias)} ocorrência(s) gravada(s).")
        except Exception as erro:
            print(f"[{agora()}] ciclo falhou: {erro}")
        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    main()