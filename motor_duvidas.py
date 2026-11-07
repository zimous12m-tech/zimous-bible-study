# motor_duvidas.py
# Base curada de dúvidas e aparentes contradições
# Cada dúvida tem: resposta curta, contexto, explicação e versículos-chave

DUVIDAS = [
    {
        "id": "golias",
        "categoria": "Aparentes contradições",
        "pergunta": "Quem matou Golias? A Bíblia diz que foi Davi — mas também diz que foi Elanã?",
        "resposta_curta": "Foi Davi. A passagem de 2 Samuel 21:19 provavelmente refere-se a outro gigante, ou a uma cópia antiga com erro de escriba.",
        "contexto": "1 Samuel 17 narra Davi a matar Golias. 2 Samuel 21:19 menciona 'Elanã, filho de Jair, matou Golias'. Como resolver?",
        "explicacao": "Três factos: (1) 1 Crónicas 20:5, um texto paralelo, diz que Elanã matou 'Lahmi, irmão de Golias'. (2) A palavra hebraica para 'irmão' pode ter caído por erro de cópia. (3) O próprio 2 Samuel 21 lista outros gigantes filisteus mortos por heróis de Davi — não é uma recontagem da morte original. A explicação mais sólida: Elanã matou o irmão de Golias, ou outro gigante com nome semelhante. Erros de cópia existiam; os massoretas corrigiram ao longo dos séculos, e as versões paralelas confirmam.",
        "versiculos": ["1 Samuel 17:50", "2 Samuel 21:19", "1 Crónicas 20:5"],
        "veredito": "Sem contradição — passagem paralela esclarece.",
    },
    {
        "id": "criacao",
        "categoria": "Aparentes contradições",
        "pergunta": "Génesis 1 e Génesis 2 são duas criações diferentes?",
        "resposta_curta": "Não. São dois ângulos do mesmo acontecimento — um panorâmico, outro focado no ser humano.",
        "contexto": "Génesis 1 dá a ordem dos dias: luz, céu, terra, plantas, animais, homem. Génesis 2 'reinicia' e diz que o homem veio antes das plantas.",
        "explicacao": "O estilo hebraico antigo não é cronológico como o nosso. Génesis 1 é uma visão macro (o que aconteceu), Génesis 2 é uma visão micro (como o ser humano foi feito, e a instituição do casamento). O termo 'gerações' em Génesis 2:4 marca uma nova secção — não uma nova criação. Génesis 2 aprofunda o dia 6.",
        "versiculos": ["Génesis 1:1-31", "Génesis 2:4-25"],
        "veredito": "Sem contradição — dois géneros literários.",
    },
    {
        "id": "ressurreicao",
        "categoria": "Aparentes contradições",
        "pergunta": "Os quatro evangelhos dizem coisas diferentes sobre a ressurreição. É confiável?",
        "resposta_curta": "As diferenças são complementares, não contraditórias. É o que se espera de quatro testemunhas honestas.",
        "contexto": "Mateus, Marcos, Lucas e João diferem em quem viu, quantos anjos, e a ordem dos eventos.",
        "explicacao": "Testemunhos reais variam em detalhes sem se contradizerem. Se fossem idênticos palavra-a-palavra, diríamos que copiaram — como acontece com relatos falsos. As diferenças: número de anjos (Mateus menciona um, Lucas dois — um é subconjunto do outro), quem viu primeiro (Maria Madalena em João, várias mulheres nos sinópticos — todos verdadeiros). A mensagem central — o túmulo vazio, a ressurreição, a comissão — é idêntica nos quatro.",
        "versiculos": ["Mateus 28", "Marcos 16", "Lucas 24", "João 20"],
        "veredito": "Complementar, não contraditório.",
    },
    {
        "id": "judas",
        "categoria": "Aparentes contradições",
        "pergunta": "Judas morreu enforcado ou caiu e rebentou?",
        "resposta_curta": "As duas coisas. Enforcou-se, e o corpo caiu depois.",
        "contexto": "Mateus 27:5 diz 'enforcou-se'. Atos 1:18 diz 'caindo de cabeça, rebentou pelo meio'.",
        "explicacao": "Mateus descreve o ato, Atos descreve o resultado. É comum em relatos antigos complementares. Judas enforcou-se numa árvore, o ramo ou a corda cedeu, e o corpo caiu de grande altura — daí o resultado descrito em Atos. Os dois factos são compatíveis.",
        "versiculos": ["Mateus 27:3-10", "Atos 1:15-20"],
        "veredito": "Complementar.",
    },
    {
        "id": "arca",
        "categoria": "Aparentes contradições",
        "pergunta": "Quantos animais entraram na arca — dois de cada ou sete de cada?",
        "resposta_curta": "Dois de cada espécie 'impura', sete pares das 'puras'.",
        "contexto": "Génesis 6:19 diz 'dois de cada espécie'. Génesis 7:2 diz 'sete pares dos animais puros'.",
        "explicacao": "Não é contradição — são regras diferentes para categorias diferentes. Génesis 6 dá a regra geral ('dois de cada'). Génesis 7 detalha: os animais 'puros' (para sacrifício após o dilúvio) entram em sete pares; os 'impuros' em dois. A distinção puro/impuro já existia antes da Lei de Moisés (ver Génesis 7:2).",
        "versiculos": ["Génesis 6:19-20", "Génesis 7:2-3"],
        "veredito": "Regras diferentes para categorias diferentes.",
    },
    {
        "id": "genocidio",
        "categoria": "Sofrimento e mal",
        "pergunta": "Como pode um Deus bom ordenar a destruição de cidades inteiras no Antigo Testamento?",
        "resposta_curta": "A Bíblia descreve guerras antigas dentro do seu contexto histórico, com juízo divino sobre culturas de extrema violência — e Cristo revela o coração de Deus de forma definitiva.",
        "contexto": "Josué, Deuteronómio e outros livros mencionam ordens de destruir povos cananeus.",
        "explicacao": "Três pontos para considerar honestamente: (1) O contexto — os cananeus praticavam sacrifício de crianças, prostituição ritual e opressão extrema; Deus usou Israel como instrumento de juízo, como usaria a Babilónia contra Israel depois. (2) O género literário — os relatos de conquista usam hipérbole do antigo Oriente Próximo ('totalmente destruído' era fórmula, não censo literal — ver Josué 11:22 vs Juízes 1:27-28, onde esses povos continuam a existir). (3) A revelação progressiva — Cristo é a revelação plena de Deus (Hebreus 1:1-2). Não é desculpar; é contextualizar. Muitos teólogos sérios continuam a debater este ponto.",
        "versiculos": ["Deuteronómio 9:4-5", "Josué 11:22", "Juízes 1:27-28", "Hebreus 1:1-2", "João 14:9"],
        "veredito": "Tema difícil — não há resposta fácil. A Bíblia não esconde as dificuldades.",
    },
    {
        "id": "escravidao",
        "categoria": "Sofrimento e mal",
        "pergunta": "A Bíblia aprova a escravidão?",
        "resposta_curta": "A Bíblia regula a escravidão do mundo antigo e lança sementes que a aboliram — mas não a institui.",
        "contexto": "O Antigo Testamento fala de escravos; o Novo dá instruções a senhores e escravos.",
        "explicacao": "A escravidão bíblica era radicalmente diferente da escravidão colonial moderna: era sobretudo económica, com limite de 6 anos (Êxodo 21:2), com proteção (Deuteronómio 23:15-16), e com o princípio de que todo o ser humano é imagem de Deus (Génesis 1:27). O Novo Testamento não faz uma revolução social imediata, mas mina a instituição: Paulo diz a Filemon que o escravo Onésimo é 'irmão amado' — impensável na época. Foi a leitura bíblica que aboliu a escravidão no século XIX (Wilberforce, Lincoln). É progresso histórico, não aprovação.",
        "versiculos": ["Êxodo 21:2", "Génesis 1:27", "Filemon 1:16", "Gálatas 3:28"],
        "veredito": "A Bíblia regula e mina a escravidão; não a inventa.",
    },
    {
        "id": "dias",
        "categoria": "Fé e ciência",
        "pergunta": "A Bíblia diz que o mundo tem 6.000 anos?",
        "resposta_curta": "Não. A Bíblia não dá uma idade à Terra. 'Dia' em Génesis é debatido entre cristãos sérios.",
        "contexto": "Génesis 1 fala em 'dias'. Alguns calculam 6.000 anos a partir das genealogias.",
        "explicacao": "O texto hebraico 'yom' (dia) pode significar dia literal, era, ou período. As genealogias bíblicas têm saltos (Mateus 1 salta reis). Cristãos históricos como Agostinho e Orígenes não liam Génesis 1 literalmente. Hoje, cristãos sinceros defendem várias posições (jovem Terra, Terra antiga, evolução teísta). O ponto central de Génesis 1 não é o 'quando', é o 'quem' — Deus criou. A Bíblia não é um livro de ciência, mas não contradiz ciência verdadeira.",
        "versiculos": ["Génesis 1:1", "Salmos 90:4", "2 Pedro 3:8"],
        "veredito": "Cristãos debatem o 'como'; todos afirmam o 'quem'.",
    },
    {
        "id": "genealogias",
        "categoria": "Aparentes contradições",
        "pergunta": "As genealogias de Jesus em Mateus e Lucas são diferentes. Erro?",
        "resposta_curta": "Diferentes porque têm propósitos diferentes — uma é linha legal de José, outra é linha biológica de Maria (ou vice-versa).",
        "contexto": "Mateus 1 e Lucas 3 listam antepassados de Jesus — e diferem entre Davi e José.",
        "explicacao": "Mateus escreve para judeus e traça a linha real de Davi até José (pai legal). Lucas, médico e historiador, traça provavelmente a linhagem biológica de Maria (o 'genro' era chamado 'filho' na época — Lucas 3:23 diria 'José, como se pensava, filho de Eli'). Isto é aceite desde os primeiros séculos. As diferenças não são erros — são dois documentos legais diferentes, um para judeus, outro para gentios.",
        "versiculos": ["Mateus 1:1-17", "Lucas 3:23-38"],
        "veredito": "Duas linhagens complementares.",
    },
    {
        "id": "abandonaste",
        "categoria": "Jesus",
        "pergunta": "Por que Jesus gritou 'Deus meu, por que me abandonaste?' — Deus abandonou-o?",
        "resposta_curta": "Jesus estava a citar o Salmo 22 — o salmo da cruz — e a carregar o pecado do mundo.",
        "contexto": "Mateus 27:46 e Marcos 15:34 registam o grito.",
        "explicacao": "Duas coisas ao mesmo tempo: (1) Jesus cita o Salmo 22:1, que descreve profeticamente toda a cena da crucificação (mãos e pés traspassados, sorte sobre vestes, escárnio). Era uma citação — os judeus reconheciam o salmo inteiro. (2) Na cruz, Jesus carregou o pecado do mundo (2 Coríntios 5:21) — e a comunhão com o Pai foi quebrada por um instante. É o momento mais profundo da história: o Filho experimenta o abandono que nós merecíamos, para que nós nunca sejamos abandonados.",
        "versiculos": ["Mateus 27:46", "Salmos 22:1-18", "2 Coríntios 5:21"],
        "veredito": "Citação profética + substituição.",
    },
    {
        "id": "at_vs_nt",
        "categoria": "Bíblia em geral",
        "pergunta": "Por que Deus parece vingativo no Antigo Testamento e amoroso no Novo?",
        "resposta_curta": "Não é outro Deus. É a mesma paciência e santidade — a cruz revela o custo do perdão.",
        "contexto": "O Antigo Testamento tem juízos severos; o Novo fala de amor e graça.",
        "explicacao": "No Antigo Testamento, Deus também é amoroso (Êxodo 34:6-7 — 'misericordioso e piedoso, tardio em irar-se'). No Novo, Jesus também fala de juízo (Mateus 25). A diferença é o centro da história: no Antigo, o juízo é adiado e a graça é prometida; na cruz, o juízo cai sobre o próprio Deus encarnado — é aí que vemos simultaneamente a santidade e o amor de Deus em plenitude. Não são dois deuses — é a mesma história a chegar ao clímax.",
        "versiculos": ["Êxodo 34:6-7", "João 3:16-17", "Romanos 3:25-26", "Hebreus 1:1-3"],
        "veredito": "Um só Deus — revelação progressiva.",
    },
    {
        "id": "sofrimento",
        "categoria": "Sofrimento e mal",
        "pergunta": "Se Deus é bom, por que existe tanto sofrimento?",
        "resposta_curta": "Deus não é a causa do mal. Escolheu criar um mundo com liberdade — e escolheu entrar no sofrimento.",
        "contexto": "A pergunta mais antiga da humanidade. O livro de Job dedica 42 capítulos a ela.",
        "explicacao": "Três pontos: (1) A Bíblia não minimiza — Job grita, os salmos lamentam, Jeremias chora. O sofrimento é real. (2) A Bíblia localiza a origem do mal na liberdade — humana e angelical — não em Deus. Sem liberdade não há amor. (3) A resposta central do cristianismo não é um argumento, é uma pessoa: Deus entrou no sofrimento. Jesus sofreu injustiça, tortura e morte — não à distância, mas pessoalmente. A promessa não é 'não vais sofrer', é 'não estás sozinho, e a história terá fim'. Apocalipse 21:4 — 'não haverá mais morte, nem pranto'.",
        "versiculos": ["Job 1-2", "Romanos 5:12", "João 11:35", "Apocalipse 21:4"],
        "veredito": "Deus não explica todo o sofrimento — entra nele.",
    },
    {
        "id": "oracao",
        "categoria": "Bíblia em geral",
        "pergunta": "Se Deus já sabe tudo, por que orar?",
        "resposta_curta": "Oração não é informar Deus — é relacionamento. Muda-nos enquanto Deus age.",
        "contexto": "Mateus 6:8 diz 'vosso Pai sabe do que tendes necessidade, antes de lho pedirdes'.",
        "explicacao": "A Bíblia apresenta a oração como diálogo, não como pedido a um distribuidor. Deus escolheu agir em resposta à oração (Tiago 5:16). Não é que a oração mude a mente de Deus — é que Deus decidiu um mundo onde a oração importa. Além disso, a oração muda quem ora: alinha-nos, acalma-nos, abre-nos para ver. É por isso que Filipenses 4:6-7 promete paz na oração — não como resposta garantida, mas como transformação de quem entrega.",
        "versiculos": ["Mateus 6:8", "Tiago 5:16", "Filipenses 4:6-7", "Lucas 18:1-8"],
        "veredito": "Oração é relação — não informação.",
    },
    {
        "id": "inferno",
        "categoria": "Bíblia em geral",
        "pergunta": "Inferno existe mesmo? Como um Deus de amor pode enviar alguém para lá?",
        "resposta_curta": "Jesus falou mais de inferno do que qualquer outro. A questão é: aceitamos o convite ou recusamos?",
        "contexto": "O tema 'inferno' aparece em Mateus, Marcos, Lucas e Apocalipse.",
        "explicacao": "A Bíblia fala de 'gehenna' e 'sheol/hades' com imagens — fogo, trevas, choro. Cristãos históricos debatem se é eterno consciente, aniquilação ou restauração (Gregory of Nyssa acreditava em restauração, Agostinho em eterno). O que a Bíblia é clara: (1) o inferno não foi feito para pessoas, mas para o diabo (Mateus 25:41); (2) Deus 'não quer que nenhum pereça' (2 Pedro 3:9); (3) só entra quem recusa o convite — o inferno é o resultado de rejeitar o amor de Deus até ao fim. Não é Deus a enviar, é a pessoa a fechar a porta de dentro.",
        "versiculos": ["Mateus 25:41", "2 Pedro 3:9", "Lucas 16:19-31", "Apocalipse 20:11-15"],
        "veredito": "Tema sério — a Bíblia descreve; cristãos debatem detalhes.",
    },
    {
        "id": "denominacoes",
        "categoria": "Bíblia em geral",
        "pergunta": "Por que existem tantas igrejas diferentes? Qual é a certa?",
        "resposta_curta": "As denominações divergem em pontos secundários. O essencial é comum — e é isso que define se és cristão.",
        "contexto": "Católicos, ortodoxos, protestantes, evangélicos, pentecostais — cada um com nuances.",
        "explicacao": "O Credo dos Apóstolos (séc. II) resume o essencial: Deus criador, Jesus Salvador, Espírito Santo, ressurreição. As denominações surgiram historicamente por questões de governança, liturgia, interpretação de sacramentos e ênfases espirituais. Duas igrejas podem divergir em batismo infantil e ambas serem cristãs. O que definiria uma seita: negar que Jesus é Deus encarnado, negar a ressurreição corporal, negar a autoridade da Bíblia. A 'certa' é a que ensina a Bíblia fielmente — e onde vês fruto real (Gálatas 5:22-23).",
        "versiculos": ["1 Coríntios 1:10-13", "Efésios 4:1-6", "Gálatas 5:22-23"],
        "veredito": "Unidade no essencial; liberdade no secundário.",
    },
]


class MotorDuvidas:
    def __init__(self):
        self.duvidas = DUVIDAS

    def listar(self):
        return [
            {
                "id": d["id"],
                "categoria": d["categoria"],
                "pergunta": d["pergunta"],
                "resposta_curta": d["resposta_curta"],
            }
            for d in self.duvidas
        ]

    def categorias(self):
        cats = []
        for d in self.duvidas:
            if d["categoria"] not in cats:
                cats.append(d["categoria"])
        return cats

    def detalhe(self, duvida_id):
        for d in self.duvidas:
            if d["id"] == duvida_id:
                return d
        return None

    def pesquisar(self, termo):
        termo = termo.lower().strip()
        if not termo:
            return []
        return [
            d for d in self.duvidas
            if termo in d["pergunta"].lower()
            or termo in d["resposta_curta"].lower()
            or termo in d["explicacao"].lower()
        ]