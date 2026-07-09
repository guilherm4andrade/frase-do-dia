import json
import os
import random
import sys
import urllib.error
import urllib.request

from generate_card import generate

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
IMAGE_BLOCK_ID = os.environ["IMAGE_BLOCK_ID"]  # ID do bloco IMAGE dentro do callout
IMAGE_PUBLIC_URL = os.environ["IMAGE_PUBLIC_URL"]  # URL pública do GitHub Pages (docs/frase.png)
QUOTES_PATH = os.path.join(os.path.dirname(__file__), "quotes.json")
STATE_PATH = os.path.join(os.path.dirname(__file__), "last_index.txt")
IMAGE_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "docs", "frase.png")

NOTION_VERSION = "2022-06-28"
API_URL = f"https://api.notion.com/v1/blocks/{IMAGE_BLOCK_ID}"


def load_quotes():
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_quote(quotes):
    last_index = -1
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content.isdigit():
                last_index = int(content)

    candidates = [i for i in range(len(quotes)) if i != last_index]
    new_index = random.choice(candidates)

    with open(STATE_PATH, "w", encoding="utf-8") as f:
        f.write(str(new_index))

    return quotes[new_index]


def build_payload(cache_key):
    url = f"{IMAGE_PUBLIC_URL}?v={cache_key}"
    return {
        "image": {
            "type": "external",
            "external": {"url": url},
        }
    }


def update_notion_block(payload):
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="PATCH",
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, resp.read()


def main():
    import datetime

    quotes = load_quotes()
    quote = pick_quote(quotes)

    generate(quote["frase"], quote["fonte"], IMAGE_OUTPUT_PATH)

    cache_key = datetime.date.today().isoformat()
    payload = build_payload(cache_key)

    try:
        status, body = update_notion_block(payload)
        print(f"OK [{status}] -> {quote['fonte']}")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"FALHA HTTP {e.code} -> {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"FALHA -> {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()