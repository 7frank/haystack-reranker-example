from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch

# Initialize FastAPI app
app = FastAPI()

# Load the SentenceTransformer model for reranking
reranker_model = SentenceTransformer('cross-encoder/ms-marco-MiniLM-L-6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')

# Define input structure
class RerankRequest(BaseModel):
    query: str
    documents: list[str]

# Reranking endpoint
@app.post("/rerank")
async def rerank(request: RerankRequest):
    query = request.query
    documents = request.documents

    if not query or not documents:
        raise HTTPException(status_code=400, detail="Invalid input data.")

    # Rerank documents using cosine similarity
    query_embedding = reranker_model.encode(query, convert_to_tensor=True)
    document_embeddings = reranker_model.encode(documents, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)

    # Combine documents with their rerank scores
    reranked_documents = [
        {"document": doc, "score": score.item()} for doc, score in zip(documents, cosine_scores[0])
    ]

    # Sort documents by the rerank score
    reranked_documents = sorted(reranked_documents, key=lambda x: x["score"], reverse=True)

    return {"reranked_documents": reranked_documents}
