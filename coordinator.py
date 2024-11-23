from big_llm import Big_LLM
from edge_llm.edge_llm import EdgeLlmStream

class Coordinator:

    def __init__(self):
        self.big_llm = Big_LLM()
        self.edge_llm = EdgeLlmStream("qwen2.5:7b")

    def run(self):
        # Pause and wait for user input
        user_input = input("Please enter some text: ")
        
        
        
        

if __name__ == "__main__":
    coord = Coordinator()
    coord.run()  