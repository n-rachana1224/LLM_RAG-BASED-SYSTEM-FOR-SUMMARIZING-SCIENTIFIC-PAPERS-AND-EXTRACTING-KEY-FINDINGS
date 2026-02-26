import fitz  # PyMuPDF
import yaml

def load_config():
    with open("config\\config.yaml", "r") as f:
        return yaml.safe_load(f)

def extract_text(pdf_path):
    """Extract and chunk text from a PDF."""
    config = load_config()
    chunk_size = config["chunk_size"]
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        
        # Chunk text for LLM
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        return text, chunks
    except Exception as e:
        return None, f"Error: {e}"