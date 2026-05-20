from langchain_community.vectorstores import chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a job market analyst. Based ONLY on the job postings below,
answer the question concisely with specific skill names and counts where possible.

Job posting excerpts:
{context}

Question: {question}

Answer:"""
)

def build_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name = 'all-MiniLM-L6-v2'
    )
    vectordb = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_name="job_postings"
    )

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8, "fetch_k": 20}
    )

    llm = Ollama(model="llama3.2", temperature=0.0)   # runs on your machine
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )