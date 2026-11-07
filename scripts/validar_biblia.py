
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BIBLE_FILE = BASE_DIR / "dados" / "biblia.json"

with open(BIBLE_FILE, "r", encoding="utf-8") as f:
    bible = json.load(f)

books = bible["books"]

print("=" * 45)
print("VALIDAÇÃO — ZIMOUS BIBLE STUDY")
print("=" * 45)

print("Versão:", bible.get("version"))
print("Livros:", len(books))

total_chapters = 0
total_verses = 0

for book in books:

    if not isinstance(book, dict):
        continue

    name = book.get("name", book.get("abbrev", "Desconhecido"))

    chapters = book.get("chapters", [])

    if not isinstance(chapters, list):
        continue

    total_chapters += len(chapters)

    for chapter in chapters:

        if isinstance(chapter, list):
            total_verses += len(chapter)

        elif isinstance(chapter, dict):
            verses = chapter.get("verses", [])
            total_verses += len(verses)

print("Capítulos:", total_chapters)
print("Versículos:", total_verses)

print("=" * 45)

print("AMOSTRA DA ESTRUTURA:")
print(json.dumps(books[0], ensure_ascii=False, indent=2)[:2000])

print("=" * 45)
