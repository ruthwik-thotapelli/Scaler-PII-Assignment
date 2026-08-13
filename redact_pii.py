def redact_text(text, analyzer):
    results = analyzer.analyze(text=text, language='en')
    results.sort(key=lambda x: x.start, reverse=True)
    for result in results:
        # desc order replacement
        pass
