from edge_llm.edge_llm import EdgeLlmStream
edge_llm = EdgeLlmStream("qwen2.5:7b")

stream = edge_llm.chat([
    {
        "role":"user",
        "content":"J'aimes la pluie et toi ?"
    }
]
)
for chunk in stream:
    print(chunk, end="")