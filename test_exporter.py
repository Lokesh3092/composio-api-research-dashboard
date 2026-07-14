from agent.exporter import export_batch

batch = export_batch()

print(batch[0]["file"])

print(batch[0]["content"][:500])