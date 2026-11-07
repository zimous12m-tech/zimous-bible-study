# -*- coding: utf-8 -*-
"""
ZIMOUS BIBLE STUDY - servidor local e na nuvem
"""
import json
import urllib.parse
import sys
import os
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

# Correção para encontrar os ficheiros, seja no PC, .exe ou Render
if getattr(sys, 'frozen', False):
    ROOT = Path(sys._MEIPASS)
else:
    ROOT = Path(__file__).resolve().parent

# Correção para o Render: usa a porta que a plataforma definir
PORT = int(os.environ.get("PORT", 8765))
HOST = "0.0.0.0" # Permite ligações da internet (Render)

print("A carregar a Bíblia...")
LIVROS = ordenar_livros(motor.carregar_biblia())
print("A construir índice...")
INDICE = motor.preparar_indice(LIVROS)
print("A inicializar Motores...")
motor_tematico = MotorTematico()
motor_duvidas = MotorDuvidas()
print("Livros:", len(LIVROS), "| Versículos:", len(INDICE))

def item_publico(item):
    if not isinstance(item, dict):
        return {"texto": str(item)}
    return {
        "livro": item.get("livro", ""),
        "capitulo": item.get("capitulo", ""),
        "versiculo": item.get("versiculo", ""),
        "referencia": item.get("referencia", ""),
        "texto": item.get("texto", ""),
    }

def pesquisar(opcao, consulta):
    consulta = (consulta or "").strip()
    if not consulta:
        raise ValueError("Introduz um termo ou uma expressão.")
    palavras = motor.extrair_palavras(consulta)
    if opcao == 1:
        if not palavras:
            raise ValueError("Nenhum termo válido na pesquisa.")
        resultados = motor.pesquisar_todos(INDICE, palavras)
        return {"tipo": "versiculos", "total": len(resultados), "resultados": [item_publico(x) for x in resultados]}
    if opcao == 2:
        resultados = motor.pesquisar_frase(INDICE, consulta)
        return {"tipo": "versiculos", "total": len(resultados), "resultados": [item_publico(x) for x in resultados]}
    if opcao == 3:
        if not palavras:
            raise ValueError("Nenhum termo válido na pesquisa.")
        resultados = motor.pesquisar_qualquer(INDICE, palavras)
        return {"tipo": "versiculos", "total": len(resultados), "resultados": [item_publico(x) for x in resultados]}
    if opcao == 4:
        if not palavras:
            raise ValueError("Nenhum termo válido na pesquisa.")
        contador = motor.pesquisar_concordancia(INDICE, set(palavras))
        if not contador:
            linhas = "Nenhuma ocorrência encontrada."
            total_ocorrencias = 0
        else:
            linhas = "\n".join(f"{palavra:<20} {quantidade:>6}" for palavra, quantidade in contador.most_common())
            total_ocorrencias = sum(contador.values())
        return {"tipo": "concordancia", "total": total_ocorrencias, "relatorio": "CONCORDÂNCIA\n" + "=" * 40 + "\n" + linhas}
    if opcao == 5:
        grupos = getattr(motor, "GRUPOS_RELACIONADOS", {})
        relacionados = []
        for termo in palavras:
            if termo in grupos:
                relacionados.extend(grupos[termo])
        relacionados = list(dict.fromkeys(relacionados))
        if not relacionados:
            return {"tipo": "informacao", "total": 0, "mensagem": "Sem grupo relacionado."}
        resultados = motor.pesquisar_qualquer(INDICE, relacionados)
        return {"tipo": "versiculos", "total": len(resultados), "termos_relacionados": relacionados, "resultados": [item_publico(x) for x in resultados]}
    if opcao == 6:
        if not palavras:
            raise ValueError("Nenhum termo válido.")
        buffer = StringIO()
        with redirect_stdout(buffer):
            motor.analisar_contextos(INDICE, set(palavras))
        return {"tipo": "analise", "relatorio": buffer.getvalue(), "mensagem": "Análise contextual concluída."}
    if opcao == 7:
        if len(palavras) != 1:
            raise ValueError("Introduz apenas uma entidade.")
        buffer = StringIO()
        with redirect_stdout(buffer):
            motor.analisar_relacoes(INDICE, palavras[0])
        return {"tipo": "analise", "relatorio": buffer.getvalue(), "mensagem": "Análise de relações concluída."}
    raise ValueError("Operação inválida.")


class Handler(BaseHTTPRequestHandler):
    def enviar(self, codigo, dados, tipo="application/json; charset=utf-8"):
        corpo = dados if isinstance(dados, bytes) else json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)

        if url.path in ("/", "/index.html"):
            try:
                html = (ROOT / "index.html").read_text(encoding="utf-8")
                return self.enviar(200, html.encode("utf-8"), "text/html; charset=utf-8")
            except Exception as e:
                return self.enviar(500, {"erro": f"Erro a ler index.html: {e}"})

        if url.path == "/api/status":
            return self.enviar(200, {"ok": True, "livros": len(LIVROS), "versiculos": len(INDICE), "motor": "ZIMOUS BIBLE STUDY"})

        if url.path == "/api/books":
            return self.enviar(200, [{"nome": x.get("name", "Desconhecido"), "abbrev": x.get("abbrev", ""), "capitulos": [c.get("number") for c in x.get("chapters", [])]} for x in LIVROS])

        if url.path == "/api/temas":
            return self.enviar(200, motor_tematico.listar_temas())

        if url.path == "/api/duvidas":
            return self.enviar(200, {
                "categorias": motor_duvidas.categorias(),
                "duvidas": motor_duvidas.listar(),
            })

        if url.path.startswith("/api/duvida/"):
            duvida_id = url.path.rsplit("/", 1)[-1]
            d = motor_duvidas.detalhe(duvida_id)
            if d:
                d["versiculos_resolvidos"] = [
                    r for r in (motor_tematico.buscar_referencia(x) for x in d.get("versiculos", []))
                    if r
                ]
                return self.enviar(200, d)
            return self.enviar(404, {"erro": "Dúvida não encontrada."})

        if url.path.startswith("/api/estudo-tematico") or url.path.startswith("/estudo-tematico"):
            consulta = q.get("q", [""])[0]
            if not consulta:
                partes = url.path.split("/")
                if len(partes) > 2 and partes[-1]:
                    consulta = urllib.parse.unquote(partes[-1])
            resposta = motor_tematico.analisar_tema(consulta) if consulta else {"sucesso": False, "erro": "Consulta vazia."}
            return self.enviar(200, resposta)

        if url.path == "/api/chapter":
            nome = q.get("book", [""])[0]
            try:
                numero = int(q.get("chapter", ["1"])[0])
            except ValueError:
                return self.enviar(400, {"erro": "Capítulo inválido."})
            for livro in LIVROS:
                if livro.get("name") == nome or livro.get("abbrev") == nome:
                    for cap in livro.get("chapters", []):
                        if cap.get("number") == numero:
                            return self.enviar(200, {"livro": livro.get("name"), "capitulo": numero, "versiculos": cap.get("verses", [])})
            return self.enviar(404, {"erro": "Capítulo não encontrado."})

        return self.enviar(404, {"erro": "Rota não encontrada."})

    def do_POST(self):
        url = urlparse(self.path)
        if url.path != "/api/search":
            return self.enviar(404, {"erro": "Rota não encontrada."})
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            dados = json.loads(self.rfile.read(tamanho).decode("utf-8"))
            resultado = pesquisar(int(dados.get("opcao", 1)), dados.get("consulta", ""))
            self.enviar(200, resultado)
        except Exception as erro:
            self.enviar(400, {"erro": str(erro)})

    def log_message(self, formato, *args):
        print("[HTTP]", formato % args)

class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    print(f"\nZIMOUS BIBLE STUDY disponível em http://{HOST}:{PORT}")
    print("Para parar o servidor: Ctrl+C")
    ReusableThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
