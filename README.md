# Gestió d'inventari amb IA

Backend per a la gestió d'inventari d'un negoci de revenda de accessoris mitjançant instruccions en llenguatge natural. L'agent permet consultar, afegir i controlar l'estoc de manera ràpida i automatitzada, incloent fluxos de revisió humana per a les operacions. Les dades s'emmagatzemen a MongoDB.

## Tecnologies

- **FastAPI** per a l'API.
- **LangChain (amb LangGraph)** i **OpenAI** per gestionar les converses i les accions de l'agent.
- **MongoDB** per desar l'inventari.
- **Pydantic** per validar les peticions i estructurar les respostes.

## Setup del projecte

Cal tenir Python 3.12 o superior, [uv](https://docs.astral.sh/uv/) i una base de dades MongoDB.

Les dependències del projecte estan definides a `pyproject.toml`. Des de l'arrel del repositori, instal·la-les amb:

```bash
uv sync
```

`uv sync` utilitza la configuració de `pyproject.toml` i el fitxer `uv.lock`.

Crea un fitxer `.env` a l'arrel del projecte i configura les credencials necessàries:

```env
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_mongodb_connection_string
```

Engega el servidor de desenvolupament:

```bash
uv run uvicorn --app-dir src inventory_ai_agent.app.main:app --reload
```

L'API estarà disponible a `http://127.0.0.1:8000`. La documentació interactiva de FastAPI és a `http://127.0.0.1:8000/docs`.

## Rutes principals

- `GET /` comprova que el servidor està en funcionament.
- `POST /agent/chat` envia un missatge a l'agent. (Obten, crea, o actualitza)
- Per eliminar o vendre un article, demana-ho primer a `POST /agent/chat`. Quan l'agent indiqui que l'acció està pendent d'aprovació, envia una petició a `POST /agent/approve` amb el mateix `thread_id`; aquest endpoint reprèn l'acció.

## Proves ràpides amb Postman

Per provar el xat, selecciona el mètode `POST`, utilitza l'adreça `http://127.0.0.1:8000/agent/chat` i tria `Body` → `raw` → `JSON`.

Consulta els articles:

```json
{
  "thread_id": "postman-test",
  "message": "Show me all items in the inventory"
}
```

Afegeix un article:

```json
{
  "thread_id": "postman-test",
  "message": "Add a black Nike hoodie, size M, in good condition, for 35 euros"
}
```

Per eliminar un article, primer demana-ho al xat. Si l'agent deixa l'acció pendent d'aprovació, envia la segona petició amb el mateix `thread_id`:

**1. Demana l'eliminació** — `POST http://127.0.0.1:8000/agent/chat`

```json
{
  "thread_id": "delete-test",
  "message": "Remove the black Nike hoodie from the inventory"
}
```

**2. Aprova i reprèn l'acció** — `POST http://127.0.0.1:8000/agent/approve`

```json
{
  "thread_id": "delete-test",
  "decision": "approve"
}
```
