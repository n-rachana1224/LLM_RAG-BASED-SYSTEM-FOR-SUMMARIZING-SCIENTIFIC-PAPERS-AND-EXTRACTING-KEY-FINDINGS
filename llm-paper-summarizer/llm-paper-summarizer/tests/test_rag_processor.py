from utils.rag_processor import RAGProcessor

def test_rag_processor():
    rag = RAGProcessor()
    chunks = ["This is a test chunk about AI with 95% accuracy."]
    rag.embed_text(chunks)
    answer = rag.answer_question("What is the accuracy?", chunks[0])
    assert isinstance(answer, str) and len(answer) > 0