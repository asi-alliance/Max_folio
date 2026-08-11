import os
import time
import json
from pathlib import Path
from openai import OpenAI
import chromadb

DESCRIPTION = "Store a memory in the PeTTa chroma_db long-term memory. The memory will be retrievable via chroma_query."

def run(text):
    """
    text: str - the text to remember/store in long-term memory
    returns: str - success or error message
    """
    gptrun = Path.home() / "PeTTa" / "gptrun.sh"
    if not gptrun.is_file():
        return "Error: ~/PeTTa/gptrun.sh not found"

    api_key = None
    for line in gptrun.read_text().splitlines():
        line = line.strip()
        if line.startswith("export OPENAI_API_KEY="):
            api_key = line.split("=", 1)[1].strip('"')
            break
    if not api_key:
        return "Error: OPENAI_API_KEY not found in gptrun.sh"

    client = OpenAI(api_key=api_key)
    embedding_response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    embedding = embedding_response.data[0].embedding

    db_path = str(Path.home() / "PeTTa" / "chroma_db")
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(
        name="memories",
        embedding_function=None
    )

    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    import uuid
    collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"time": ts}]
    )

    return f"REMEMBER-SUCCESS: stored at {ts}"
