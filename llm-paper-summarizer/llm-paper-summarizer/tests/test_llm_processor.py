from utils.llm_processor import summarize, extract_findings

def test_llm_processor():
    sample_text = "This is a test paper about AI. It proposes a new model with 95% accuracy."
    summary = summarize(sample_text)
    findings = extract_findings(sample_text)
    assert isinstance(summary, str) and len(summary) > 0
    assert isinstance(findings, str) and len(findings) > 0