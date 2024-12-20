import requests
import json
import numpy as np
from typing import List
import random

from graph_plotting import graph_plotting

class Big_LLM():

    def __init__(self):

        self.IAM_API_KEY = "334d920a-dfb3-4aea-ab17-c8a37b58423a"
        self.DEPLOYMENT_UUID = "38ed1927-8685-4925-a3f6-de02fb09bf3b"

        self.URL = f"https://api.scaleway.ai/{self.DEPLOYMENT_UUID}/v1/chat/completions"

        self.HEADERS = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.IAM_API_KEY}" # Replace $SCW_API_KEY with your IAM API key
        }

        self.has_initialised = False
        
        self.KG = {
            'A1': {
                'Grammaire': [
                    ['Articles définis et indéfinis', 'Utilisation de le, la, les et un, une, des', 0],
                    ['Pronoms personnels sujets', 'Utilisation de je, tu, il/elle, nous, vous, ils/elles', 0],
                    ['Adjectifs qualificatifs', 'Accord des adjectifs en genre et en nombre', 0],
                    ['Négation', 'Formation de la négation avec ne... pas', 0],
                    ['Questions simples', 'Formation de questions avec qui, que, où, pourquoi', 0]
                ],
                'Vocabulaire': [
                    ['Présentations', 'Se présenter et poser des questions simples', 0],
                    ['Famille et relations', 'Nommer les membres de la famille et les relations', 0],
                    ['Maison et objets quotidiens', 'Décrire les pièces et objets courants', 0],
                    ['Transports', 'Nommer les moyens de transport courants', 0],
                    ['Couleurs, nombres et jours', 'Apprendre les couleurs, nombres et jours', 0]
                ],
                'Orthographe': [
                    ['Genres des noms', 'Différencier masculin et féminin', 0],
                    ['Pluriels réguliers et irréguliers', 'Formation des pluriels (-s, -x)', 0],
                    ['Accents sur les voyelles', 'Utilisation correcte des accents (é, è, à, etc.)', 0],
                    ['Confusions courantes', 'Différencier les homophones courants (a/à, et/est)', 0],
                    ['Ponctuation', 'Règles basiques de ponctuation', 0]
                ],
                'Conjugaison': [
                    ['Présent des verbes en -ER', 'Conjuguer les verbes réguliers en -ER', 0],
                    ['Présent des verbes en -IR', 'Conjuguer les verbes réguliers en -IR', 0],
                    ['Présent des verbes irréguliers', 'Conjuguer les verbes être, avoir, aller, faire', 0],
                    ['Futur proche', 'Utiliser aller + infinitif pour parler du futur', 0],
                    ['Verbes pronominaux', "Utilisation de se lever, s'appeler, etc.", 0]
                ]
            },
            'A2': {
                'Grammaire': [
                    ['Articles contractés', 'Utilisation de au, du, des', 0],
                    ['Pronoms compléments', 'Utilisation de me, te, lui, nous, vous, leur', 0],
                    ['Adjectifs démonstratifs', 'Utilisation de ce, cet, cette, ces', 0],
                    ['Adverbes de fréquence', 'Placer les adverbes (souvent, toujours, parfois)', 0],
                    ['Discours rapporté au présent', "Utilisation de que et d'autres subordonnées", 0]
                ],
                'Vocabulaire': [
                    ['Santé et bien-être', 'Nommer les parties du corps et parler de la santé', 0],
                    ['Vie quotidienne', 'Parler de ses activités et de ses routines', 0],
                    ['Voyages et vacances', 'Nommer les lieux et les activités de voyage', 0],
                    ['Météo et environnement', 'Décrire la météo et parler de la nature', 0],
                    ['Achats et consommation', 'Nommer les produits et faire des achats', 0]
                ],
                'Orthographe': [
                    ['Accord sujet-verbe', 'Respecter les accords dans les phrases complexes', 0],
                    ['Pluriels irréguliers avancés', 'Formation des pluriels complexes (bijou -> bijoux)', 0],
                    ['Mots composés', "Comprendre l'écriture des mots composés", 0],
                    ['Homonymes et paronymes', "Différencier les mots proches (c'est/ses/ces)", 0]
                ],
                'Conjugaison': [
                    ['Passé composé avec avoir', 'Conjuguer les verbes réguliers et irréguliers au passé composé', 0],
                    ['Passé composé avec être', 'Conjuguer les verbes de mouvement au passé composé', 0],
                    ['Imparfait', 'Conjuguer les verbes pour décrire des actions habituelles ou continues', 0],
                    ['Futur simple', 'Utiliser le futur simple pour des événements à venir', 0],
                    ['Verbes pronominaux au passé', 'Conjuguer les verbes pronominaux au passé composé', 0]
                ]
            },
            'B1': {
                'Grammaire': [
                    ['Pronoms relatifs', 'Utilisation de qui, que, dont, où', 0],
                    ['Exprimer le subjonctif présent', "Exprimer le doute, le désir, ou l'obligation", 0],
                    ['Voix passive', 'Formation et utilisation de la voix passive', 0],
                    ['Gérondif', 'Formation et utilisation du gérondif', 0]
                ],
                'Vocabulaire': [
                    ['Travail et emploi', 'Parler du monde professionnel', 0],
                    ['Éducation et études', "Parler de l'école, de l'université, et des formations", 0],
                    ['Médias et technologie', 'Nommer les outils technologiques et parler des médias', 0],
                    ['Vie sociale', 'Parler des interactions sociales et des relations', 0],
                    ['Problèmes de société', 'Nommer les défis sociaux et économiques', 0]
                ],
                'Orthographe': [
                    ['Homophones grammaticaux complexes', 'Différencier leurs, ce/se, on/ont', 0],
                    ['Accord des participes passés', "Règles d'accord des participes avec avoir et être", 0],
                    ['Noms et adjectifs dérivés', 'Écriture correcte des dérivés (ex. science -> scientifique)', 0],
                    ['Verbes irréguliers complexes', 'Écrire correctement les conjugaisons irrégulières', 0]
                ],
                'Conjugaison': [
                    ['Subjonctif présent', 'Conjuguer les verbes réguliers et irréguliers au subjonctif', 0],
                    ['Futur antérieur', "Utiliser le futur antérieur pour parler d'actions futures accomplies", 0],
                    ['Conditionnel passé', 'Exprimer des regrets ou des hypothèses non réalisées', 0],
                    ['Participe présent', 'Utilisation et formation du participe présent', 0],
                    ['Discours indirect au passé', 'Rapporter des propos au passé', 0]
                ]
            }, 
            'B2': {
                'Grammaire': [
                    ['Pronoms relatifs composés', 'Utilisation de lequel, laquelle, duquel, auquel, etc.', 0],
                    ['Concordance des temps avancée', 'Harmonisation des temps dans des phrases complexes', 0],
                    ['Hypothèses', 'Utilisation de si + imparfait, conditionnel ou plus-que-parfait', 0],
                    ['Expressions idiomatiques', 'Comprendre et utiliser des expressions courantes', 0]
                ],
                'Vocabulaire': [
                    ['Relations internationales', 'Nommer et décrire les enjeux internationaux', 0],
                    ['Arts et culture', "Parler de la littérature, de l'art et de la musique", 0],
                    ['Développement durable', "Nommer les concepts liés à l'écologie et au développement durable", 0],
                    ['Vie professionnelle', 'Parler des compétences, des métiers et des enjeux professionnels', 0]
                ],
                'Orthographe': [
                    ['Néologismes et emprunts', "Écrire correctement les mots nouveaux ou empruntés à d'autres langues", 0],
                    ['Subtilités des accents', 'Maîtriser les nuances des accents sur les voyelles complexes', 0],
                    ['Homophones avancés', 'Différencier des homophones rares comme bal/balle, saut/sot', 0],
                    ['Pluriels complexes', "Gérer les pluriels des noms composés et des mots d'origine étrangère", 0]
                ],
                'Conjugaison': [
                    ['Subjonctif passé', 'Conjuguer les verbes réguliers et irréguliers au subjonctif passé', 0],
                    ['Conditionnel passé deuxième forme', 'Utilisation avancée du conditionnel passé', 0],
                    ['Futur antérieur avancé', 'Expliquer des actions futures déjà terminées', 0],
                    ['Participes passés et accords complexes', 'Accords avancés des participes passés', 0]
                ]
            }
        }
        
        for level in self.KG:
            for category in self.KG[level]:
                for lesson in self.KG[level][category]:
                    lesson[0] = lesson[0].lower().replace(",", "").replace("(", "").replace(")", "").replace("'", "")
                    lesson[1] = lesson[1].lower().replace(",", "").replace("(", "").replace(")", "").replace("'", "")

        #self.KG = {'A1': {'Grammaire': [('Articles définis et indéfinis', 'Utilisation de le, la, les et un, une, des', 0)]}}
        self.all_levels = ["A1", "A2", "B1", "B2"]
        self.current_level = 0

    def get_llm_answer(self, system_prompt:str, user_prompt:str, long=False):
        
        max_tokens = 3000 if long else 512

        PAYLOAD = {
        "model": "llama-3.1-70b-instruct",
        "messages": [
                { "role": "system", "content": system_prompt },
                { "role": "user", "content": user_prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": 0.5,
            "top_p": 0.7,
            "presence_penalty": 0.1,
            "stream": True,
        }

        response = requests.post(self.URL, headers=self.HEADERS, data=json.dumps(PAYLOAD), stream=True)

        # transform llm response to knowledge graph
        full_response = ""

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8").strip()
                if decoded_line == "data: [DONE]":
                    break
                if decoded_line.startswith("data: "):
                    try:
                        data = json.loads(decoded_line[len("data: "):])
                        content = data["choices"][0]["delta"].get("content")
                        if content:
                            full_response += content  # Concatenate the content to the full response
                    except json.JSONDecodeError:
                        continue

        return full_response
    

    def total_update(self, conversation:str, mistakes:str, native_lang="english", target_lang="french", plotting=False):
        self.reply(conversation, mistakes, native_lang, target_lang)
        min_topics, max_topics, suggested_new_lessons = self.get_kg_summary()
        exercises = self.make_prompts_for_future_lessons(suggested_new_lessons)

        if plotting is True:
            graph_plotting(self.KG)

        return min_topics, max_topics, exercises


    def reply(self, conversation:str, mistakes:str, native_lang:str, target_lang:str):

        if not self.has_initialised:
            initial_prompt = self.make_initial_prompt(conversation, mistakes, native_lang, target_lang, self.KG)
        else:
            initial_prompt = self.make_update_prompt(conversation, mistakes, native_lang, target_lang, self.KG)

        # Print or use the full response as needed
        kg = self.get_llm_answer(f"You are a JSON formatting assistant with expertise in language learning and evaluation, particularly for French. Your task is to process text inputs and return data extracted from them in JSON format only. You must not include any additional text, explanations, or commentary. Respond with JSON alone, adhering strictly to the format provided in the user's prompt of the knowledge graph.", initial_prompt, long=True)
        
        kg = kg.replace("'", '"')
        self.KG = json.loads(kg)

        self.has_initialised = True

        #Put some noise into the KG
        
        for level in self.KG:
            for category in self.KG[level]:
                for lesson in self.KG[level][category]:
                    lesson[2] = min(max(np.random.uniform(-0.3, 0.5)*0.08+lesson[2], 0), 1)
        

        print("KG:", kg)


    def get_kg_summary(self):
        """ 
        outuput:
        - min_topics: list of topics that need to be improved
        - max_topics: list of topics that are mastered
        - suggested_new_lessons: list of lessons that could be added
        - suggested_former_lessons: list of lessons that could be reviewed
        """

        #gather the summary of the KG for each level
        summary = {}

        for level in self.KG:
            summary[level] = {}

            for category in self.KG[level]:
                cat_score = 0
                total = 0

                for _, _, weight in self.KG[level][category]:
                    cat_score += weight
                    total += 1

                summary[level][category] = cat_score / total

        #Update current level
        for level in range(len(self.all_levels)):
            if level>=self.current_level and np.mean(list(summary[self.all_levels[level]].values())) >= 0.8:
                self.current_level = level

        full_summary = {}
        for level in summary:
            full_summary[level] = np.mean(list(summary[level].values()))

        #Gather weak and strong points for the given level
        min_topics = self.get_min_topics(self.all_levels[self.current_level])
        max_topics = self.get_max_topics(self.all_levels[self.current_level])

        #Add suggested lessons
        sampling_proba = self.get_level_sampling_probability(full_summary)
        epslion = np.random.uniform(0, 1)

        # lesson[0] is the name, lesson[1] is the description, lesson[2] is the weight
        suggested_new_lessons = []

        for _ in range(3):

            if epslion < sampling_proba[0] or epslion < sampling_proba[1]:
                if epslion < sampling_proba[0]:
                    level = self.current_level -1
                elif epslion < sampling_proba[1]:
                    level = self.current_level

                    found = False
                    while found == False:
                        k = np.random.choice(list(self.KG[self.all_levels[level]].keys()))
                        lesson = random.choice(self.KG[self.all_levels[level]][k])
                        if lesson[2] <= full_summary[self.all_levels[level]] and lesson[0] + " " + lesson[1] not in suggested_new_lessons:
                            found = True
                            suggested_new_lessons.append(lesson[0] + " " + lesson[1])

            else:
                level = self.current_level + 1

                found = False
                while found == False:
                    k = np.random.choice(list(self.KG[self.all_levels[level]].keys()))
                    lesson = random.choice(self.KG[self.all_levels[level]][k])
                    if lesson[2] >= full_summary[self.all_levels[level]] and lesson[0] + " " + lesson[1] not in suggested_new_lessons:
                        found = True
                        suggested_new_lessons.append(lesson[0] + " " + lesson[1])



                    
        return min_topics, max_topics, suggested_new_lessons
    
    def get_level_sampling_probability(self, full_summary):
        previous = self.current_level - 1 if self.current_level > 0 else None
        next = self.current_level + 1 if self.current_level < len(self.all_levels) - 1 else None
        total = 0


        if previous is not None:
            total+=full_summary[self.all_levels[previous]]
            previous_score = full_summary[self.all_levels[previous]]
        else:
            previous_score = 0

        if next is not None:
            total+=full_summary[self.all_levels[next]]
            next_score = full_summary[self.all_levels[next]]
        else:
            next_score = 0

        total+=full_summary[self.all_levels[self.current_level]]

        return [previous_score/total, full_summary[self.all_levels[self.current_level]]/total, next_score/total]


    
    def get_min_topics(self, level:str, threshold=0.2):
        level_data = self.KG.get(level, {})
        mean_scores = {}
        
        # Calculate mean score for each key in the level
        for key, topics in level_data.items():
            scores = [item[2] for item in topics]  # Extract scores from position 2
            mean_scores[key] = sum(scores) / len(scores) if scores else float('inf')  # Handle empty topics

        # Filter keys with mean score ≤ threshold
        min_topics = [key for key, mean in mean_scores.items() if mean <= threshold]

        # If none is found, return the one with the lowest mean score
        if not min_topics:
            min_topics = [min(mean_scores, key=mean_scores.get)]

        return min_topics
    
    def get_max_topics(self, level:str, threshold=0.8):
        level_data = self.KG.get(level, {})
        mean_scores = {}
        
        # Calculate mean score for each key in the level
        for key, topics in level_data.items():
            scores = [item[2] for item in topics]  # Extract scores from position 2
            mean_scores[key] = sum(scores) / len(scores) if scores else float('-inf')  # Handle empty topics

        # Filter keys with mean score ≥ threshold
        max_topics = [key for key, mean in mean_scores.items() if mean >= threshold]

        # If none is found, return the one with the highest mean score
        if not max_topics:
            max_topics = [max(mean_scores, key=mean_scores.get)]

        return max_topics


    def make_initial_prompt(self, conversation:str, mistakes:str, native_lang:str, target_lang:str, KG):

        initial_prompt = f"""
        The following conversation is from a student whose native language is {native_lang} and who is learning {target_lang}.
        The conversation is {conversation}. We have already spotted the following mistakes: {mistakes}.
        The following knowledge graph summuarises the skills set to learn {target_lang}. It has the following structure: {KG}.
        You notice that all the weights are set to 0, this is the initial conditions. Try to update the weights in a coherent way given the conversation. 
        Weights are set between 0 (skill not mastered at all), to 1 (skill fully mastered). You must set a weight to each skill given the conversation and the mistakes made. The graph will reflect the level of a student. 
        Fill in the knowledge graph smartly, meaning don't put a high score in a skill in B2 and low score in A1, there should be some logic: mastering B1 means you have good scores in A1 and A2 overall (not necessarily 1 everywhere but 0.8 at least).
        If you feel like the student has a good level, give a good score to the skills that are in equivalent or lower language level even if you haven't necessarily evaluated them. 
        Output the updated graph:
        """

        return initial_prompt


    def make_update_prompt(self, conversation:str, mistakes:str, native_lang:str, target_lang:str, KG):

        update_prompt = f"""
        The following conversation is from a student whose native language is {native_lang} and who is learning {target_lang}.
        The conversation is {conversation}. We have already spotted the following mistakes: {mistakes}.
        The following knowledge graph summuarises the skills set to learn {target_lang}. It has the following structure: {KG}.
        Weights are set between 0 (skill not mastered at all), to 1 (skill fully mastered). They represent the current evaluation of the student's skills in {target_lang}.
        Given the conversation and the mistakes, update the knowledge graph weights (DO NOT CHANGE THE STRUCTURE). At most, weights can change by ±0.1 and are capped by 0 and 1. 
        Output the updated graph:
        """

        return update_prompt
    
    def make_prompts_for_future_lessons(self, topics:List[str]):
        
        sys_prompt = """
            ["<Provide a SHORT introductory instruction or context for the exercise.>", "<Clearly state the question or exercise prompt>", "<Provide an exemplary response for the given question>", "Specify detailed criteria to evaluate the response."]
        """

        stri = "lesson "
        exercises = {}
        i = 1
        for topic in topics:

            sample_dict = {
                        "system_message": None,
                        "exercises": [
                            {
                                "question": None,
                                "answer_expected": {
                                    "model_answer": None,
                                    "grading_guidelines": None
                                }
                            }
                        ]
                    }
            
            new = self.get_llm_answer("ONLY OUTPUT THE DESIRED LIST with 4 elements " + sys_prompt + " ONLY use commas between the 4 elements, NO COMMA inside a given element", f"The topic is the following {topic}")

            new = new.replace("\n", "").replace("[", "").replace("]", "")
            new = new.split(",")

            sample_dict["system_message"] = (new[0])
            sample_dict["exercises"][0]["question"] = new[1]
            sample_dict["exercises"][0]["answer_expected"]["model_answer"] = new[2]
            sample_dict["exercises"][0]["answer_expected"]["grading_guidelines"] = new[3]

            exercises[stri + str(i)] = sample_dict

            i+=1
            
        return exercises

 

if __name__ == "__main__":
    big_llm = Big_LLM()
    conversation = "question: Explain your day in French, answer: J'ai mangé des croissantes cet matin et je allé a la marché pour acheter mes nourrittures. Puis, j'ai rencontré mes amis pour boire un verre de café."
    mistakes = "'croissantes' should be 'croissants', 'cet matin' should be 'ce matin', 'allé' should be 'suis allé', 'mes nourrittures' should be 'de la nourriture', 'boire un verre de café' could be 'un café'"
    native_lang = "English"
    target_lang = "French"
    min_topics, max_topics, exercises = big_llm.total_update(conversation, mistakes, native_lang, target_lang, plotting=True)
    print(min_topics, max_topics, exercises)