from .detect_langage_mistakes import DetectLangageMistakes
from ollama import chat, ChatResponse
import json
from .prompts import PROMPT_FORMAT_ERROR, PROMPT_FRENCH_ASSISTANT
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

    def chat(self, messages: list[dict[str, str]]):
        messages.insert(0, {
            'role': 'system',
            'content': PROMPT_FRENCH_ASSISTANT
        })
        self.history_storage.store_conversion(messages[0])
        self.history_storage.store_conversion(messages[1])

        mistakes = self.detect_langage_mistakes.spot_mistake(messages[-1]["content"])

        if mistakes:
            answer = ""
            for response_chunk in self._answer_to_mistakes(mistakes):
                yield response_chunk['message']['content']
                answer += response_chunk['message']['content']
            yield "\n"

            self.history_storage.store_conversion(
                {
                    'role': 'assistant',
                    'content': answer
                }
            )   


        # Stream the main chat response as well
        stream = chat(
            model=self.model_name,
            messages=messages,
            stream=True
        )
        
        answer = ""
        for chunk in stream:
            yield chunk['message']['content'] 
            answer += chunk['message']['content']
        yield "\n"
        self.history_storage.store_conversion(
            {
                'role': 'assistant',
                'content': answer
            }
        )
