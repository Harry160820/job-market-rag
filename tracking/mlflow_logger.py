import mlflow

def log_ingestion_run(json_path: str, num_jobs: int, num_chunks: int):
    mlflow.set_experiment("job-market-rag-ingestion")
    with mlflow.start_run():
        mlflow.log_param("source_file", json_path)
        mlflow.log_metric("num_jobs", num_jobs)
        mlflow.log_metric("num_chunks", num_chunks)
        mlflow.log_artifact(json_path) # archive the raw data too

def log_query(question: str, latency_ms: float, num_sources: int):
    mlflow.set_experiment("job-market-rag-queries")
    with mlflow.start_run():
        mlflow.log_param("question", question[:200])
        mlflow.log_metric("latency_ms", latency_ms)
        mlflow.log_metric("num_sources", num_sources)