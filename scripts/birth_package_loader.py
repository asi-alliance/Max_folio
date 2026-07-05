#!/usr/bin/env python3
"""Birth Package Loader — batch-injects curated memories into OmegaClaw ChromaDB."""
import os, re, uuid, sys
from datetime import datetime, timezone
from openai import OpenAI
import chromadb

BP_FILE = os.environ.get("BP_FILE", "/tmp/birth_package.txt")
CHROMA_PATH = os.environ.get("CHROMA_PATH", "./chroma_db")
MODEL = "text-embedding-3-large"

def parse_entries(path):
    with open(path) as f:
        text = f.read()
    return [m.group(0).strip() for m in re.finditer(r"BP-\d{3}:.*?(?=\nBP-\d{3}:|\n---|$)", text, re.DOTALL)]

def embed(texts, client):
    resp = client.embeddings.create(input=texts, model=MODEL)
    return [d.embedding for d in resp.data]

def load(entries, embeddings, collection):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    ids = [str(uuid.uuid4()) for _ in entries]
    metas = [{"time": ts} for _ in entries]
    collection.add(ids=ids, documents=entries, embeddings=embeddings, metadatas=metas)
    return len(ids)

if __name__ == "__main__":
    entries = parse_entries(BP_FILE)
    print(f"Parsed {len(entries)} entries from {BP_FILE}")
    oai = OpenAI()
    BATCH = 20
    all_embs = []
    for i in range(0, len(entries), BATCH):
        all_embs.extend(embed(entries[i:i+BATCH], oai))
    print(f"Embedded {len(all_embs)} entries")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    col = client.get_or_create_collection(name="memories", embedding_function=None)
    n = load(entries, all_embs, col)
    print(f"Loaded {n} birth package memories into {CHROMA_PATH}")