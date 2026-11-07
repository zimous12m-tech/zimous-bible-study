
import json
import re
import unicodedata
from pathlib import Path
from collections import Counter, defaultdict


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent
FICHEIRO_BIBLIA = PASTA_PROJETO / "dados" / "biblia.json"

RESULTADOS_POR_PAGINA = 20
LIMITE_EXPRESSOES = 30
EXEMPLOS_POR_EXPRESSAO = 2
FREQUENCIA_MINIMA = 2


# ============================================================
# PALAVRAS FUNCIONAIS
# ============================================================

STOPWORDS_CONTEXTO = {
    "a", "as", "o", "os",
    "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas",
    "e", "ou", "mas",
    "que", "se",
    "por", "pelo", "pela", "pelos", "pelas",
    "para", "perante",
    "com", "sem",
    "ao", "aos", "a", "as",
    "sobre", "entre", "ate",
    "como", "quando", "onde",
    "porque", "pois",
    "lhe", "lhes",
    "me", "te",
    "ele", "ela", "eles", "elas",
    "isso", "isto", "aquilo",
    "qual", "quais",
    "ser", "estar",
}

POSSESSIVOS = {
    "meu", "minha", "meus", "minhas",
    "teu", "tua", "teus", "tuas",
    "seu", "sua", "seus", "suas",
    "nosso", "nossa", "nossos", "nossas",
    "vosso", "vossa", "vossos", "vossas",
}


# ============================================================
# GRUPOS DE TERMOS RELACIONADOS
# ============================================================

GRUPOS_RELACIONADOS = {
    "deus": [
        "deus", "deuses", "divino",
        "divina", "divindade", "divindades"
    ],

    "jesus": [
        "jesus", "cristo", "messias",
        "nazareno", "salvador"
    ],

    "amor": [
        "amor", "amar", "amado", "amada",
        "amados", "amadas", "caridade"
    ],

    "guerra": [
        "guerra", "guerras", "batalha",
        "batalhas", "combate", "combates",
        "inimigo", "inimigos"
    ],

    "morte": [
        "morte", "morrer", "morto",
        "mortos", "morta", "mortas",
        "falecer", "falecido"
    ],

    "vida": [
        "vida", "viver", "vivente",
        "viventes", "vivendo"
    ],

    "pecado": [
        "pecado", "pecados", "pecador",
        "pecadores", "pecadora", "pecar"
    ],

    "perdao": [
        "perdao", "perdoar", "perdoado",
        "perdoados", "perdoada", "perdoadas"
    ],

    "fe": [
        "fe", "crer", "cre", "crenca",
        "crente", "crentes", "acreditar"
    ],

    "poder": [
        "poder", "poderoso", "poderosa",
        "poderosos", "forca", "autoridade"
    ],
}


# ============================================================
# VERBOS PARA ANÁLISE DE RELAÇÕES
# ============================================================

# Todas as formas estão escritas sem acentos,
# porque serão comparadas com palavras normalizadas.

VERBOS_ANALISE = {
    "criou", "criaram", "cria", "criado", "criador",
    "fez", "fizeram", "faze", "fazer", "feito",
    "disse", "diz", "dizem", "dito", "disseram",
    "falou", "fala", "falaram", "falado",
    "ordenou", "ordena", "ordenaram", "ordenado",
    "mandou", "manda", "mandaram", "mandado",
    "deu", "da", "dara", "dado", "deram",
    "tirou", "tira", "tiraram",
    "salvou", "salva", "salvaram",
    "perdoou", "perdoa", "perdoaram",
    "castigou", "castiga", "castigaram",
    "julgou", "julga", "julgaram",
    "amou", "ama", "amaram",
    "abencoou", "abencoa", "abencoaram",
    "prometeu", "promete", "prometeram",
    "escolheu", "escolhe", "escolheram",
    "conhece", "conheceu", "conheceram",
    "viu", "ve", "viram",
    "ouviu", "ouve", "ouviram",
    "respondeu", "responde", "responderam",
    "pediu", "pede", "pediram",
    "proibiu", "proibe", "proibiram",
    "permitiu", "permite", "permitiram",
    "estabeleceu", "estabelece", "estabeleceram",
    "reinara", "reina", "reinou", "reinaram",
    "habita", "habitou", "habitara", "habitaram",
    "destruiu", "destroi", "destruiram",
    "ressuscitou", "ressuscita",
    "envia", "enviou", "enviaram",
    "conduziu", "conduz", "conduziram",
    "libertou", "liberta", "libertaram",
    "condenou", "condena", "condenaram",
    "revelou", "revela", "revelaram",
    "apareceu", "aparece", "apareceram",
    "habitava", "habitar",
    "passou", "passa", "passaram",
    "tomou", "toma", "tomaram",
    "recebeu", "recebe", "receberam",
    "fez", "faz", "fazem",
    "pode", "podera", "poderia",
    "sera", "sao", "era", "foram",
    "esta", "estava", "estao",
    "vive", "viveu", "viveram",
    "morreu", "morre", "morreram",
    "nasceu", "nasce", "nasceram",
    "subiu", "sobe", "subiram",
    "desceu", "desce", "desceram",
    "venceu", "vence", "venceram",
    "rejeitou", "rejeita", "rejeitaram",
    "adorou", "adora", "adoraram",
    "serviu", "serve", "serviram",
    "guiou", "guia", "guiaram",
    "ensinou", "ensina", "ensinaram",
    "curou", "cura", "curaram",
    "ressuscitaram", "ressuscitar",
    "pecou", "peca", "pecaram",
    "matou", "mata", "mataram",
    "escreveu", "escreve", "escreveram",
    "chamou", "chama", "chamaram",
    "resgatou", "resgata", "resgataram",
    "construiu", "constroi", "construiram",
    "levantou", "levanta", "levantaram",
    "jurou", "jura", "juraram",
    "acrescentou", "acrescenta",
    "declarou", "declara", "declararam",
    "manifestou", "manifesta", "manifestaram",
}


PREPOSICOES_ASSOCIACAO = {
    "de", "do", "da", "dos", "das"
}

STOP_FIM_RELACAO = {
    "e", "ou", "mas", "porque", "pois",
    "que", "quando", "como", "se",
}


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def normalizar(texto):

    texto = str(texto).casefold()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    return "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )


def expandir_contracoes(texto):

    """
    Trata algumas contrações antigas.

    d'Israel  -> de Israel
    d'elle    -> de elle
    n'aquelle -> em aquelle

    A expansão é uma regra lexical simplificada.
    """

    texto = re.sub(
        r"\bd['’](?=[A-Za-zÀ-ÿ])",
        "de ",
        texto,
        flags=re.IGNORECASE
    )

    texto = re.sub(
        r"\bn['’](?=[A-Za-zÀ-ÿ])",
        "em ",
        texto,
        flags=re.IGNORECASE
    )

    return texto


def extrair_palavras(texto):

    return re.findall(
        r"\w+",
        normalizar(texto)
    )


def extrair_palavras_originais(texto):

    return re.findall(
        r"\w+",
        texto
    )


# ============================================================
# CARREGAMENTO DA BÍBLIA
# ============================================================

def carregar_biblia():

    print("A carregar a Bíblia...")

    if not FICHEIRO_BIBLIA.exists():

        raise FileNotFoundError(
            f"Ficheiro não encontrado: {FICHEIRO_BIBLIA}"
        )

    with open(
        FICHEIRO_BIBLIA,
        "r",
        encoding="utf-8"
    ) as ficheiro:

        dados = json.load(ficheiro)

    if isinstance(dados, dict):

        livros = dados.get("books", [])

    elif isinstance(dados, list):

        livros = dados

    else:

        raise ValueError(
            "Formato JSON da Bíblia inválido."
        )

    livros = [
        livro for livro in livros
        if isinstance(livro, dict)
        and isinstance(livro.get("chapters"), list)
    ]

    if not livros:

        raise ValueError(
            "Nenhum livro válido encontrado."
        )

    return livros


# ============================================================
# CONSTRUÇÃO DO ÍNDICE
# ============================================================

def preparar_indice(livros):

    print("A construir índice de pesquisa...")

    indice = []

    for livro in livros:

        nome_livro = livro.get(
            "name",
            livro.get("abbrev", "Livro desconhecido")
        )

        for capitulo in livro.get("chapters", []):

            numero_capitulo = capitulo.get(
                "number",
                0
            )

            for versiculo in capitulo.get("verses", []):

                numero_versiculo = versiculo.get(
                    "number",
                    0
                )

                texto = str(
                    versiculo.get("text", "")
                )

                referencia = (
                    f"{nome_livro} "
                    f"{numero_capitulo}:{numero_versiculo}"
                )

                tokens = extrair_palavras(texto)

                indice.append({

                    "livro": nome_livro,
                    "capitulo": numero_capitulo,
                    "versiculo": numero_versiculo,
                    "referencia": referencia,
                    "texto": texto,
                    "normalizado": normalizar(texto),
                    "tokens": tokens,
                    "palavras": set(tokens)

                })

    return indice


# ============================================================
# DESTAQUE DOS TERMOS
# ============================================================

def destacar_termos(texto, termos):

    if not termos:
        return texto

    termos_validos = set()

    for termo in termos:

        termos_validos.update(
            extrair_palavras(termo)
        )

    normalizado = ""
    mapa = []

    for posicao, caractere in enumerate(texto):

        parte = unicodedata.normalize(
            "NFD",
            caractere.casefold()
        )

        for letra in parte:

            if unicodedata.category(letra) == "Mn":
                continue

            normalizado += letra
            mapa.append(posicao)

    intervalos = []

    for correspondencia in re.finditer(
        r"\w+",
        normalizado
    ):

        palavra = correspondencia.group()

        if palavra in termos_validos:

            inicio = mapa[correspondencia.start()]

            fim = (
                mapa[correspondencia.end() - 1] + 1
            )

            intervalos.append(
                (inicio, fim)
            )

    if not intervalos:
        return texto

    unidos = []

    for inicio, fim in intervalos:

        if unidos and inicio <= unidos[-1][1]:

            unidos[-1] = (
                unidos[-1][0],
                max(unidos[-1][1], fim)
            )

        else:

            unidos.append(
                (inicio, fim)
            )

    resultado = []
    posicao_atual = 0

    for inicio, fim in unidos:

        resultado.append(
            texto[posicao_atual:inicio]
        )

        resultado.append(
            "[" + texto[inicio:fim].upper() + "]"
        )

        posicao_atual = fim

    resultado.append(
        texto[posicao_atual:]
    )

    return "".join(resultado)


# ============================================================
# PESQUISA
# ============================================================

def pesquisar_todos(indice, termos):

    return [
        item for item in indice
        if all(
            termo in item["palavras"]
            for termo in termos
        )
    ]


def pesquisar_frase(indice, frase):

    resultados = []

    tokens_frase = extrair_palavras(frase)

    if not tokens_frase:
        return resultados

    tamanho = len(tokens_frase)

    for item in indice:

        tokens = item["tokens"]

        for posicao in range(
            len(tokens) - tamanho + 1
        ):

            if (
                tokens[posicao:posicao + tamanho]
                == tokens_frase
            ):

                resultados.append(item)
                break

    return resultados


def pesquisar_qualquer(indice, termos):

    return [
        item for item in indice
        if any(
            termo in item["palavras"]
            for termo in termos
        )
    ]


def pesquisar_concordancia(indice, termos):

    contador = Counter()

    for item in indice:

        for palavra in item["tokens"]:

            if palavra in termos:

                contador[palavra] += 1

    return contador


# ============================================================
# ANÁLISE CONTEXTUAL
# ============================================================

def palavra_informativa(palavra, termos):

    if palavra in termos:
        return True

    if palavra in POSSESSIVOS:
        return True

    if palavra in STOPWORDS_CONTEXTO:
        return False

    return True


def analisar_contextos(indice, termos):

    contador = Counter()

    referencias = defaultdict(set)

    exemplos = defaultdict(list)

    termos = set(termos)

    total_versiculos = 0

    for item in indice:

        texto_expandido = expandir_contracoes(
            item["texto"]
        )

        tokens = extrair_palavras(
            texto_expandido
        )

        tokens_originais = extrair_palavras_originais(
            texto_expandido
        )

        tamanho_tokens = min(
            len(tokens),
            len(tokens_originais)
        )

        versiculo_tem_termo = any(
            palavra in termos
            for palavra in tokens
        )

        if not versiculo_tem_termo:
            continue

        total_versiculos += 1

        for posicao, palavra in enumerate(tokens):

            if palavra not in termos:
                continue

            for tamanho in (2, 3, 4):

                inicio_minimo = max(
                    0,
                    posicao - tamanho + 1
                )

                inicio_maximo = min(
                    posicao,
                    tamanho_tokens - tamanho
                )

                for inicio in range(
                    inicio_minimo,
                    inicio_maximo + 1
                ):

                    fim = inicio + tamanho

                    expressao_tokens = tokens[inicio:fim]

                    if not any(
                        p in termos
                        for p in expressao_tokens
                    ):
                        continue

                    outras_palavras = [
                        p for p in expressao_tokens
                        if p not in termos
                        and palavra_informativa(p, termos)
                    ]

                    if not outras_palavras:
                        continue

                    chave = " ".join(
                        expressao_tokens
                    )

                    expressao_original = " ".join(
                        tokens_originais[inicio:fim]
                    )

                    contador[chave] += 1

                    referencias[chave].add(
                        item["referencia"]
                    )

                    ja_existe = any(
                        exemplo["referencia"]
                        == item["referencia"]
                        for exemplo in exemplos[chave]
                    )

                    if not ja_existe:

                        exemplos[chave].append({

                            "referencia": item["referencia"],
                            "texto": item["texto"],
                            "expressao": expressao_original

                        })

    expressoes = [
        chave
        for chave, quantidade in contador.items()
        if quantidade >= FREQUENCIA_MINIMA
    ]

    expressoes.sort(
        key=lambda chave: (
            len(referencias[chave]),
            contador[chave]
        ),
        reverse=True
    )

    print("\n" + "=" * 70)
    print("              ANÁLISE CONTEXTUAL")
    print("=" * 70)

    print(
        "Termos analisados:",
        ", ".join(sorted(termos))
    )

    print(
        "Versículos com os termos:",
        total_versiculos
    )

    if not expressoes:

        print(
            "\nNão foram encontradas expressões "
            "repetidas com os critérios atuais."
        )

        return

    print(
        "\nExpressões identificadas:",
        len(expressoes)
    )

    print(
        "A apresentar:",
        min(len(expressoes), LIMITE_EXPRESSOES)
    )

    print("\n" + "-" * 70)

    for numero, chave in enumerate(
        expressoes[:LIMITE_EXPRESSOES],
        start=1
    ):

        print(f"\n{numero}. {chave}")

        print(
            "   Ocorrências:",
            contador[chave]
        )

        print(
            "   Versículos distintos:",
            len(referencias[chave])
        )

        print("   Exemplos completos:")

        for exemplo in exemplos[chave][
            :EXEMPLOS_POR_EXPRESSAO
        ]:

            print(
                f"\n   [{exemplo['referencia']}]"
            )

            print(
                "   " + exemplo["texto"]
            )

    print("\n" + "-" * 70)

    print(
        "Nota: as expressões são identificadas por "
        "proximidade lexical. Não representam "
        "automaticamente relações gramaticais "
        "ou conclusões teológicas."
    )


# ============================================================
# ESTATÍSTICAS POR LIVRO
# ============================================================

def estatisticas_por_livro(resultados):

    contador = Counter(
        item["livro"]
        for item in resultados
    )

    total = len(resultados)

    print("\n" + "=" * 50)
    print("          ESTATÍSTICAS POR LIVRO")
    print("=" * 50)

    if not contador:

        print("Nenhum resultado para analisar.")
        return

    for livro, quantidade in contador.most_common():

        percentagem = (
            quantidade / total * 100
        )

        print(
            f"{livro:<25} "
            f"{quantidade:>5} versículos "
            f"({percentagem:5.1f}%)"
        )

    print("-" * 50)

    print(
        f"Total de versículos encontrados: {total}"
    )


# ============================================================
# APRESENTAÇÃO E PAGINAÇÃO
# ============================================================

def apresentar_resultados(
    resultados,
    termos_destaque=None
):

    if termos_destaque is None:
        termos_destaque = []

    total = len(resultados)

    if total == 0:

        print("\nNenhum resultado encontrado.")
        return

    total_paginas = (
        total + RESULTADOS_POR_PAGINA - 1
    ) // RESULTADOS_POR_PAGINA

    pagina_atual = 1

    while True:

        inicio = (
            pagina_atual - 1
        ) * RESULTADOS_POR_PAGINA

        fim = min(
            inicio + RESULTADOS_POR_PAGINA,
            total
        )

        print("\n" + "=" * 65)

        print(
            f"RESULTADOS: {total} | "
            f"PÁGINA {pagina_atual}/{total_paginas}"
        )

        print("=" * 65)

        for item in resultados[inicio:fim]:

            texto = destacar_termos(
                item["texto"],
                termos_destaque
            )

            print(f"\n{item['referencia']}")
            print(texto)

        print("\n" + "-" * 65)

        print(
            f"A mostrar {inicio + 1}-{fim} "
            f"de {total} resultados."
        )

        print("\nN - Próxima página")
        print("A - Página anterior")
        print("S - Sair dos resultados")

        escolha = input(
            "\nEscolhe: "
        ).strip().casefold()

        if escolha == "n":

            if pagina_atual < total_paginas:
                pagina_atual += 1
            else:
                print("Já estás na última página.")

        elif escolha == "a":

            if pagina_atual > 1:
                pagina_atual -= 1
            else:
                print("Já estás na primeira página.")

        elif escolha == "s":

            break

        else:

            print("Opção inválida.")


# ============================================================
# MENU DE TERMOS RELACIONADOS
# ============================================================

def menu_termos_relacionados():

    print("\n" + "=" * 50)
    print("       GRUPOS DE TERMOS RELACIONADOS")
    print("=" * 50)

    grupos = list(
        GRUPOS_RELACIONADOS.keys()
    )

    for numero, grupo in enumerate(
        grupos,
        start=1
    ):

        print(
            f"{numero} - {grupo.capitalize()}"
        )

    print("0 - Voltar")

    escolha = input(
        "\nEscolhe um grupo: "
    ).strip()

    if escolha == "0":
        return None

    if not escolha.isdigit():

        print("Opção inválida.")
        return None

    numero = int(escolha)

    if numero < 1 or numero > len(grupos):

        print("Opção inválida.")
        return None

    grupo = grupos[numero - 1]

    termos = GRUPOS_RELACIONADOS[grupo]

    print(f"\nGrupo selecionado: {grupo}")

    print(
        "Termos incluídos:",
        ", ".join(termos)
    )

    return termos


# ============================================================
# DIVISÃO DE FRASES
# ============================================================

def dividir_frases(texto):

    """
    Divide um versículo em segmentos delimitados
    por pontuação forte ou intermédia.

    Esta divisão é uma aproximação.
    """

    partes = re.split(
        r"(?<=[.!?;:])\s+",
        texto
    )

    return [
        parte.strip()
        for parte in partes
        if parte.strip()
    ]


# ============================================================
# REGISTO DE RELAÇÕES
# ============================================================

def registar_relacao(
    dados,
    chave,
    referencia,
    texto
):

    dados[chave]["ocorrencias"] += 1

    dados[chave]["referencias"].add(
        referencia
    )

    ja_existe = any(
        exemplo["referencia"] == referencia
        and exemplo["texto"] == texto
        for exemplo in dados[chave]["exemplos"]
    )

    if (
        not ja_existe
        and len(dados[chave]["exemplos"]) < 3
    ):

        dados[chave]["exemplos"].append({

            "referencia": referencia,
            "texto": texto

        })


# ============================================================
# ANÁLISE DE RELAÇÕES E AFIRMAÇÕES
# ============================================================

def analisar_relacoes(indice, entidade="deus"):

    """
    Procura padrões lexicais de associação e verbos
    próximos de uma entidade.

    A. Associação:
       Deus de Israel
       Deus de Abraão
       Deus dos seus pais

    B. Verbos próximos:
       Deus criou
       Deus disse
       Deus ordenou

    IMPORTANTE:
    A proximidade de um verbo não prova que a
    entidade seja o sujeito ou agente da ação.
    """

    entidade = normalizar(
        entidade
    ).strip()

    if not entidade:

        print("Entidade vazia.")
        return

    dados_associacao = defaultdict(
        lambda: {
            "ocorrencias": 0,
            "referencias": set(),
            "exemplos": []
        }
    )

    dados_acoes = defaultdict(
        lambda: {
            "ocorrencias": 0,
            "referencias": set(),
            "exemplos": []
        }
    )

    total_segmentos = 0

    for item in indice:

        frases = dividir_frases(
            item["texto"]
        )

        for frase in frases:

            frase_expandida = expandir_contracoes(
                frase
            )

            palavras_originais = re.findall(
                r"\w+",
                frase_expandida
            )

            palavras = [
                normalizar(p)
                for p in palavras_originais
            ]

            if entidade not in palavras:
                continue

            total_segmentos += 1

            for posicao, palavra in enumerate(palavras):

                if palavra != entidade:
                    continue

                # ------------------------------------------------
                # A. EXPRESSÕES DE ASSOCIAÇÃO
                # ------------------------------------------------

                if posicao + 1 < len(palavras):

                    seguinte = palavras[
                        posicao + 1
                    ]

                    if seguinte in PREPOSICOES_ASSOCIACAO:

                        complemento = []

                        for p in palavras[
                            posicao + 2:posicao + 6
                        ]:

                            if p in STOP_FIM_RELACAO:
                                break

                            if p in VERBOS_ANALISE:
                                break

                            complemento.append(p)

                        if complemento:

                            nome_relacao = (
                                entidade
                                + " "
                                + seguinte
                                + " "
                                + " ".join(complemento)
                            )

                            registar_relacao(
                                dados_associacao,
                                nome_relacao,
                                item["referencia"],
                                frase
                            )

                # ------------------------------------------------
                # B. VERBOS PRÓXIMOS DA ENTIDADE
                # ------------------------------------------------

                inicio = max(
                    0,
                    posicao - 5
                )

                fim = min(
                    len(palavras),
                    posicao + 6
                )

                janela = palavras[
                    inicio:fim
                ]

                verbos_encontrados = set(
                    verbo
                    for verbo in janela
                    if verbo in VERBOS_ANALISE
                )

                for verbo in verbos_encontrados:

                    chave = verbo

                    registar_relacao(
                        dados_acoes,
                        chave,
                        item["referencia"],
                        frase
                    )

    # ========================================================
    # APRESENTAÇÃO
    # ========================================================

    print("\n" + "=" * 70)
    print("       ANÁLISE DE RELAÇÕES E AFIRMAÇÕES")
    print("=" * 70)

    print(
        "Entidade analisada:",
        entidade
    )

    print(
        "Segmentos com a entidade:",
        total_segmentos
    )

    # --------------------------------------------------------
    # A. ASSOCIAÇÕES
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("A. EXPRESSÕES DE ASSOCIAÇÃO")
    print("-" * 70)

    associacoes = sorted(
        dados_associacao.items(),
        key=lambda x: (
            len(x[1]["referencias"]),
            x[1]["ocorrencias"]
        ),
        reverse=True
    )

    if not associacoes:

        print(
            "Nenhuma associação identificada."
        )

    for numero, (nome, dados) in enumerate(
        associacoes[:20],
        start=1
    ):

        print(f"\n{numero}. {nome}")

        print(
            "   Ocorrências:",
            dados["ocorrencias"]
        )

        print(
            "   Versículos distintos:",
            len(dados["referencias"])
        )

        for exemplo in dados["exemplos"][:2]:

            print(
                f"   [{exemplo['referencia']}]"
            )

            print(
                "   " + exemplo["texto"]
            )

    # --------------------------------------------------------
    # B. VERBOS PRÓXIMOS
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("B. VERBOS PRÓXIMOS DA ENTIDADE")
    print("-" * 70)

    acoes = sorted(
        dados_acoes.items(),
        key=lambda x: (
            len(x[1]["referencias"]),
            x[1]["ocorrencias"]
        ),
        reverse=True
    )

    if not acoes:

        print(
            "Nenhum verbo identificado."
        )

    for numero, (verbo, dados) in enumerate(
        acoes[:25],
        start=1
    ):

        print(
            f"\n{numero}. {entidade} / {verbo}"
        )

        print(
            "   Ocorrências:",
            dados["ocorrencias"]
        )

        print(
            "   Versículos distintos:",
            len(dados["referencias"])
        )

        for exemplo in dados["exemplos"][:2]:

            print(
                f"   [{exemplo['referencia']}]"
            )

            print(
                "   " + exemplo["texto"]
            )

    print("\n" + "-" * 70)

    print(
        "Nota: a proximidade entre entidade e verbo "
        "não prova que a entidade seja o sujeito "
        "ou agente da ação. Cada passagem exige "
        "verificação gramatical e contextual."
    )


# ============================================================
# EXECUÇÃO DE UMA PESQUISA
# ============================================================

def executar_pesquisa(indice, tipo, termos):

    if tipo == 1:

        resultados = pesquisar_todos(
            indice,
            termos
        )

    elif tipo == 2:

        resultados = pesquisar_frase(
            indice,
            " ".join(termos)
        )

    elif tipo == 3:

        resultados = pesquisar_qualquer(
            indice,
            termos
        )

    elif tipo == 4:

        concordancia = pesquisar_concordancia(
            indice,
            set(termos)
        )

        print("\n" + "=" * 50)
        print("             CONCORDÂNCIA")
        print("=" * 50)

        if not concordancia:

            print(
                "Nenhuma ocorrência encontrada."
            )

        else:

            for palavra, quantidade in concordancia.most_common():

                print(
                    f"{palavra:<20} {quantidade:>6}"
                )

        return

    elif tipo == 5:

        resultados = pesquisar_qualquer(
            indice,
            termos
        )

    elif tipo == 6:

        analisar_contextos(
            indice,
            set(termos)
        )

        return

    elif tipo == 7:

        if len(termos) != 1:

            print(
                "\nPara esta análise introduz "
                "apenas uma entidade de cada vez."
            )

            print(
                "Exemplos: Deus, Jesus, Cristo, Moisés."
            )

            return

        analisar_relacoes(
            indice,
            termos[0]
        )

        return

    else:

        return

    print(
        "\nVersículos encontrados:",
        len(resultados)
    )

    estatisticas_por_livro(
        resultados
    )

    apresentar_resultados(
        resultados,
        termos_destaque=termos
    )


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal(indice):

    while True:

        print("\n" + "=" * 50)
        print("          ZIMOUS BIBLE STUDY")
        print("=" * 50)

        print("\n1 - Pesquisa por todos os termos")
        print("2 - Pesquisa por frase exata")
        print("3 - Pesquisa por qualquer termo")
        print("4 - Concordância")
        print("5 - Pesquisa por termos relacionados")
        print("6 - Análise contextual de expressões")
        print("7 - Análise de relações e afirmações")
        print("0 - Sair")

        print("-" * 50)

        escolha = input(
            "Escolhe uma operação: "
        ).strip()

        if escolha == "0":

            print(
                "\nA encerrar Zimous Bible Study."
            )

            break

        if escolha not in [
            "1", "2", "3", "4",
            "5", "6", "7"
        ]:

            print("Opção inválida.")
            continue

        tipo = int(escolha)

        if tipo == 5:

            termos = menu_termos_relacionados()

            if termos is None:
                continue

        else:

            pesquisa = input(
                "\nIntroduz a pesquisa: "
            ).strip()

            if not pesquisa:

                print("Pesquisa vazia.")
                continue

            if tipo == 2:

                termos = [pesquisa]

            else:

                termos = extrair_palavras(
                    pesquisa
                )

                if not termos:

                    print(
                        "Não foram encontrados termos válidos."
                    )

                    continue

        executar_pesquisa(
            indice,
            tipo,
            termos
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    livros = carregar_biblia()

    indice = preparar_indice(
        livros
    )

    print("\n" + "=" * 50)
    print("       ZIMOUS BIBLE STUDY")
    print("=" * 50)

    print(
        "Livros carregados:",
        len(livros)
    )

    print(
        "Versículos indexados:",
        len(indice)
    )

    menu_principal(
        indice
    )


if __name__ == "__main__":

    try:

        main()

    except Exception as erro:

        print("\nERRO:", erro)

        input(
            "\nPressiona ENTER para terminar..."
        )
