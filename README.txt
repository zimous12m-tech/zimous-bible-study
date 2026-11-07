ZIMOUS BIBLE STUDY
===================

ESTRUTURA ESPERADA
------------------
BIBLIA_STUDY/
  dados/
    biblia.json
  scripts/
    descarregar_biblia.py
    validar_biblia.py
  motor_pesquisa.py
  servidor.py
  index.html
  diagnostico_biblia.py
  README.txt

INSTALAÇÃO / EXECUÇÃO NO ANDROID
--------------------------------
1. Copia servidor.py e index.html para a pasta principal BIBLIA_STUDY,
   ao lado de motor_pesquisa.py.
2. Confirma que dados/biblia.json existe.
3. Abre o terminal/Pydroid na pasta BIBLIA_STUDY.
4. Executa:
      python servidor.py
5. Abre o navegador e visita:
      http://127.0.0.1:8765
6. Mantém o servidor em execução enquanto utilizas a interface.
7. Para parar, interrompe o processo no terminal.

O QUE ESTA VERSÃO JÁ FAZ
------------------------
- Lê a Bíblia a partir do JSON existente.
- Mostra a navegação dos livros e capítulos.
- Mostra os versículos do capítulo selecionado.
- Liga a interface às operações 1 a 7 do motor, através de uma API HTTP local.
- Adapta o layout a ecrãs pequenos.

NOTAS IMPORTANTES
-----------------
- Esta camada assume que motor_pesquisa.py disponibiliza:
    carregar_biblia()
    preparar_indice(livros)
    pesquisar_todos(indice, consulta)
    pesquisar_frase(indice, consulta)
    pesquisar_qualquer(indice, consulta)
    concordancia(indice, palavra)
    analisar_contextos(indice, consulta)
    analisar_relacoes(indice, entidade)
- A operação 5 utiliza GRUPOS_RELACIONADOS, se existir no motor.
- Se os nomes ou assinaturas das funções forem diferentes, a integração
  terá de ser ajustada ao código real do motor.
- O JSON atual contém Almeida 1911 em português. As secções Grego e
  Morfologia ficam identificadas como futuras; não simulam dados originais.
- O servidor escuta apenas em 127.0.0.1, não expõe a aplicação à rede local.

SEGURANÇA E CÓPIAS
------------------
Faz uma cópia de segurança de motor_pesquisa.py e biblia.json antes de
qualquer alteração. Esta versão não modifica esses ficheiros.
