from pygrammalecte import grammalecte_text,GrammalecteGrammarMessage

class DetectLangageMistakes:

    def __init__(self):
        self.mistakes_history = []

    def _transform_grammarlect_error(self,text:str,messages:list[GrammalecteGrammarMessage]) -> dict:
        errors = []
        texts = text.splitlines()
        for message in messages:
            if hasattr(message,"type") and message.type == "nbsp":
                continue
            formatted_error = {}
            formatted_error["word_error"] = texts[message.line-1][message.start:message.end]
            formatted_error["rule"] = message.message
            if hasattr(message,"suggestion"):
                formatted_error["suggestion"] = message.suggestions
            errors.append(
                formatted_error
            )
        return errors
        
    
    def spot_mistake(self,text:str)->dict:
        mistakes = grammalecte_text(text)
        if not mistakes:
            return False
        else:
            mistakes_formatted = self._transform_grammarlect_error(text,mistakes)
            if not mistakes_formatted: 
                return False
        self.mistakes_history.extend(mistakes_formatted)
        return mistakes_formatted
