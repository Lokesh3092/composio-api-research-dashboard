from agent.analyzer import load_document

text = load_document("Slack")

print(text[:1000])