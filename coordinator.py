from big_llm import Big_LLM
from edge_llm.edge_llm import EdgeLlmStream


initial_test = {"A1": {
        "system_message": "Présentez-vous en une ou deux phrases. Dites votre nom, votre âge et où vous habitez.",
        "exercises": [
            {
                "question": "Présentez-vous en une ou deux phrases. Dites votre nom, votre âge et où vous habitez.",
                "answer_expected": {
                    "model_answer": "Je m'appelle Marie, j'ai 25 ans et j'habite à Paris.",
                    "grading_guidelines": (
                        "The student should correctly introduce themselves using basic vocabulary and structures, "
                        "such as 'je m'appelle', 'j'ai ... ans', and 'j'habite à ...'. Minor errors (e.g., missing accents) "
                        "are acceptable if they don't hinder comprehension."
                    )
                }
            }
        ]
    },
    "A2": {
        "system_message": "Décrivez votre routine quotidienne en cinq phrases. Par exemple, dites ce que vous faites le matin, l'après-midi et le soir.",
        "exercises": [
            {
                "question": "Décrivez votre routine quotidienne en cinq phrases. Par exemple, dites ce que vous faites le matin, l'après-midi et le soir.",
                "answer_expected": {
                    "model_answer": (
                        "Le matin, je me réveille à 7 heures. Ensuite, je prends mon petit déjeuner. L'après-midi, "
                        "je travaille ou j'étudie. Le soir, je dîne avec ma famille et je regarde la télévision. Enfin, je me couche vers 22 heures."
                    ),
                    "grading_guidelines": (
                        "The student should use common verbs (e.g., 'se réveiller', 'prendre', 'travailler') in the present tense. "
                        "The sentences should be simple and clear, demonstrating familiarity with basic time expressions and routine vocabulary."
                    )
                }
            }
        ]
    },
    "B1": {
        "system_message": "Racontez une expérience de voyage que vous avez faite récemment. Utilisez au moins six phrases pour décrire où vous êtes allé(e), ce que vous avez fait, et comment vous avez trouvé l'expérience.",
        "exercises": [
            {
                "question": "Racontez une expérience de voyage que vous avez faite récemment. Utilisez au moins six phrases pour décrire où vous êtes allé(e), ce que vous avez fait, et comment vous avez trouvé l'expérience.",
                "answer_expected": {
                    "model_answer": (
                        "L'été dernier, je suis allé en Espagne avec ma famille. Nous avons visité Barcelone et Madrid. "
                        "J'ai adoré l'architecture de Gaudi et les musées. Nous avons aussi essayé des plats typiques comme la paella. "
                        "Le temps était magnifique et les gens très accueillants. Ce fut un voyage inoubliable."
                    ),
                    "grading_guidelines": (
                        "The student should use the passé composé to describe past events and demonstrate coherence in their narrative. "
                        "The vocabulary should reflect travel-related topics (e.g., 'visiter', 'manger', 'le temps'). "
                        "Minor grammar mistakes are acceptable if the story remains clear."
                    )
                }
            }
        ]
    },
    "B2": {
        "system_message": (
            "Discutez des avantages et des inconvénients du télétravail. Rédigez une réponse structurée en huit phrases minimum, "
            "en exprimant votre opinion avec des arguments."
        ),
        "exercises": [
            {
                "question": "Discutez des avantages et des inconvénients du télétravail. Rédigez une réponse structurée en huit phrases minimum, en exprimant votre opinion avec des arguments.",
                "answer_expected": {
                    "model_answer": (
                        "Le télétravail présente de nombreux avantages, comme la flexibilité et le gain de temps en évitant les trajets. "
                        "Cependant, il peut être difficile de se concentrer chez soi et de séparer la vie professionnelle et personnelle. "
                        "Certaines personnes trouvent aussi le télétravail isolant, car elles manquent d'interactions sociales. "
                        "D'un autre côté, il permet une meilleure gestion de son emploi du temps et favorise l'équilibre travail-vie personnelle. "
                        "À mon avis, le télétravail est une bonne solution pour certaines professions, mais il n'est pas adapté à tout le monde."
                    ),
                    "grading_guidelines": (
                        "The student should present a balanced argument, using connectors (e.g., 'cependant', 'd'un autre côté') and precise vocabulary. "
                        "The response should show grammatical accuracy and the ability to organize ideas logically. "
                        "Errors are acceptable as long as they do not hinder comprehension."
                    )
                }
            }
        ]
    }
}


class Coordinator:

    def __init__(self):

        self.small_llm = EdgeLlmStream("qwen2.5:7b")
        self.big_llm = Big_LLM()
        self.context = initial_test

    def run(self):
        
        for l in range(10):

            print("ITERATION ", l)
            ##################################################
            # Part where you run the little lm 
            for k in self.context:
                for chunk in self.small_llm.teach_a_lesson(self.context[k]):
                    print(chunk, end='', flush=True)  # flush=True ensures prompt appears immediately

            conversation = self.small_llm.get_conversions()
            mistakes = self.small_llm.get_mistakes()

            # Expected output: history of the conversation (str), mistakes (str)
            
            ##################################################

            _, _, self.context = self.big_llm.total_update(conversation, mistakes, plotting=True)



        # Given the current 

if __name__ == "__main__":
    coord = Coordinator()
    coord.run()  