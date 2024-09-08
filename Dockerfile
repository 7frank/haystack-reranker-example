FROM deepset/haystack:gpu-v1.26.3

WORKDIR /app

# RUN pip install fastapi uvicorn sentence-transformers hayhooks
RUN pip install fastapi uvicorn 
COPY reranker_app.py /app/reranker_app.py

# Expose ports for Haystack API and FastAPI

EXPOSE 8000 8001

# CMD ["tail", "-f", "/dev/null"]

CMD ["uvicorn", "reranker_app:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]