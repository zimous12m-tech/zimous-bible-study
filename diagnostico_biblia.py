import json
from pathlib import Path

# =====================================================
# CONFIGURAÇÃO
# =====================================================

PASTA_PROJETO = Path(__file__).resolve().parent
FICHEIRO_BIBLIA = PASTA_PROJETO / "dados" / "biblia.json"

# =====================================================
# ORDEM CANÓNICA DOS 66 LIVROS
# =====================================================

ORDEM_CANONICA = [
    "GEN", "EXO", "LEV", "NUM", "DEU",
    "JOS", "JDG", "RUT",
    "1SA", "2SA", "1KI", "2KI",
    "1CH", "2CH", "EZR", "NEH", "EST",
    "JOB", "PSA", "PRO", "ECC", "SNG",
    "ISA", "JER", "LAM", "EZK", "DAN",
    "HOS", "JOL", "AMO", "OBA", "JON",
    "MIC", "NAM", "HAB", "ZEP", "HAG",
    "ZEC", "MAL",
    "MAT", "MRK", "LUK", "JHN",
    "ACT", "ROM", "1CO", "2CO",
    "GAL", "EPH", "PHP", "COL",
    "1TH", "2TH", "1TI", "2TI",
    "TIT", "PHM", "HEB", "JAS",
    "1PE", "2PE", "1JN", "2JN",
    "3JN", "JUD", "REV"
]

# =====================================================
# CARREGAR FICHEIRO
# =====================================================

def carregar_biblia():

    if not FICHEIRO_BIBLIA.exists():
        print("ERRO: ficheiro da Bíblia não encontrado.")
        print(FICHEIRO_BIBLIA)
        return None

    try:
        with open(FICHEIRO_BIBLIA, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError as erro:
        print("ERRO: o ficheiro JSON está inválido.")
        print(erro)
        return None

    except Exception as erro:
        print("ERRO ao carregar a Bíblia:")
        print(erro)
        return None


# =====================================================
# FILTRAR LIVROS
# =====================================================

def filtrar_livros(dados):

    if isinstance(dados, dict):
        lista = dados.get("books", [])
    elif isinstance(dados, list):
        lista = dados
    else:
        return []

    livros = []

    for item in lista:

        if not isinstance(item, dict):
            continue

        capitulos = item.get("chapters")

        # Ignora metadados e objetos que não sejam livros
        if not isinstance(capitulos, list):
            continue

        livros.append(item)

    return livros


# =====================================================
# VALIDAR E CONTABILIZAR
# =====================================================

def analisar_livros(livros):

    total_livros = len(livros)
    total_capitulos = 0
    total_versiculos = 0

    livros_com_problemas = []
    codigos_encontrados = []

    print("\n" + "=" * 65)
    print("             DIAGNÓSTICO DA BÍBLIA")
    print("=" * 65)

    for livro in livros:

        nome = livro.get("name", "Nome desconhecido")
        codigo = livro.get("code", "SEM_CODIGO")
        capitulos = livro.get("chapters", [])

        codigos_encontrados.append(codigo)

        numero_capitulos = len(capitulos)
        numero_versiculos = 0

        problemas = []

        for capitulo in capitulos:

            if not isinstance(capitulo, dict):
                problemas.append("Capítulo com estrutura inválida")
                continue

            versiculos = capitulo.get("verses")

            if not isinstance(versiculos, list):
                problemas.append("Lista de versículos inválida")
                continue

            numero_versiculos += len(versiculos)

            numeros = []

            for versiculo in versiculos:

                if not isinstance(versiculo, dict):
                    problemas.append("Versículo com estrutura inválida")
                    continue

                numero = versiculo.get("number")
                texto = versiculo.get("text")

                if numero is None:
                    problemas.append("Versículo sem número")

                if not isinstance(texto, str) or not texto.strip():
                    problemas.append(
                        f"Texto vazio ou inválido no capítulo "
                        f"{capitulo.get('number', '?')}"
                    )

                if numero is not None:
                    numeros.append(numero)

            # Verificar numeração duplicada
            if len(numeros) != len(set(numeros)):
                problemas.append(
                    f"Numeração duplicada no capítulo "
                    f"{capitulo.get('number', '?')}"
                )

        total_capitulos += numero_capitulos
        total_versiculos += numero_versiculos

        print(
            f"{nome:<25} "
            f"| {numero_capitulos:>3} capítulos "
            f"| {numero_versiculos:>5} versículos"
        )

        if problemas:
            livros_com_problemas.append({
                "nome": nome,
                "problemas": problemas
            })

    return (
        total_livros,
        total_capitulos,
        total_versiculos,
        livros_com_problemas,
        codigos_encontrados
    )


# =====================================================
# VERIFICAR LIVROS EM FALTA OU DUPLICADOS
# =====================================================

def verificar_catalogo(codigos):

    print("\n" + "=" * 65)
    print("                 VERIFICAÇÃO DO CATÁLOGO")
    print("=" * 65)

    duplicados = []

    for codigo in set(codigos):
        if codigos.count(codigo) > 1:
            duplicados.append(codigo)

    faltantes = [
        codigo for codigo in ORDEM_CANONICA
        if codigo not in codigos
    ]

    desconhecidos = [
        codigo for codigo in codigos
        if codigo not in ORDEM_CANONICA
    ]

    print(f"Livros esperados: {len(ORDEM_CANONICA)}")
    print(f"Livros encontrados: {len(codigos)}")

    if faltantes:
        print("\nLIVROS EM FALTA:")
        for codigo in faltantes:
            print("-", codigo)
    else:
        print("\nTodos os livros canónicos foram encontrados.")

    if duplicados:
        print("\nCÓDIGOS DUPLICADOS:")
        for codigo in duplicados:
            print("-", codigo)
    else:
        print("\nNenhum código duplicado.")

    if desconhecidos:
        print("\nCÓDIGOS NÃO RECONHECIDOS:")
        for codigo in desconhecidos:
            print("-", codigo)
    else:
        print("\nTodos os códigos são reconhecidos.")


# =====================================================
# RELATÓRIO FINAL
# =====================================================

def apresentar_relatorio(
    livros,
    total_livros,
    total_capitulos,
    total_versiculos,
    problemas
):

    print("\n" + "=" * 65)
    print("                   RESULTADO FINAL")
    print("=" * 65)

    print(f"Total de livros:      {total_livros}")
    print(f"Total de capítulos:   {total_capitulos}")
    print(f"Total de versículos:  {total_versiculos}")

    print("\nESTRUTURA:")

    if total_livros == 66:
        print("Quantidade de livros: OK")
    else:
        print("Quantidade de livros: VERIFICAR")

    if total_capitulos == 1189:
        print("Quantidade de capítulos: OK")
    else:
        print("Quantidade de capítulos: DIFERENTE DO PADRÃO")

    print("\nINTEGRIDADE DOS DADOS:")

    if not problemas:
        print("Não foram encontrados problemas estruturais.")
    else:
        print(f"Foram encontrados problemas em {len(problemas)} livro(s).")

        for item in problemas:
            print(f"\nLivro: {item['nome']}")

            for problema in item["problemas"]:
                print("-", problema)

    print("\n" + "=" * 65)
    print("             FIM DO DIAGNÓSTICO")
    print("=" * 65)


# =====================================================
# EXECUÇÃO PRINCIPAL
# =====================================================

def main():

    dados = carregar_biblia()

    if dados is None:
        return

    livros = filtrar_livros(dados)

    if not livros:
        print("ERRO: nenhum livro válido foi encontrado.")
        return

    (
        total_livros,
        total_capitulos,
        total_versiculos,
        problemas,
        codigos
    ) = analisar_livros(livros)

    verificar_catalogo(codigos)

    apresentar_relatorio(
        livros,
        total_livros,
        total_capitulos,
        total_versiculos,
        problemas
    )


if __name__ == "__main__":
    main()