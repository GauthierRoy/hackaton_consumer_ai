from big_llm import Big_LLM
from edge_llm.edge_llm import EdgeLlmStream

class Coordinator:

    def __init__(self):

        self.small_llm = EdgeLlmStream("qwen2.5:7b")
        self.big_llm = Big_LLM()

    def run(self):
        # Pause and wait for user input
        user_input = input("Please enter some text: ")
        
        ##################################################
        # Part where you run the little lm 

        # Expected output: history of the conversation (str), mistakes (str)
        conversation = ""
        mistakes = ""
        ##################################################

        min_topics, max_topics, exercises = self.big_llm.run(conversation, mistakes)

        # Expected output: min_topics (str), max_topics (str), exercises (str)
        # min_topics: for the given level (A1, A2, B1, B2), the topics (grammaire, orthographe...) that the student should focus on
        # max_topics: for the given level (A1, A2, B1, B2), the topics (grammaire, orthographe...) that the student has mastered
        # exercises: context prompts to give to the baby lm

        # Given the current 

if __name__ == "__main__":
    coord = Coordinator()
    coord.run()  