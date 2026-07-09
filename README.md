# Frase do Dia — Automação Protocolo Forja

## O que mudou (v2 — card visual)

Em vez de texto puro, o robô agora **gera uma imagem** (estilo story: 1080x1920, gradiente preto/vermelho, frase centralizada) e publica no Notion como bloco de **imagem**.

## Setup (uma vez)

1. **Criar integração Notion**
   - notion.so/my-integrations → New integration → copiar o token (`NOTION_TOKEN`).

2. **Compartilhar a página com a integração**
   - Na página "PROTOCOLO forja" → `...` → Connections → adicionar a integração criada.

3. **No Notion: trocar o bloco de texto por um bloco de imagem vazio**
   - Delete o heading_4 antigo dentro do callout FRASE DO DIA.
   - No lugar, adicione um bloco de imagem qualquer (upload temporário de qualquer PNG só para criar o bloco).
   - Rode o mesmo processo de `curl` usado antes para descer nos `children` até achar esse bloco `type: "image"` e pegar o `id` → isso é o `IMAGE_BLOCK_ID`.

4. **Ativar GitHub Pages**
   - Repo → Settings → Pages → Source: **Deploy from branch** → Branch: `main` → Folder: `/docs` → Save.
   - URL pública final: `https://guilherm4andrade.github.io/frase-do-dia/frase.png`
   - Esse é o `IMAGE_PUBLIC_URL` (sem o `?v=...`, o script adiciona sozinho).

5. **Configurar Secrets no GitHub**
   - Repo → Settings → Secrets and variables → Actions:
     - `NOTION_TOKEN`
     - `IMAGE_BLOCK_ID`
     - `IMAGE_PUBLIC_URL`

6. **Ativar o workflow**
   - Actions → "Frase do Dia" → Run workflow (teste manual).

## Manutenção

- Adicionar novas frases: editar `quotes.json` (uma citação por fonte, curta, com atribuição).
- Ajustar visual do card: editar `generate_card.py` (cores, fontes, layout).
- `last_index.txt` evita repetição consecutiva — não editar manualmente.

