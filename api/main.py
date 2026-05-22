from fastapi import FastAPI
from pydantic import BaseModel
from api.rag_chain import build_chain
import time

app = FastAPI(title = "Job Market Intelligence API")
chain = build_chain() #load once at startup

class Query(BaseModel):
    question: str
class Answer(BaseModel):
    Answer: str
    sources: list[dict]
    latency_ms: float


@app.post("/query", response_model=Answer)
async def query(q: Query):
    t0 = time.time()
    result = chain.run(q.question)
    latency = (time.time() - t0) * 1000


    sources = [
        {"company": doc.metadata["company"], "title": doc.metadata["title"]}
        for doc in result["source_documents"]
    ]
    return Answer(Answer=result["answer"], sources=sources, latency_ms=round(latency, 2))

app.get("/health")
def health():
    return {"status": "ok"}