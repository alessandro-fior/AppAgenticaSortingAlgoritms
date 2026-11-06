"""Prompt engine RAG per consigliare algoritmi di ordinamento."""
from openai import OpenAI
from qdrant_client import QdrantClient
from rich.console import Console
from rich.markdown import Markdown

import config
from embeddings import embed_query

SYSTEM_PROMPT = """Sei un assistente esperto di algoritmi di ordinamento. Rispondi in italiano usando le schede fornite. Consiglia l'algoritmo o la funzione corretta per il linguaggio e il caso d'uso; spiega complessita, stabilita e compromessi. Mostra un breve esempio usando il codice della scheda quando disponibile. Se il contesto non basta, dichiaralo senza inventare."""
console = Console()


def make_clients():
    client = OpenAI(
        api_key=config.require_api_key(),
        base_url=config.OPENROUTER_BASE_URL,
    )
    qdrant = QdrantClient(url=config.QDRANT_URL)
    if not qdrant.collection_exists(config.COLLECTION_NAME):
        raise RuntimeError(
            f"Collection '{config.COLLECTION_NAME}' assente. Avvia Qdrant e lancia prima: python ingest.py"
        )
    return client, qdrant


def retrieve(question: str, top_k: int = 5, *, openai_client=None, qdrant=None):
    if not question.strip():
        raise ValueError("Scrivi una domanda.")
    if openai_client is None or qdrant is None:
        openai_client, qdrant = make_clients()
    embedding = embed_query(question)
    return qdrant.query_points(
        collection_name=config.COLLECTION_NAME,
        query=embedding,
        limit=top_k,
        with_payload=True,
    ).points


def ask(question: str, top_k: int = 5, *, openai_client=None, qdrant=None, display=True) -> str:
    if openai_client is None or qdrant is None:
        openai_client, qdrant = make_clients()
    points = retrieve(question, top_k, openai_client=openai_client, qdrant=qdrant)
    if not points:
        return "Non ho trovato algoritmi pertinenti nel dataset."
    context = "\n\n".join(
        f"- {p.payload['name']} [{p.payload['language']}], {p.payload['algorithm']}; "
        f"medio {p.payload['time_avg']}, peggiore {p.payload['time_worst']}; "
        f"stabile {p.payload['stable']}. {p.payload['description']} "
        f"Quando: {p.payload['use_when']}\nCodice:\n{p.payload['code']}"
        for p in points
    )
    response = openai_client.chat.completions.create(
        model=config.CHAT_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Schede recuperate:\n{context}\n\nDomanda: {question}"},
        ],
    )
    answer = response.choices[0].message.content or "Non è arrivata una risposta testuale."
    if display:
        console.print(Markdown(answer))
    return answer


def main() -> None:
    client, qdrant = make_clients()
    console.print("[bold]Consulente di algoritmi di ordinamento[/bold] — scrivi 'esci' per terminare.")
    while True:
        try:
            question = console.input("\n[cyan]Domanda> [/cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nA presto!")
            break
        if question.lower() in {"esci", "exit", "quit"}:
            break
        if not question:
            continue
        try:
            ask(question, openai_client=client, qdrant=qdrant)
        except Exception as exc:
            console.print(f"[red]Errore: {exc}[/red]")


if __name__ == "__main__":
    main()
