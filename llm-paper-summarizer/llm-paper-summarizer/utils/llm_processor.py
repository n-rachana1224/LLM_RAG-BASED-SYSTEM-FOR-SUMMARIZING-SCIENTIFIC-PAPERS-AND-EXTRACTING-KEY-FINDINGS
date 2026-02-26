from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import yaml
import torch

def load_config():
    with open("config\\config.yaml", "r") as f:
        return yaml.safe_load(f)

def summarize(text):
    """Generate a summary using BART-large-cnn."""
    config = load_config()
    try:
        # Try quantized model with Accelerate
        try:
            model = AutoModelForSeq2SeqLM.from_pretrained(config["llm_model"], device_map="auto", load_in_8bit=True)
            tokenizer = AutoTokenizer.from_pretrained(config["llm_model"])
            summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
        except:
            # Fallback to CPU without quantization
            summarizer = pipeline("summarization", model=config["llm_model"], device=-1)
        prompt = config["summarization_prompt"].format(text=text[:1000])  # Limit input
        summary = summarizer(prompt, max_length=300, min_length=100, do_sample=False)[0]["summary_text"]
        return summary
    except Exception as e:
        return f"Error summarizing: {e}"

def extract_findings(text):
    """Extract key findings as a bulleted list."""
    config = load_config()
    try:
        # Try quantized model with Accelerate
        try:
            model = AutoModelForSeq2SeqLM.from_pretrained(config["llm_model"], device_map="auto", load_in_8bit=True)
            tokenizer = AutoTokenizer.from_pretrained(config["llm_model"])
            summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
        except:
            # Fallback to CPU without quantization
            summarizer = pipeline("summarization", model=config["llm_model"], device=-1)
        prompt = config["extraction_prompt"].format(text=text[:1000])
        findings = summarizer(prompt, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]
        return findings
    except Exception as e:
        return f"Error extracting findings: {e}"