# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from api.rag_chain import build_chain
import time

app = FastAPI(title="Job Market Intelligence API")
chain = build_chain()

class Query(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    sources: list[dict]
    latency_ms: float

@app.post("/query", response_model=Answer)
async def query(q: Query):
    t0 = time.time()
    result = chain.invoke({"query": q.question})  # changed from chain.run()
    latency = (time.time() - t0) * 1000

    sources = [
        {"company": doc.metadata["company"], "title": doc.metadata["title"]}
        for doc in result["source_documents"]
    ]
    return Answer(
        answer=result["result"],
        sources=sources,
        latency_ms=round(latency)
    )

@app.get("/health")
def health():
    return {"status": "ok"}