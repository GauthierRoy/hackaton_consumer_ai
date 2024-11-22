from edge_llm.edge_llm import EdgeLlmStream
edge_llm = EdgeLlmStream("qwen2.5:3b")

anwser = edge_llm.chat([
    {
        "role":"user",
        "content":"J'aimes la soleil et toi ?"
    }
]
)