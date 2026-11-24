import os

from coleta import coletar_tudo
from saida import gravar_json

PASTA_WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

if __name__ == "__main__":
    gravar_json(coletar_tudo(), os.path.join(PASTA_WEB, "dados.json"))