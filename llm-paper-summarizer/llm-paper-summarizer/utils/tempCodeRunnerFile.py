from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import yaml
from utils.llm_processor import summarize  # Reuse BART for answers

def load_config():
    with open("config\\config.yaml", "r") as f:
        return yaml.safe_load(f)

class RAGProcessor:
    def __init__(self):
        config = load_config()
        self.embedder = SentenceTransformer(config["embedding_model"])
        self.index = None
        self.chunks = []

    def embed_text(self, chunks):
        """Embed text chunks and store in FAISS."""
        self.chunks = chunks
        embeddings = self.embedder.encode(chunks, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def answer_question(self, question, text):
        """Answer a question using RAG."""
        config = load_config()
        try:
            # Embed question
            question_embedding = self.embedder.encode([question], convert_to_numpy=True)
            # Search for top-3 relevant chunks
            _, indices = self.index.search(question_embedding, 3)
            context = " ".join([self.chunks[i] for i in indices[0]])
            # Generate answer
            prompt = config["qa_prompt"].format(question=question, context=context[:1000])
            answer = summarize(prompt)  # Reuse BART
            return answer
        except Exception as e:
            return f"Error answering: {e}"