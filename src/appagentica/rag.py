"""Motore RAG (Retrieval-Augmented Generation) per la raccomandazione di algoritmi."""
from typing import Any
from openai import OpenAI
from qdrant_client import QdrantClient
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from appagentica import config
from appagentica.embeddings import embed_query

SYSTEM_PROMPT = """Sei un consulente software senior specializzato in strutture dati e algoritmi di ordinamento.
Rispondi in lingua italiana usando in modo rigoroso le schede fornite nel contesto.
Linee guida:
1. Consiglia con precisione la funzione o algoritmo ottimale per il linguaggio e il caso d'uso descritto.
2. Dettaglia la complessità temporale (caso medio, caso peggiore) e spaziale, specificando stabilità e in-place.
3. Spiega i compromessi (trade-off) e perché questa scelta è preferibile ad alternative.
4. Fornisci un esempio di codice chiaro e pronto all'uso basato sulle schede.
5. Se il contesto fornito non contiene informazioni sufficienti, indicalo esplicitamente senza inventare dettagli non presenti."""

console = Console()


def make_clients() -> tuple[OpenAI, QdrantClient]:
    """Inizializza e verifica i client OpenAI (OpenRouter) e Qdrant."""
    client = OpenAI(
        api_key=config.require_api_key(),
        base_url=config.OPENROUTER_BASE_URL,
    )
    qdrant = QdrantClient(url=config.QDRANT_URL)
    if not qdrant.collection_exists(config.COLLECTION_NAME):
        raise RuntimeError(
            f"Collection '{config.COLLECTION_NAME}' non trovata su {config.QDRANT_URL}. "
            f"Assicurati che Qdrant sia avviato (docker compose up -d) e lancia: python ingest.py"
        )
    return client, qdrant


def retrieve(
    question: str,
    top_k: int = 5,
    *,
    qdrant: QdrantClient | None = None,
) -> list[Any]:
    """Cerca vettorialmente le schede di algoritmi più pertinenti per la domanda."""
    if not question or not question.strip():
        raise ValueError("La domanda non può essere vuota.")

    if qdrant is None:
        qdrant = QdrantClient(url=config.QDRANT_URL)
        if not qdrant.collection_exists(config.COLLECTION_NAME):
            raise RuntimeError(
                f"Collection '{config.COLLECTION_NAME}' non trovata su {config.QDRANT_URL}."
            )

    embedding = embed_query(question.strip())
    response = qdrant.query_points(
        collection_name=config.COLLECTION_NAME,
        query=embedding,
        limit=top_k,
        with_payload=True,
    )
    return response.points


def format_context(points: list[Any]) -> str:
    """Formatta i punti recuperati da Qdrant come testo contestuale per l'LLM."""
    if not points:
        return ""
    entries = []
    for p in points:
        payload = p.payload or {}
        entries.append(
            f"### {payload.get('name', 'Algoritmo')} [{payload.get('language', 'Generale')}]\n"
            f"- Famiglia: {payload.get('algorithm', 'N/D')}\n"
            f"- Complessità tempo: medio {payload.get('time_avg', 'N/D')}, peggiore {payload.get('time_worst', 'N/D')}\n"
            f"- Memoria / Stabilità: spazio {payload.get('space', 'N/D')}, stabile: {payload.get('stable')}, in-place: {payload.get('in_place')}\n"
            f"- Descrizione: {payload.get('description', '')}\n"
            f"- Quando usarlo: {payload.get('use_when', '')}\n"
            f"- Esempio di codice:\n```{payload.get('language', '').lower()}\n{payload.get('code', '')}\n```"
        )
    return "\n\n".join(entries)


def ask(
    question: str,
    top_k: int = 5,
    *,
    openai_client: OpenAI | None = None,
    qdrant: QdrantClient | None = None,
    display: bool = True,
) -> str:
    """Esegue la pipeline RAG completa: ricerca semantica, costruzione del prompt e generazione."""
    if openai_client is None or qdrant is None:
        created_client, created_qdrant = make_clients()
        openai_client = openai_client or created_client
        qdrant = qdrant or created_qdrant

    points = retrieve(question, top_k=top_k, qdrant=qdrant)
    if not points:
        msg = "Non sono stati trovati algoritmi pertinenti nel catalogo per la richiesta."
        if display:
            console.print(f"[yellow]{msg}[/yellow]")
        return msg

    context = format_context(points)
    user_prompt = f"Contesto informativo dalle schede tecniche:\n\n{context}\n\nDomanda utente: {question}"

    response = openai_client.chat.completions.create(
        model=config.CHAT_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    answer = response.choices[0].message.content or "Nessuna risposta testuale generata dal modello."

    if display:
        console.print("\n", Markdown(answer), "\n")
    return answer


def main() -> None:
    """Interfaccia interattiva a riga di comando (CLI)."""
    try:
        client, qdrant = make_clients()
    except Exception as exc:
        console.print(Panel(f"[bold red]Inizializzazione fallita:[/bold red]\n{exc}", title="Errore"))
        return

    welcome_text = (
        "[bold cyan]Benvenuto in AppAgentica![/bold cyan]\n"
        "Consulente RAG intelligente per algoritmi di ordinamento.\n"
        "Supporta Python, Java, C++, JavaScript, C#, Go, Rust e implementazioni classiche.\n\n"
        "[dim]Digita 'esci', 'exit' o premi Ctrl+C per terminare.[/dim]"
    )
    console.print(Panel(welcome_text, title="🤖 AppAgentica", expand=False))

    while True:
        try:
            query = console.input("\n[bold cyan]Cosa vuoi ordinare? > [/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Arrivederci![/dim]")
            break

        if query.lower() in {"esci", "exit", "quit"}:
            console.print("[dim]Sessione terminata. Arrivederci![/dim]")
            break

        if not query:
            continue

        try:
            with console.status("[bold green]Ricerca semantica e consultazione LLM in corso...[/bold green]"):
                ask(query, top_k=5, openai_client=client, qdrant=qdrant, display=True)
        except Exception as exc:
            console.print(f"[bold red]Errore:[/bold red] {exc}")


if __name__ == "__main__":
    main()
