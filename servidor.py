import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def iniciar(diretorio: str, porta: int) -> None:
    handler = partial(SimpleHTTPRequestHandler, directory=diretorio)
    servidor = ThreadingHTTPServer(("0.0.0.0", porta), handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    print(f"Painel disponível em: http://localhost:{porta}/")