# PII Redaction Evaluation Strategy and Metrics

## Evaluation Strategy
To evaluate the PII redaction script, a mock ground-truth dataset was created representing typical ticket logs containing PII (names, emails, phone numbers, addresses, IP addresses, dates, and organizations).

The `evaluate_redaction.py` script runs the Presidio Analyzer on the sample text and compares the detected entities against the predefined ground-truth list.

### Definitions:
- **True Positives (TP)**: PII entities correctly identified by the analyzer.
- **False Positives (FP)**: Text incorrectly identified as PII by the analyzer (e.g., fragments of URLs identified as emails or names).
- **False Negatives (FN)**: Actual PII entities that the analyzer missed.

## Evaluation Results

Based on the evaluation run on the sample dataset:

- **True Positives (TP)**: 4
- **False Positives (FP)**: 9
- **False Negatives (FN)**: 3
- **Precision**: 0.31 (31%)
- **Recall**: 0.57 (57%)

*Note on Metrics*: The precision and recall numbers are indicative of the baseline `en_core_web_lg` model performance on this specific formatted text. The false positives mainly resulted from Presidio identifying overlapping entities (e.g., identifying a 10-digit number as both a Phone Number, US Bank Number, and UK NHS number simultaneously) and partial matches on email URLs. 

### Improving the Metrics
In a production setting, the precision and recall can be significantly improved by:
1. **Adding Custom Recognizers**: Defining specific regex patterns for known formats (like Indian phone numbers +91) to reduce False Negatives.
2. **Context Enhancements**: Adding context words (e.g., "Phone:", "Email:") to Presidio to boost the confidence of specific entities.
3. **Threshold Tuning**: Adjusting the acceptance threshold of the analyzer to drop low-confidence predictions, thereby reducing False Positives.
