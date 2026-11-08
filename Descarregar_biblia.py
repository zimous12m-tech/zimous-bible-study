import json
import urllib.request
from pathlib import Path

# Configurações
PASTA = Path(__file__).resolve().parent
FICHEIRO_DESTINO = PASTA / "dados" / "biblia.json"

# Link para a Bíblia Almeida Atualizada (Texto moderno)
URL_BIBLIA = "https://raw.githubusercontent.com/thiagobodruk/biblia/master/json/aa.json"

# A ordem exata dos 66 livros (isto garante que o código de cada livro fica certo)
ORDEM_CANONICA = [
    "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT",
    "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST",
    "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN",
    "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG",
    "ZEC", "MAL", "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO",
    "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM",
    "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"
]

def descarregar_e_converter():
    print("A descarregar a Bíblia moderna (Almeida Atualizada)...")
    req = urllib.request.Request(URL_BIBLIA, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as response:
        # A MÁGICA ESTÁ AQUI: utf-8-sig remove aquele caracter invisível (BOM) do início
        conteudo = response.read().decode('utf-8-sig')
        dados_originais = json.loads(conteudo)

    print("A converter para o formato da Zimous...")
    
    novos_livros = []
    for i, livro_orig in enumerate(dados_originais):
        # Pega o código exato da lista canónica (GEN, EXO, etc.)
        codigo_correto = ORDEM_CANONICA[i] if i < len(ORDEM_CANONICA) else "UNK"
        
        capitulos_formatados = []
        for cap_idx, versiculos_orig in enumerate(livro_orig.get("chapters", []), start=1):
            versiculos_formatados = []
            for ver_idx, texto_orig in enumerate(versiculos_orig, start=1):
                versiculos_formatados.append({
                    "number": ver_idx,
                    "text": texto_orig.strip()
                })
            capitulos_formatados.append({
                "number": cap_idx,
                "verses": versiculos_formatados
            })

        novo_livro = {
            "code": codigo_correto,
            "name": livro_orig.get("name", ""),
            "abbrev": livro_orig.get("abbrev", ""),
            "chapters": capitulos_formatados
        }
        novos_livros.append(novo_livro)

    # Cria a estrutura final
    biblia_final = {
        "project": "Zimous Bible Study",
        "version": "AA",
        "translation": "Almeida Atualizada",
        "language": "pt",
        "total_books": len(novos_livros),
        "books": novos_livros
    }

    # Cria a pasta 'dados' se ela não existir
    (PASTA / "dados").mkdir(exist_ok=True)
    
    # Guarda o ficheiro
    with open(FICHEIRO_DESTINO, "w", encoding="utf-8") as f:
        json.dump(biblia_final, f, ensure_ascii=False, indent=2)

    print(f"Sucesso! Bíblia atualizada com {len(novos_livros)} livros.")
    print(f"Ficheiro guardado em: {FICHEIRO_DESTINO}")

if __name__ == "__main__":
    descarregar_e_converter()