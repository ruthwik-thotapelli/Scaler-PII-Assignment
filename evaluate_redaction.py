from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

def evaluate(text, ground_truth):
    """
    Evaluates the PII redaction by comparing Presidio's output with ground truth.
    ground_truth is a list of dicts: [{'text': 'Rashi Patil', 'type': 'PERSON'}, ...]
    """
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
    }
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
    results = analyzer.analyze(text=text, entities=[], language='en')
    
    predicted_entities = []
    for result in results:
        predicted_entities.append({
            'text': text[result.start:result.end],
            'type': result.entity_type
        })
        
    # Calculate True Positives, False Positives, False Negatives
    tp = 0
    fp = 0
    fn = 0
    
    # We match by exact text for simplicity
    predicted_texts = [e['text'] for e in predicted_entities]
    gt_texts = [e['text'] for e in ground_truth]
    
    for gt in gt_texts:
        if gt in predicted_texts:
            tp += 1
        else:
            fn += 1
            
    for pred in predicted_texts:
        if pred not in gt_texts:
            # Check if it's a known non-PII or an actual FP
            fp += 1
            
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    print("--- Evaluation Report ---")
    print(f"True Positives (TP): {tp}")
    print(f"False Positives (FP): {fp}")
    print(f"False Negatives (FN): {fn}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print("\nPredicted Entities:")
    for p in predicted_entities:
        print(f"  - {p['text']} ({p['type']})")

if __name__ == "__main__":
    sample_text = """
    Reported by: Rashi Patil (rashhi.patil@gmail.com)
    Phone: +91 9876543210
    DOB: 12/05/1990
    Company: Acme Corp
    Address: 123 Main St, Springfield, IL 62701
    Issue: The server at 192.168.1.1 is not responding. Please check.
    """
    
    ground_truth = [
        {'text': 'Rashi Patil', 'type': 'PERSON'},
        {'text': 'rashhi.patil@gmail.com', 'type': 'EMAIL_ADDRESS'},
        {'text': '+91 9876543210', 'type': 'PHONE_NUMBER'},
        {'text': '12/05/1990', 'type': 'DATE_TIME'},
        {'text': 'Acme Corp', 'type': 'ORGANIZATION'},
        {'text': '123 Main St, Springfield, IL 62701', 'type': 'LOCATION'},
        {'text': '192.168.1.1', 'type': 'IP_ADDRESS'}
    ]
    
    evaluate(sample_text, ground_truth)
