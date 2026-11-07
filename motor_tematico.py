# motor_tematico.py
# Motor de Estudo Temático — Zimous Bible Study
# Curadoria por tema: o que Deus diz, exemplos, soluções, versículos-chave

import json
import os
from pathlib import Path
import unicodedata
import re


# ============================================================
# BIBLIOTECA DE TEMAS CURADOS
# Cada tema tem: perspetiva de Deus, exemplos bíblicos,
# soluções práticas, versículos-chave e termos de pesquisa
# ============================================================

TEMAS = {
    "depressao": {
        "titulo": "Depressão e tristeza profunda",
        "icone": "🌧",
        "cor": "#5b8bbf",
        "resumo": "Quando a alma está abatida e não há vontade de continuar.",
        "gatilhos": ["deprimid", "depress", "triste", "vazio", "sem vontade", "abatid", "desanim", "desesper", "sem forças"],
        "perspetiva_deus": {
            "titulo": "Deus não te abandona na escuridão",
            "texto": "A Bíblia mostra um Deus que se aproxima dos quebrantados, não que se afasta. O próprio Jesus sentiu angústia profunda (Mateus 26:38). Não estás sozinho — e não é pecado sentir o que sentes.",
            "versiculos": ["Salmos 34:18", "Salmos 42:11", "Isaías 41:10", "Mateus 5:4"],
        },
        "exemplos": [
            {"nome": "Davi", "referencia": "Salmos 42:5-11", "resumo": "Escreveu salmos de pura angústia e, no mesmo texto, fala à própria alma para esperar em Deus."},
            {"nome": "Job", "referencia": "Job 3:1-26", "resumo": "Amaldiçoou o dia do seu nascimento — e Deus não o castigou por isso. Falar a verdade é o começo da cura."},
            {"nome": "Elias", "referencia": "1 Reis 19:3-8", "resumo": "Queria morrer, e Deus respondeu-lhe com sono, comida e uma voz mansa — não com repreensão."},
        ],
        "solucoes": [
            {"titulo": "Fala com Deus com honestidade", "referencia": "Salmos 62:8", "texto": "A Bíblia não pede que finjas. Derrama o teu coração — mesmo com raiva, dúvida ou queixa."},
            {"titulo": "Não te isoles — deixa outros carregarem contigo", "referencia": "Eclesiastes 4:9-10", "texto": "Solidão alimenta depressão. Comunidade é remédio. Procura um irmão, um pastor, um amigo."},
            {"titulo": "Espera — a noite não dura para sempre", "referencia": "Salmos 30:5", "texto": "A promessa não é que nunca chores, mas que o choro tem fim."},
        ],
        "versiculos_chave": ["Salmos 34:18", "Salmos 42:5", "Salmos 62:8", "Isaías 41:10", "Mateus 11:28-30"],
        "termos_pesquisa": ["triste", "chor", "lament", "consol", "angust", "desanim", "abatid", "socorro", "esperança"],
    },
    "ansiedade": {
        "titulo": "Ansiedade, medo e preocupação",
        "icone": "🌊",
        "cor": "#4a9b9b",
        "resumo": "Quando o coração está acelerado e o futuro pesa.",
        "gatilhos": ["ansios", "ansiedade", "medo", "pânico", "preocup", "receio", "nervos", "estresse"],
        "perspetiva_deus": {
            "titulo": "Deus cuida — podes largar",
            "texto": "Deus não te pede para não ter medo 'porque sim'. Pede porque Ele está contigo. O medo é real, mas não é a última palavra sobre a tua vida.",
            "versiculos": ["Filipenses 4:6-7", "Isaías 41:10", "1 Pedro 5:7", "Mateus 6:25-34"],
        },
        "exemplos": [
            {"nome": "David", "referencia": "Salmos 3:5-6", "resumo": "Cercado de exércitos, dormiu em paz porque sabia quem o guardava."},
            {"nome": "Josafá", "referencia": "2 Crónicas 20:1-13", "resumo": "Com um exército enorme a caminho, reuniu o povo para orar — e Deus lutou por eles."},
            {"nome": "Jesus", "referencia": "Marcos 4:35-41", "resumo": "Em tempestade real, dormia. Depois acalmou o mar — e o coração dos discípulos."},
        ],
        "solucoes": [
            {"titulo": "Entrega a ansiedade em oração específica", "referencia": "Filipenses 4:6-7", "texto": "Oração com gratidão troca a espiral de pensamentos por uma paz que 'excede todo o entendimento'."},
            {"titulo": "Vive o dia de hoje", "referencia": "Mateus 6:34", "texto": "Ansiedade vive no amanhã. Deus dá graça para o hoje. Basta o mal de cada dia."},
            {"titulo": "Lança o teu cuidado sobre Ele — não o segures", "referencia": "1 Pedro 5:7", "texto": "A palavra original é 'lançar', não 'guardar'. Ele cuida."},
        ],
        "versiculos_chave": ["Filipenses 4:6-7", "1 Pedro 5:7", "Mateus 6:25-34", "Isaías 41:10", "Salmos 23"],
        "termos_pesquisa": ["medo", "temor", "ansios", "paz", "refúgio", "confian", "cuidado", "descans"],
    },
    "solidao": {
        "titulo": "Solidão e abandono",
        "icone": "🌙",
        "cor": "#7a5fa3",
        "resumo": "Quando sentes que ninguém está contigo.",
        "gatilhos": ["solidão", "solid", "sozinh", "abandon", "ninguém", "isolad", "esquecid"],
        "perspetiva_deus": {
            "titulo": "Deus promete: 'nunca te deixarei'",
            "texto": "A presença de Deus não depende de sentires. Ele prometeu estar — e não falha.",
            "versiculos": ["Deuteronómio 31:6", "Salmos 139:7-12", "Hebreus 13:5", "Mateus 28:20"],
        },
        "exemplos": [
            {"nome": "José", "referencia": "Génesis 39:21", "resumo": "Preso no Egito, longe de todos — mas 'o Senhor era com José'."},
            {"nome": "Jesus", "referencia": "João 16:32", "resumo": "Os discípulos iam abandoná-lo, e Ele disse: 'não estou só, o Pai está comigo'."},
        ],
        "solucoes": [
            {"titulo": "Procura comunidade ativa", "referencia": "Hebreus 10:24-25", "texto": "Fé não foi feita para ser vivida sozinha. Junta-te a outros crentes."},
            {"titulo": "Serve — a solidão foge quando serves", "referencia": "Filipenses 2:4", "texto": "Olhar para as necessidades dos outros quebra o ciclo de olhar só para dentro."},
        ],
        "versiculos_chave": ["Salmos 139:1-18", "Deuteronómio 31:6", "Hebreus 13:5", "Salmos 23:4"],
        "termos_pesquisa": ["sozinh", "solid", "abandon", "nunca deixar", "companheir", "presença"],
    },
    "luto": {
        "titulo": "Morte, luto e perda",
        "icone": "🕯",
        "cor": "#8a7a5a",
        "resumo": "Quando alguém que amamos parte.",
        "gatilhos": ["morte", "luto", "morreu", "faleceu", "perda", "perdemos", "saudade"],
        "perspetiva_deus": {
            "titulo": "A morte não é o fim",
            "texto": "A Bíblia não minimiza a dor da perda. Mas promete ressurreição — o luto tem esperança.",
            "versiculos": ["1 Tessalonicenses 4:13-14", "João 11:25-26", "Apocalipse 21:4", "Salmos 116:15"],
        },
        "exemplos": [
            {"nome": "Jesus", "referencia": "João 11:35", "resumo": "Chorou na sepultura de Lázaro — mesmo sabendo que o iria ressuscitar. A dor é real e legítima."},
            {"nome": "Davi", "referencia": "2 Samuel 12:16-23", "resumo": "Chorou e jejuou pela vida do filho. Depois levantou-se — luto tem tempo e depois tem passo."},
        ],
        "solucoes": [
            {"titulo": "Chora — não te justifiques", "referencia": "Eclesiastes 3:4", "texto": "Há tempo de chorar. Deus não espera que sejas forte em 24 horas."},
            {"titulo": "Aguarda com esperança", "referencia": "1 Tessalonicenses 4:13", "texto": "A dor dos que têm esperança é diferente: não é sem esperança."},
        ],
        "versiculos_chave": ["João 11:25-26", "1 Tessalonicenses 4:13-18", "Apocalipse 21:4", "Salmos 23"],
        "termos_pesquisa": ["morte", "morrer", "luto", "chor", "consol", "ressurrei", "viv"],
    },
    "dinheiro": {
        "titulo": "Dinheiro, pobreza e provisão",
        "icone": "🪙",
        "cor": "#c9a24a",
        "resumo": "Quando as contas não fecham ou o dinheiro virou ídolo.",
        "gatilhos": ["dinheiro", "dívida", "pobre", "falta", "desempreg", "riqueza", "avareza", "mamo"],
        "perspetiva_deus": {
            "titulo": "Deus é o teu provedor",
            "texto": "O dinheiro é ferramenta, não senhor. Deus promete prover o necessário — e adverte contra a ansiedade que escraviza.",
            "versiculos": ["Mateus 6:25-34", "Filipenses 4:19", "Provérbios 3:9-10", "1 Timóteo 6:10"],
        },
        "exemplos": [
            {"nome": "Elias e a viúva de Sarepta", "referencia": "1 Reis 17:8-16", "resumo": "Farinha e azeite não acabaram — Deus provê de formas improváveis."},
            {"nome": "Jesus e a moeda no peixe", "referencia": "Mateus 17:24-27", "resumo": "Até imposto foi pago de modo milagroso. Detalhes pequenos não escapam a Deus."},
        ],
        "solucoes": [
            {"titulo": "Busca primeiro o Reino", "referencia": "Mateus 6:33", "texto": "O resto é acrescentado. Alinhar prioridades desbloqueia provisão."},
            {"titulo": "Foge do amor ao dinheiro", "referencia": "1 Timóteo 6:10", "texto": "O problema não é o dinheiro — é o amor a ele. Contentamento é a chave."},
        ],
        "versiculos_chave": ["Mateus 6:25-34", "Filipenses 4:19", "Provérbios 3:5-10", "Malaquias 3:10"],
        "termos_pesquisa": ["dinheiro", "riqueza", "pobre", "provisão", "dívida", "pão", "necessidade", "contentamento"],
    },
    "familia": {
        "titulo": "Família, casamento e filhos",
        "icone": "🏠",
        "cor": "#c97a5b",
        "resumo": "Conflitos em casa, criação de filhos, casamento difícil.",
        "gatilhos": ["família", "famili", "casamento", "marido", "esposa", "filho", "filha", "pai", "mãe", "divórcio", "briga"],
        "perspetiva_deus": {
            "titulo": "A família é projeto de Deus",
            "texto": "Deus criou a família como lugar de amor sacrificial. Não é fácil — mas há princípios claros.",
            "versiculos": ["Efésios 5:21-33", "Colossenses 3:18-21", "Provérbios 22:6", "Deuteronómio 6:6-7"],
        },
        "exemplos": [
            {"nome": "Abraão e Sara", "referencia": "Génesis 21", "resumo": "Esperaram 25 anos pelo filho. A paciência de Deus é maior que a nossa pressa."},
            {"nome": "Boaz e Rute", "referencia": "Rute 4", "resumo": "Amor maduro: proteção, escolha consciente e compromisso diante da comunidade."},
        ],
        "solucoes": [
            {"titulo": "Ama com sacrifício, não com sentimento", "referencia": "Efésios 5:25-28", "texto": "O amor conjugal é decisão prática, não emoção passageira."},
            {"titulo": "Cria com instrução e graça", "referencia": "Efésios 6:4", "texto": "Não provoques — disciplina com amor, não com raiva."},
        ],
        "versiculos_chave": ["Efésios 5:21-33", "Colossenses 3:18-21", "Provérbios 22:6", "1 Coríntios 13"],
        "termos_pesquisa": ["família", "marido", "esposa", "filho", "pai", "mãe", "casament", "cri", "amor"],
    },
    "perdao": {
        "titulo": "Perdão, mágoa e ofensa",
        "icone": "🤲",
        "cor": "#8fb98b",
        "resumo": "Quando perdoar é a coisa mais difícil do mundo.",
        "gatilhos": ["perdão", "perdo", "mágoa", "mago", "ofensa", "vingança", "ving", "traição", "reconcilia"],
        "perspetiva_deus": {
            "titulo": "Deus perdoa-te; por isso podes perdoar",
            "texto": "O perdão não é dizer que não doeu. É libertar-te da dívida. Deus fez isso contigo primeiro.",
            "versiculos": ["Mateus 18:21-22", "Efésios 4:32", "Colossenses 3:13", "Mateus 6:14-15"],
        },
        "exemplos": [
            {"nome": "José", "referencia": "Génesis 45:4-8", "resumo": "Traído pelos irmãos, tornou-se governador — e perdoou. 'Vós pensastes mal, mas Deus pensou bem'."},
            {"nome": "Estêvão", "referencia": "Atos 7:59-60", "resumo": "Apedrejado, orou: 'Senhor, não lhes imputes este pecado.' Perdão até ao fim."},
            {"nome": "Jesus", "referencia": "Lucas 23:34", "resumo": "Na cruz: 'Pai, perdoa-lhes.' O perdão mais radical da história."},
        ],
        "solucoes": [
            {"titulo": "Perdoa 70×7 — não é número, é postura", "referencia": "Mateus 18:22", "texto": "Perdão é decisão repetida, não sentimento único."},
            {"titulo": "Lembra-te de quanto te foi perdoado", "referencia": "Mateus 18:21-35", "texto": "A parábola do servo mostra: quem sabe que foi perdoado muito, perdoa muito."},
        ],
        "versiculos_chave": ["Mateus 18:21-22", "Efésios 4:32", "Colossenses 3:13", "Lucas 23:34"],
        "termos_pesquisa": ["perd", "perdo", "mágoa", "ving", "ofens", "reconcilia", "amor"],
    },
    "culpa": {
        "titulo": "Culpa, vergonha e arrependimento",
        "icone": "🕊",
        "cor": "#a8b8c8",
        "resumo": "Quando o peso do que fizeste não te deixa respirar.",
        "gatilhos": ["culpa", "culpad", "vergonha", "arrepend", "pecad", "erro", "falhei"],
        "perspetiva_deus": {
            "titulo": "Há perdão — e ele é completo",
            "texto": "Deus não te trata como a culpa diz. Se confessas, Ele perdoa — e afasta o pecado como o Oriente do Ocidente.",
            "versiculos": ["1 João 1:9", "Salmos 103:12", "Romanos 8:1", "Isaías 1:18"],
        },
        "exemplos": [
            {"nome": "Davi", "referencia": "Salmos 51", "resumo": "Depois do adultério com Bate-Seba, escreveu o salmo do arrependimento — e foi perdoado."},
            {"nome": "Pedro", "referencia": "João 21:15-19", "resumo": "Negou Jesus três vezes; Jesus restaurou-o três vezes. A culpa não é o fim."},
            {"nome": "Paulo", "referencia": "1 Timóteo 1:15", "resumo": "Perseguiu a igreja — e chamou-se 'o principal dos pecadores'. Deus usou-o poderosamente."},
        ],
        "solucoes": [
            {"titulo": "Confessa — não esconde", "referencia": "1 João 1:9", "texto": "Confissão não é informar Deus; é alinhar-te com a verdade."},
            {"titulo": "Aceita o perdão — não voltes a ele", "referencia": "Romanos 8:1", "texto": "Não há condenação. Se Deus não condena, porque te condenas tu?"},
        ],
        "versiculos_chave": ["1 João 1:9", "Salmos 51", "Salmos 103:12", "Romanos 8:1", "Isaías 1:18"],
        "termos_pesquisa": ["culpa", "vergonh", "arrepend", "perd", "confess", "pecad", "purific"],
    },
    "fe": {
        "titulo": "Fé, dúvida e crises espirituais",
        "icone": "✨",
        "cor": "#d4b96a",
        "resumo": "Quando Deus parece distante ou as respostas não vêm.",
        "gatilhos": ["fé", "duvid", "crise", "deus não", "silêncio", "afastad", "descrente", "incrédul"],
        "perspetiva_deus": {
            "titulo": "Dúvida não é o oposto de fé — é parte dela",
            "texto": "Os maiores homens da Bíblia duvidaram. Tomé duvidou. Deus não rejeita o que pergunta — rejeita o que finge.",
            "versiculos": ["Marcos 9:24", "João 20:24-29", "Hebreus 11:1", "Tiago 1:5-6"],
        },
        "exemplos": [
            {"nome": "Tomé", "referencia": "João 20:24-29", "resumo": "Disse que não acreditaria sem ver — e Jesus mostrou-lhe as mãos. Dúvida honesta é acolhida."},
            {"nome": "Habacuque", "referencia": "Habacuque 1:1-4", "resumo": "Perguntou a Deus por que o mal prospera. Deus respondeu — e ele aprendeu a esperar."},
            {"nome": "Jó", "referencia": "Job 23:8-10", "resumo": "Não sentia Deus — mas disse: 'Ele sabe o meu caminho'. Fé é confiar sem sentir."},
        ],
        "solucoes": [
            {"titulo": "Traz a dúvida a Deus, não a escondas", "referencia": "Marcos 9:24", "texto": "'Creio, ajuda a minha incredulidade' — oração honesta é aceite."},
            {"titulo": "Alimenta a fé com a Palavra, não com sentimento", "referencia": "Romanos 10:17", "texto": "Fé vem por ouvir. Ler a Bíblia mesmo sem vontade é o caminho."},
        ],
        "versiculos_chave": ["Marcos 9:24", "João 20:24-29", "Hebreus 11:1-6", "Salmos 42:11"],
        "termos_pesquisa": ["fé", "crer", "duvid", "incredul", "esper", "confian", "orac"],
    },
    "raiva": {
        "titulo": "Raiva, injustiça e vingança",
        "icone": "🔥",
        "cor": "#c87869",
        "resumo": "Quando a injustiça te consome e queres justiça pelas tuas mãos.",
        "gatilhos": ["raiva", "ira", "ódio", "injustiça", "justiça", "vingança", "revolt", "indign"],
        "perspetiva_deus": {
            "titulo": "Deus é justo — e luta por ti",
            "texto": "A raiva não é pecado; a raiva que age sem Deus é. A Bíblia reconhece a dor da injustiça e promete justiça divina.",
            "versiculos": ["Efésios 4:26-27", "Romanos 12:19", "Salmos 37:1-11", "Tiago 1:19-20"],
        },
        "exemplos": [
            {"nome": "Davi", "referencia": "1 Samuel 24", "resumo": "Podia matar Saul — não matou. Deixou a justiça nas mãos de Deus."},
            {"nome": "Jesus", "referencia": "João 2:13-17", "resumo": "Irou-se justamente contra a corrupção do templo. Raiva santa existe — direcionada a injustiça real."},
        ],
        "solucoes": [
            {"titulo": "Ira sem pecar — não deixes o sol pôr-se", "referencia": "Efésios 4:26", "texto": "Sentir raiva é legítimo; alimentá-la é o problema."},
            {"titulo": "Deixa a vingança para Deus", "referencia": "Romanos 12:19", "texto": "'Minha é a vingança' — Ele vê o que ninguém vê."},
        ],
        "versiculos_chave": ["Efésios 4:26-31", "Romanos 12:17-21", "Salmos 37", "Tiago 1:19-20"],
        "termos_pesquisa": ["ira", "raiva", "justiça", "ving", "injust", "juiz", "revolt"],
    },
}


class MotorTematico:
    def __init__(self, caminho_biblia="dados/biblia.json"):
        base_dir = Path(__file__).resolve().parent
        self.caminho_biblia = base_dir / caminho_biblia
        self.dados_biblia = self.carregar_biblia()

    def normalizar(self, texto):
        texto = str(texto).casefold()
        texto = unicodedata.normalize("NFD", texto)
        return "".join(c for c in texto if unicodedata.category(c) != "Mn")

    def carregar_biblia(self):
        try:
            if os.path.exists(self.caminho_biblia):
                with open(self.caminho_biblia, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    return dados.get("books", []) if isinstance(dados, dict) else dados
        except Exception as e:
            print(f"Erro ao carregar a Bíblia: {e}")
        return []

    # ---------------------------------------------------------
    # Resolver "Isaías 41:10" ou "Salmos 42:1-5" para texto real
    # ---------------------------------------------------------
    def buscar_referencia(self, ref_str):
        m = re.match(r"^(.+?)\s+(\d+):(.+)$", ref_str.strip())
        if not m:
            return None
        livro_alvo, cap_str, verses_str = m.groups()
        cap_num = int(cap_str)

        livro_alvo_norm = self.normalizar(livro_alvo)
        livro = None
        for l in self.dados_biblia:
            nome_norm = self.normalizar(l.get("name", ""))
            abrev_norm = self.normalizar(l.get("abbrev", ""))
            if nome_norm == livro_alvo_norm or abrev_norm == livro_alvo_norm:
                livro = l
                break
        if not livro:
            return None

        for cap in livro.get("chapters", []):
            if cap.get("number") != cap_num:
                continue
            mapa = {v.get("number"): v.get("text", "") for v in cap.get("verses", [])}
            versos = []
            for parte in verses_str.split(","):
                parte = parte.strip()
                if "-" in parte:
                    a, b = parte.split("-")
                    for n in range(int(a), int(b) + 1):
                        if n in mapa:
                            versos.append({"number": n, "text": mapa[n]})
                else:
                    n = int(parte)
                    if n in mapa:
                        versos.append({"number": n, "text": mapa[n]})
            return {"referencia": ref_str, "livro": livro.get("name"), "capitulo": cap_num, "versiculos": versos}
        return None

    # ---------------------------------------------------------
    # Encontrar tema por gatilho (situação do utilizador)
    # ---------------------------------------------------------
    def encontrar_tema(self, input_utilizador):
        inp = self.normalizar(input_utilizador)
        melhor = None
        melhor_score = 0
        for chave, dados in TEMAS.items():
            score = 0
            for gat in dados["gatilhos"]:
                if gat in inp:
                    score += len(gat)
            if score > melhor_score:
                melhor_score = score
                melhor = chave
        return melhor

    # ---------------------------------------------------------
    # Pesquisa ampla (prefixo) para preencher versículos extra
    # ---------------------------------------------------------
    def pesquisa_diversa(self, termos, limite=12):
        resultados = []
        for livro in self.dados_biblia:
            nome = livro.get("name", "?")
            for cap in livro.get("chapters", []):
                num_cap = cap.get("number")
                for v in cap.get("verses", []):
                    texto = v.get("text", "")
                    tokens = re.findall(r"\w+", self.normalizar(texto))
                    if any(any(tok.startswith(t) for t in termos) for tok in tokens):
                        resultados.append({
                            "referencia": f"{nome} {num_cap}:{v.get('number')}",
                            "texto": texto,
                        })
        # Amostragem diversa (não só o início)
        if len(resultados) <= limite:
            return resultados
        passo = len(resultados) / limite
        return [resultados[int(i * passo)] for i in range(limite)]

    # ---------------------------------------------------------
    # Análise principal
    # ---------------------------------------------------------
    def analisar_tema(self, input_utilizador):
        chave = self.encontrar_tema(input_utilizador)

        if not chave:
            # Tema livre: devolve o que encontrar
            termos = [self.normalizar(input_utilizador)]
            return {
                "sucesso": True,
                "personalizado": True,
                "tema": {
                    "titulo": f"Sobre: {input_utilizador}",
                    "icone": "🔍",
                    "cor": "#c5a66d",
                    "resumo": "Resultados encontrados para a tua pesquisa.",
                    "pesquisa_ampliada": self.pesquisa_diversa(termos, 20),
                },
            }

        dados = TEMAS[chave]

        # Resolver versículos curados
        perspetiva = {
            "titulo": dados["perspetiva_deus"]["titulo"],
            "texto": dados["perspetiva_deus"]["texto"],
            "versiculos": [
                r for r in (self.buscar_referencia(x) for x in dados["perspetiva_deus"]["versiculos"])
                if r
            ],
        }

        exemplos = []
        for ex in dados["exemplos"]:
            v = self.buscar_referencia(ex["referencia"])
            if v:
                exemplos.append({**ex, "versiculo": v})

        solucoes = []
        for s in dados["solucoes"]:
            v = self.buscar_referencia(s["referencia"])
            if v:
                solucoes.append({**s, "versiculo": v})

        versiculos_chave = [
            r for r in (self.buscar_referencia(x) for x in dados["versiculos_chave"])
            if r
        ]

        pesquisa_ampliada = self.pesquisa_diversa(dados["termos_pesquisa"], 10)

        return {
            "sucesso": True,
            "personalizado": False,
            "tema": {
                "id": chave,
                "titulo": dados["titulo"],
                "icone": dados["icone"],
                "cor": dados["cor"],
                "resumo": dados["resumo"],
                "perspetiva_deus": perspetiva,
                "exemplos": exemplos,
                "solucoes": solucoes,
                "versiculos_chave": versiculos_chave,
                "pesquisa_ampliada": pesquisa_ampliada,
            },
        }

    # ---------------------------------------------------------
    # Listar todos os temas (para o grid inicial)
    # ---------------------------------------------------------
    def listar_temas(self):
        return [
            {
                "id": chave,
                "titulo": d["titulo"],
                "icone": d["icone"],
                "cor": d["cor"],
                "resumo": d["resumo"],
            }
            for chave, d in TEMAS.items()
        ]