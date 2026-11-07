# -*- coding: utf-8 -*-
"""
ZIMOUS BIBLE STUDY - servidor local e na nuvem
"""
import json
import urllib.parse
import sys
import os # Necessário para ler a porta do Render
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from contextlib import redirect_stdout
from io import StringIO

import motor_pesquisa as motor
from motor_tematico import MotorTematico
from motor_duvidas import MotorDuvidas

ORDEM_CANONICA = [
    "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT",
    "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST",
    "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN",
    "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG",
    "ZEC", "MAL", "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO",
    "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM",
    "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"
]

def ordenar_livros(livros):
    def chave(livro):
        codigo = livro.get("code", livro.get("abbrev", ""))
        try:
            return ORDEM_CANONICA.index(codigo)
        except ValueError:
            return 999
    return sorted(livros, key=chave)

# Correção para encontrar os ficheiros, seja no PC ou no Render (nuvem)
if getattr(sys, 'frozen', False):
    ROOT = Path(sys._MEIPASS)
else:
    ROOT = Path(__file__).resolve().parent

# Correção para o Render: usa a porta que a plataforma definir
PORT = int(os.environ.get("PORT", 8765))
HOST = "0.0.0.0" # Permite ligações da internet

print("A carregar a Bíblia...")
LIVROS = ordenar_livros(motor.carregar_biblia())
print("A construir índice...")
INDICE = motor.preparar_indice(LIVROS)
print("A inicializar Motores...")
motor_tematico = MotorTematico()
motor_duvidas = MotorDuvidas()
print("Livros:", len(LIVROS), "| Versículos:", len(INDICE))

# ... (O resto do código - funções `item_publico`, `pesquisar` e a classe `Handler` - permanece exatamente igual ao que já tinhas)
# Podes copiar a parte restante do teu `servidor.py` atual para aqui.

class Handler(BaseHTTPRequestHandler):
    # ... (o teu código existente da classe Handler)
    pass # Substitui o 'pass' pelo código real do Handler


class ReusableThreadingHTTPServer:
    pass


if __name__ == "__main__":
    print(f"\nZIMOUS BIBLE STUDY disponível em http://{HOST}:{PORT}")
    print("Para parar o servidor: Ctrl+C")
    ReusableThreadingHTTPServer((HOST, PORT), Handler).serve_forever()