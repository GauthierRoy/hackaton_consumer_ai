from .detect_langage_mistakes import DetectLangageMistakes
from ollama import chat, ChatResponse
import json
from .prompts import PROMPT_FORMAT_ERROR, PROMPT_FRENCH_ASSISTANT,DOES_IT_ANSWER_THE_QUESTION
from .history_storage import HistoryStorage

class EdgeLlmStream:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.detect_langage_mistakes = DetectLangageMistakes()
        self.history_storage = HistoryStorage()

    def _answer_to_one_mistake(self, mistake: dict):
        # Stream the response incrementally
        stream = chat(
            model='qwen2.5:0.5b',
            messages=[
                {
                    'role': 'system',
                    'content': PROMPT_FORMAT_ERROR
                },
                {
                    'role': 'user',
                    'content': json.dumps(mistake)
                }
            ],
            stream=True
        )
        for chunk in stream:
            yield chunk

    def _answer_to_mistakes(self, mistakes: list[dict]):
        for mistake in mistakes:
            yield from self._answer_to_one_mistake(mistake)

    def _process_and_store_conversion(self, source):
        answer = ""
        # Iterate over the source (either stream or mistakes)
        for chunk in source:
            yield chunk['message']['content']  
            answer += chunk['message']['content'] 

        yield "\n" 
        
        self.history_storage.store_conversion({
            'role': 'assistant',
            'content': answer
        })

    def anwser(self, messages: list[dict[str, str]]):
        messages.insert(0, {
            'role': 'system',
            'content': PROMPT_FRENCH_ASSISTANT
        })
        self.history_storage.store_conversion(messages[0])
        self.history_storage.store_conversion(messages[1])

        mistakes = self.detect_langage_mistakes.spot_mistake(messages[-1]["content"])

        if mistakes:
            yield from self._process_and_store_conversion(self._answer_to_mistakes(mistakes))

        # Stream the main chat response as well
        stream = chat(
            model=self.model_name,
            messages=messages,
            stream=True
        )

        yield from self._process_and_store_conversion(stream)


    def ask_a_question_verify_with_detect_mistakes(self, question: str, answer_expected: dict) -> None:
        # answer_expected not used

        # Ask the question
        yield f"\nQuestion: {question}\n"
        yield "Your answer: "

        # Wait for user input
        user_answer = input()

        # store the user answer
        self.history_storage.store_conversion({
            'role': 'user',
            'content': user_answer
        })

        mistakes = self.detect_langage_mistakes.spot_mistake(user_answer)
        if not mistakes:
            mistakes = "No Mistakes Found"

        # Verify the answer against expected elements
        verify_messages = [
            {
                'role': 'system',
                'content': "You are a helpful assistant that verifies answers. Provide constructive feedback based on the expected elements. Only provide the direct feedback, it will be given directly to the user."
            },
            {
                'role': 'user',
                # Guideline: {answer_expected['grading_guidelines']}

                'content': f"""
Please verify this answer against the expected elements and provide feedback:

Student answer: {user_answer}
Mistakes found: {mistakes}

# FEEDBACK HERE PROVIDED DIRECTLY TO THE USER
                """
            }
        ]

        # Get the feedback using the chat method
        stream = chat(
            model=self.model_name,
            messages=verify_messages,
            stream=True
        )

        yield "\nFeedback:\n"
        # Process and yield the feedback
        yield from self._process_and_store_conversion(stream)

    def _does_it_answer_the_question(self, user_answer: str, example_anwser:str,question: str) -> bool:
        """
        check if the user answer the question
        """
        content = f"QUESTION: {question}\nANSWER: {user_answer}\n"
        if example_anwser:
            content += f"EXPECTED ANSWER: {example_anwser}\n"
        content += "OUTPUT (YES/NO):"
        messages = [
            {
                "role": "system",
                "content": DOES_IT_ANSWER_THE_QUESTION
            },
            {
                "role": "user",
                "content": content
            }
        ]

        stream = chat(
            model=self.model_name,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            if chunk['message']['content'].upper() == "YES":
                return True
            elif chunk['message']['content'].upper() == "NO":
                return False
        
        


    def ask_a_question_and_verify(self, question: str, answer_expected: dict) -> None:
        """
        Ask a question, wait for user input, and verify the answer against expected elements.
        
        Args:
            question (str): The question to ask
            elements_of_answer (list[str]): List of expected elements in the answer
        """
        # Ask the question
        yield f"\nQuestion: {question}\n"
        yield "Your answer: "
        
        # Wait for user input
        user_answer = input()

        # store the user answer
        self.history_storage.store_conversion({
            'role': 'user',
            'content': user_answer
        })

        mistakes = self.detect_langage_mistakes.spot_mistake(user_answer)
        if not mistakes:
            if self._does_it_answer_the_question(user_answer=user_answer, example_anwser=answer_expected.get('model_answer',""),question=question):
                response = "Good job, you answered the question"
            else:
                response = "You did not answer the question"
            self.history_storage.store_conversion({
                'role': 'assistant',
                'content': response
            })
            yield response
        else:
            yield from self._process_and_store_conversion(self._answer_to_mistakes(mistakes))
#         content_user = f"""
# Please verify this answer against the expected elements and provide feedback, only provide the direct feedback, it will be given directly to the user.

# Student answer: {user_answer}
# Possible anwser: {answer_expected['model_answer']}
# """
#         mistakes = self.detect_langage_mistakes.spot_mistake(user_answer)
#         if mistakes:
#             content_user += f"Mistakes found: {mistakes}"
#         content_user += """
# # FEEDBACK HERE PROVIDED DIRECTLY TO THE USER :
#                 """

        
        # Verify the answer against expected elements
        # verify_messages = [
        #     {
        #         'role': 'system',
        #         'content': "You are a helpful assistant that verifies answers. Provide constructive feedback based on the expected elements. Only provide the direct feedback, it will be given directly to the user."
        #     },
        #     {
        #         'role': 'user',
        #         # Guideline: {answer_expected['grading_guidelines']}
        #         'content': content_user
        #     }
        # ]
        
        # # Get the feedback using the chat method
        # stream = chat(
        #     model=self.model_name,
        #     messages=verify_messages,
        #     stream=True
        # )
        
        # yield "\nFeedback:\n"
        # # Process and yield the feedback
        # yield from self._process_and_store_conversion(stream)

    def teach_a_lesson(self, lesson: dict) -> None:
        """
        Teach a complete lesson by processing the system prompt and all exercises.
        Interacts with the user for each question.
        
        Args:
            lesson (dict): A dictionary containing the lesson structure with system_prompt and exercises
        """
        # First, process the system prompt
        system_message = {
            'role': 'system',
            'content': lesson['system_prompt']
        }
        self.history_storage.store_conversion(system_message)
        
        # Initialize the lesson
        yield "Starting the lesson...\n"
        yield f"System Prompt: {lesson['system_prompt']}\n\n"
        
        # Process each exercise
        for i, exercise in enumerate(lesson['exercices'], 1):
            yield f"\nExercise {i}:\n"
            
            # Use ask_a_question method for each exercise
            yield from self.ask_a_question_and_verify(
                question=exercise['question'],
                answer_expected=exercise['answer_expected']
            )
            # yield from self.ask_a_question_verify_with_detect_mistakes(
            #     question=exercise['question'],
            #     answer_expected=exercise['answer_expected']
            # )
            
            yield "\n---\n"  # Separator between exercises
        
        # Conclude the lesson
        yield "\nLesson completed!"

    def clean_history_and_mistakes(self):
        self.history_storage = HistoryStorage()

    def get_mistakes(self):
        return self.history_storage.get_mistakes()
    
    def get_conversions(self):
        return self.history_storage.get_conversions()



