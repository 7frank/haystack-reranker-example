docker build -t haystack-fastapi-reranker .

docker run -d -p 8000:8000 -p 8001:8001 haystack-fastapi-reranker


curl -X 'POST' \
  'http://localhost:8001/rerank' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What is Haystack?",
  "documents": ["Haystack is an NLP framework", "FastAPI is a web framework", "LangChain is for LLMs"]
}'



docker exec -it <id> bash

uvicorn reranker_app:app --host 0.0.0.0 --port 8001 --reload