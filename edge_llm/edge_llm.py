from .detect_langage_mistakes import DetectLangageMistakes
from ollama import chat, ChatResponse
import json
from ollama import chat
import json
from .prompts import PROMPT_FORMAT_ERROR,PROMPT_FRENCH_ASSISTANT
class EdgeLlmStream:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.detect_langage_mistakes = DetectLangageMistakes()

    def _answer_to_one_mistake(self, mistake: dict) -> str:
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
        response = ""
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            response += chunk['message']['content']
        print()  # To ensure proper formatting after streaming
        return response

    def _answer_to_mistakes(self, mistakes: list[dict]) -> str:
        response = ""
        for mistake in mistakes:
            response += self._answer_to_one_mistake(mistake) + "\n"
        return response

    def chat(self, messages: list[dict[str, str]]) -> str:
        messages.insert(0,{
            'role': 'system',
            'content': PROMPT_FRENCH_ASSISTANT
        })
        mistakes = self.detect_langage_mistakes.spot_mistake(messages[-1]["content"])
        answer = ""
        if mistakes:
            answer = self._answer_to_mistakes(mistakes)
        # Stream the main chat response as well
        stream = chat(
            model=self.model_name,
            messages=messages,
            stream=True
        )
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            answer += chunk['message']['content']
        print()  # To ensure proper formatting after streaming
        return answer

        
