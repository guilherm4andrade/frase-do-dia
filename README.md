# Frase do Dia — Automação Protocolo Forja

## Setup (uma vez)

1. **Criar integração Notion**
   - notion.so/my-integrations → New integration → copiar o token (`NOTION_TOKEN`).

2. **Compartilhar a página com a integração**
   - Na página "PROTOCOLO forja" → `...` → Connections → adicionar a integração criada.

3. **Obter o BLOCK_ID do heading dentro do callout "FRASE DO DIA"**
   - GET `https://api.notion.com/v1/blocks/{page_id}/children`
   - Header: `Authorization: Bearer NOTION_TOKEN`, `Notion-Version: 2022-06-28`
   - Localizar o bloco `callout` da seção FRASE DO DIA, pegar o `id` do bloco filho `heading_4` (dentro de `callout.children`, se não vier expandido, chamar `/blocks/{callout_id}/children`).
   - Esse ID vai em `BLOCK_ID`.

4. **Subir este repositório no GitHub**
   - Criar repo privado, dar push nesta pasta.

5. **Configurar Secrets no GitHub**
   - Repo → Settings → Secrets and variables → Actions:
     - `NOTION_TOKEN`
     - `BLOCK_ID`

6. **Ativar o workflow**
   - Actions já roda sozinho às 00:00 (Brasília). Testar manualmente via "Run workflow" (workflow_dispatch).

## Manutenção

- Adicionar novas frases: editar `quotes.json` (uma citação por fonte, curta, com atribuição).
- `last_index.txt` evita repetição consecutiva — não editar manualmente.
