
import json
import urllib.request
from pathlib import Path
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO DO PROJETO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "dados"

DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "biblia.json"

API_URL = (
    "https://api.github.com/repos/"
    "damarals/biblias/contents/"
    "data/canonical/ALM1911"
)

HEADERS = {
    "User-Agent": "Zimous-Bible-Study/1.0",
    "Accept": "application/vnd.github+json"
}


def download_json(url):

    request = urllib.request.Request(
        url,
        headers=HEADERS
    )

    with urllib.request.urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode("utf-8"))


def main():

    print("=" * 50)
    print("       ZIMOUS BIBLE STUDY")
    print("       DOWNLOAD DA BÍBLIA")
    print("=" * 50)

    try:

        print("\nA procurar os livros da Bíblia...")

        files = download_json(API_URL)

        books = []

        json_files = [
            item for item in files
            if item["name"].lower().endswith(".json")
        ]

        if not json_files:
            raise Exception(
                "Não foram encontrados ficheiros JSON."
            )

        total = len(json_files)

        print(f"\nForam encontrados {total} ficheiros.")

        for index, item in enumerate(json_files, 1):

            name = item["name"]

            print(
                f"[{index}/{total}] A descarregar {name}..."
            )

            book = download_json(item["download_url"])

            books.append(book)

        bible = {
            "project": "Zimous Bible Study",
            "version": "ALM1911",
            "translation": "Almeida 1911",
            "language": "pt",
            "download_date": datetime.now().isoformat(),
            "source": "damarals/biblias",
            "license": "Public Domain",
            "total_books": len(books),
            "books": books
        }

        print("\nA guardar a Bíblia em JSON...")

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                bible,
                file,
                ensure_ascii=False,
                indent=2
            )

        print("\n" + "=" * 50)
        print("DOWNLOAD CONCLUÍDO!")
        print("=" * 50)

        print(f"Livros: {len(books)}")
        print(f"Ficheiro: {OUTPUT_FILE}")
        print(f"Tamanho: {OUTPUT_FILE.stat().st_size / 1024:.2f} KB")

    except Exception as error:

        print("\nERRO NO DOWNLOAD:")
        print(error)


if __name__ == "__main__":
    main()
