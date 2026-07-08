import json
import os
import random
import sys
import urllib.request

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
BLOCK_ID = os.environ["BLOCK_ID"]  # ID do bloco heading_4 DENTRO do callout (não o callout em si)
QUOTES_PATH = os.path.join(os.path.dirname(__file__), "quotes.json")
STATE_PATH = os.path.join(os.path.dirname(__file__), "last_index.txt")

NOTION_VERSION = "2022-06-28"
API_URL = f"https://api.notion.com/v1/blocks/{BLOCK_ID}"


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


def build_payload(quote):
    text = f'{quote["fonte"]} - "{quote["frase"]}"'
    return {
        "heading_4": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": text},
                }
            ]
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
    quotes = load_quotes()
    quote = pick_quote(quotes)
    payload = build_payload(quote)
    try:
        status, body = update_notion_block(payload)
        print(f"OK [{status}] -> {quote['fonte']}")
    except Exception as e:
        print(f"FALHA -> {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
