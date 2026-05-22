# pipeline/ingest.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup   # add this
import chromadb, json, pathlib

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", ". ", " "]
)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def clean_html(text: str) -> str:
    """Strip HTML tags from description."""
    return BeautifulSoup(text, "html.parser").get_text(separator=" ").strip()

def ingest(json_path: str):
    jobs = json.loads(pathlib.Path(json_path).read_text())
    print(f"Loaded {len(jobs)} jobs")

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(
        name="job_postings",
        metadata={"hnsw:space": "cosine"}
    )

    docs, metas, ids = [], [], []

    for i, job in enumerate(jobs):
        # Clean HTML from description
        description = clean_html(job.get("description", ""))
        
        # Skip jobs with no useful content
        if not description or len(description) < 50:
            print(f"Skipping job {i} — empty description: {job.get('title')}")
            continue

        full_text = f"{job['title']} at {job['company']}\n"
        full_text += f"Tags: {', '.join(job.get('tags', []))}\n"
        full_text += description

        chunks = splitter.split_text(full_text)

        for j, chunk in enumerate(chunks):
            docs.append(chunk)
            metas.append({
                "title": job["title"],
                "company": job["company"],
                "date": job["scraped_date"],
                "tags": str(job.get("tags", []))
            })
            ids.append(f"job_{i}_chunk_{j}")

    print(f"Created {len(docs)} chunks from {len(jobs)} jobs")

    # Guard against empty docs
    if not docs:
        print("ERROR: No documents to embed. Check your JSON file.")
        return

    embeddings = embedder.encode(
        docs, batch_size=64, show_progress_bar=True
    ).tolist()

    collection.add(documents=docs, metadatas=metas,
                   embeddings=embeddings, ids=ids)
    print(f"Done! Ingested {len(docs)} chunks into ChromaDB.")