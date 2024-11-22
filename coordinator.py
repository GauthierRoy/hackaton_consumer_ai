from big_llm import Big_LLM


class Coordinator:

    def __init__(self):
        self.big_llm = Big_LLM()

    def run(self):
        # Pause and wait for user input
        user_input = input("Please enter some text: ")
        
        
        

if __name__ == "__main__":
    coord = Coordinator()
    coord.run()  