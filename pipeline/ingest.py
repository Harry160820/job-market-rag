from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import json, pathlib, chromadb

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=64,
    separators=["\n\n", "\n", " ", "", ". "]
)

embedder = SentenceTransformer("all-MiniLM-L6-v2")  # fast, 384-dim, runs locally

def ingest(jason_path: str):
    jobs = json.loads(pathlib.Path(jason_path).read_text())
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collections(
        name="job_postings",
        metadata={"hnsw:space": "cosine"} #cosine distance for semantic similarity
    )

    docs, metas, ids, embeddings = [], [], [], []


    for i, job in enumerate(jobs):
        full_text = f"{job['title']} at {job['company']}\n"
        full_text += f"Tags: {', '.join(job['tags'])}\n"
        full_text += job['description']

        chunks = splitter.create_documents([full_text])

        for j, chunk in enumerate(chunks):
            docs.append(chunk)
            metas.append(
                {
                    "title": job['title'],
                    "company": job['company'],
                    "date": job['scraped_date'],
                    "tags": job['tags']
                }
            )

            ids.append(f"job_{i}_chunk_{j}")

embeddings = embedder.encode(docs, batch_size=64, show_progress_bar=True).tolist()
collection.add(documents=docs, metadatas=metas, ids=ids, embeddings=embeddings)
print(f"Ingested {len(docs)} chunks from {len(jobs)} job postings.")