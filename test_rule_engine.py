from agent.analyzer import load_document
from agent.rule_engine import *

text = load_document("Slack")

print("Auth:", extract_auth_methods(text))
print("API:", extract_api_surface(text))
print("Self Serve:", extract_self_serve(text))
print("Buildable:", extract_buildability(text))
print("MCP:", extract_mcp(text))