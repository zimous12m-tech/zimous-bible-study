import threading
import webbrowser
import time
import servidor


def abrir_browser():
    time.sleep(1.5)  # Espera o servidor ligar
    webbrowser.open("http://127.0.0.1:8765")


if __name__ == "__main__":
    # Abre o browser numa thread separada
    threading.Thread(target=abrir_browser, daemon=True).start()

    # Inicia o servidor
    print("A iniciar ZIMOUS BIBLE STUDY...")
    server = servidor.ReusableThreadingHTTPServer(("127.0.0.1", 8765), servidor.Handler)
    server.serve_forever()