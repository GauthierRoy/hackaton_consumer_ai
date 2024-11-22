import requests
import json
import numpy as np

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

        self.KG = {'A1': {'Grammaire': [('Articles définis et indéfinis', 'Utilisation de le, la, les et un, une, des', 0), ('Pronoms personnels sujets', 'Utilisation de je, tu, il/elle, nous, vous, ils/elles', 0), ('Adjectifs qualificatifs', 'Accord des adjectifs en genre et en nombre', 0), ('Structure de la phrase simple', 'Construction de phrases simples sujet-verbe-objet', 0), ('Négation', 'Formation de la négation avec ne... pas', 0), ('Questions simples', 'Formation de questions avec qui, que, où, pourquoi', 0)], 'Vocabulaire': [('Présentations', 'Se présenter et poser des questions simples', 0), ('Famille et relations', 'Nommer les membres de la famille et les relations', 0), ('Maison et objets quotidiens', 'Décrire les pièces et objets courants', 0), ('Alimentation et boissons', 'Nommer des aliments et des boissons', 0), ('Transports', 'Nommer les moyens de transport courants', 0), ('Couleurs, nombres et jours', 'Apprendre les couleurs, nombres et jours', 0)], 'Orthographe': [('Genres des noms', 'Différencier masculin et féminin', 0), ('Pluriels réguliers et irréguliers', 'Formation des pluriels (-s, -x)', 0), ('Accents sur les voyelles', 'Utilisation correcte des accents (é, è, à, etc.)', 0), ('Liaison et élision', 'Usage des apostrophes et des liaisons', 0), ('Confusions courantes', 'Différencier les homophones courants (a/à, et/est)', 0), ('Ponctuation', 'Règles basiques de ponctuation', 0)], 'Conjugaison': [('Présent des verbes en -ER', 'Conjuguer les verbes réguliers en -ER', 0), ('Présent des verbes en -IR', 'Conjuguer les verbes réguliers en -IR', 0), ('Présent des verbes irréguliers', 'Conjuguer les verbes être, avoir, aller, faire', 0), ('Futur proche', 'Utiliser aller + infinitif pour parler du futur', 0), ('Impératif', "Donner des ordres ou conseils avec l'impératif", 0), ('Verbes pronominaux', "Utilisation de se lever, s'appeler, etc.", 0)]}, 
                     'A2': {'Grammaire': [('Articles contractés', 'Utilisation de au, du, des', 0), ('Pronoms compléments', 'Utilisation de me, te, lui, nous, vous, leur', 0), ('Adjectifs démonstratifs', 'Utilisation de ce, cet, cette, ces', 0), ('Adverbes de fréquence', 'Placer les adverbes (souvent, toujours, parfois)', 0), ('Comparatif et superlatif', 'Exprimer des comparaisons (plus que, moins que)', 0), ('Discours rapporté au présent', "Utilisation de que et d'autres subordonnées", 0)], 'Vocabulaire': [('Santé et bien-être', 'Nommer les parties du corps et parler de la santé', 0), ('Vie quotidienne', 'Parler de ses activités et de ses routines', 0), ('Voyages et vacances', 'Nommer les lieux et les activités de voyage', 0), ('Météo et environnement', 'Décrire la météo et parler de la nature', 0), ('Loisirs et intérêts', 'Parler de ses hobbies et activités', 0), ('Achats et consommation', 'Nommer les produits et faire des achats', 0)], 'Orthographe': [('Accord sujet-verbe', 'Respecter les accords dans les phrases complexes', 0), ('Pluriels irréguliers avancés', 'Formation des pluriels complexes (bijou -> bijoux)', 0), ('Accents et prononciation', "Maitriser les nuances d'accents sur les voyelles", 0), ('Mots composés', "Comprendre l'écriture des mots composés", 0), ('Homonymes et paronymes', "Différencier les mots proches (c'est/ses/ces)", 0)], 'Conjugaison': [('Passé composé avec avoir', 'Conjuguer les verbes réguliers et irréguliers au passé composé', 0), ('Passé composé avec être', 'Conjuguer les verbes de mouvement au passé composé', 0), ('Imparfait', 'Conjuguer les verbes pour décrire des actions habituelles ou continues', 0), ('Futur simple', 'Utiliser le futur simple pour des événements à venir', 0), ('Conditionnel présent', 'Exprimer la politesse ou une hypothèse avec le conditionnel', 0), ('Verbes pronominaux au passé', 'Conjuguer les verbes pronominaux au passé composé', 0)]},
                       'B1': {'Grammaire': [('Pronoms relatifs', 'Utilisation de qui, que, dont, où', 0), ('Exprimer le subjonctif présent', "Exprimer le doute, le désir, ou l'obligation", 0), ('Voix passive', 'Formation et utilisation de la voix passive', 0), ('Pronoms toniques', 'Utilisation de moi, toi, lui, elle, nous, vous, eux, elles', 0), ('Gérondif', 'Formation et utilisation du gérondif', 0)], 'Vocabulaire': [('Travail et emploi', 'Parler du monde professionnel', 0), ('Éducation et études', "Parler de l'école, de l'université, et des formations", 0), ('Médias et technologie', 'Nommer les outils technologiques et parler des médias', 0), ('Vie sociale', 'Parler des interactions sociales et des relations', 0), ('Voyages et expériences', "Décrire des expériences de voyages ou d'aventures", 0), ('Problèmes de société', 'Nommer les défis sociaux et économiques', 0)], 'Orthographe': [('Homophones grammaticaux complexes', 'Différencier leurs, ce/se, on/ont', 0), ('Accord des participes passés', "Règles d'accord des participes avec avoir et être", 0), ('Noms et adjectifs dérivés', 'Écriture correcte des dérivés (ex. science -> scientifique)', 0), ('Préfixes et suffixes', 'Comprendre les préfixes et suffixes pour créer des mots', 0), ('Verbes irréguliers complexes', 'Écrire correctement les conjugaisons irrégulières', 0)], 'Conjugaison': [('Subjonctif présent', 'Conjuguer les verbes réguliers et irréguliers au subjonctif', 0), ('Futur antérieur', "Utiliser le futur antérieur pour parler d'actions futures accomplies", 0), ('Conditionnel passé', 'Exprimer des regrets ou des hypothèses non réalisées', 0), ('Participe présent', 'Utilisation et formation du participe présent', 0), ('Plus-que-parfait', 'Exprimer une action antérieure à une autre action passée', 0), ('Discours indirect au passé', 'Rapporter des propos au passé', 0)]},
                         'B2': {'Grammaire': [('Pronoms relatifs composés', 'Utilisation de lequel, laquelle, duquel, auquel, etc.', 0), ('Concordance des temps avancée', 'Harmonisation des temps dans des phrases complexes', 0), ('Hypothèses', 'Utilisation de si + imparfait, conditionnel ou plus-que-parfait', 0), ('Connecteurs logiques', 'Utilisation de connecteurs comme cependant, néanmoins, puisque', 0), ('Expressions idiomatiques', 'Comprendre et utiliser des expressions courantes', 0)], 'Vocabulaire': [('Relations internationales', 'Nommer et décrire les enjeux internationaux', 0), ('Actualités et politique', "Parler des sujets d'actualité et des systèmes politiques", 0), ('Sciences et technologies', 'Nommer des avancées scientifiques et parler des nouvelles technologies', 0), ('Arts et culture', "Parler de la littérature, de l'art et de la musique", 0), ('Développement durable', "Nommer les concepts liés à l'écologie et au développement durable", 0), ('Vie professionnelle', 'Parler des compétences, des métiers et des enjeux professionnels', 0)], 'Orthographe': [('Néologismes et emprunts', "Écrire correctement les mots nouveaux ou empruntés à d'autres langues", 0), ('Subtilités des accents', 'Maîtriser les nuances des accents sur les voyelles complexes', 0), ('Homophones avancés', 'Différencier des homophones rares comme bal/balle, saut/sot', 0), ('Ponctuation stylistique', 'Utilisation avancée des parenthèses, tirets longs et points-virgules', 0), ('Orthographe des verbes complexes', 'Écrire correctement les conjugaisons des verbes rares', 0), ('Pluriels complexes', "Gérer les pluriels des noms composés et des mots d'origine étrangère", 0)], 'Conjugaison': [('Subjonctif passé', 'Conjuguer les verbes réguliers et irréguliers au subjonctif passé', 0), ('Conditionnel passé deuxième forme', 'Utilisation avancée du conditionnel passé', 0), ('Futur antérieur avancé', 'Expliquer des actions futures déjà terminées', 0), ('Plus-que-parfait avancé', 'Utiliser le plus-que-parfait dans des contextes complexes', 0), ('Participes passés et accords complexes', 'Accords avancés des participes passés', 0)]}}

        self.all_levels = ["A1", "A2", "B1", "B2"]
        self.current_level = 0


    def total_update(self, conversation, mistakes, native_lang, target_lang, plotting=False):
        self.reply(conversation, mistakes, native_lang, target_lang)
        min_topics, max_topics, suggested_new_lessons, suggested_former_lessons = self.get_kg_summary()

        if plotting is True:
            self.plot_graph()


    def reply(self, conversation, mistakes, native_lang, target_lang):

        if not self.has_initialised:
            initial_prompt = self.make_initial_prompt(conversation, mistakes, native_lang, target_lang, self.KG)
        else:
            initial_prompt = self.make_update_prompt(conversation, mistakes, native_lang, target_lang, self.KG)
        
        PAYLOAD = {
        "model": "llama-3.1-70b-instruct",
        "messages": [
                { "role": "system", "content": f"You are an expert in language learning and evaluation, in particular for {target_lang}." },
                { "role": "user", "content": initial_prompt},
            ],
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7,
            "presence_penalty": 0,
            "stream": True,
        }

        response = requests.post(self.URL, headers=self.HEADERS, data=json.dumps(PAYLOAD), stream=True)

        # Initialize an empty string to store the full response content
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

        # Print or use the full response as needed
        self.KG = full_response
        self.has_initialised = True


    def get_kg_summary(self):

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
            if level>=self.current_level and np.mean(list(summary[level].values())) >= 0.8:
                self.current_level = level

        #Gather weak and strong points for the given level
        min_topics = [key for key, value in summary.items() if value <= 0.2]
        if not min_topics:
            min_topics = [min(summary, key=summary.get)]

        max_topics = [key for key, value in summary.items() if value >= 0.8]
        if not max_topics:
            max_topics = [min(summary, key=summary.get)]

        suggested_new_lessons = []
        for k in min_topics:
            for lesson in self.KG[k]:
                if lesson[2] <= 0.4:
                    suggested_new_lessons.append((lesson[0], lesson[1]))

        #Figure out whether there is a weak spot in previous levels
        suggested_former_lessons = []
        if self.current_level > 0:
            previous_level = self.all_levels[self.current_level - 1]

            for lesson in self.KG[previous_level]:
                if lesson[2] <= 0.7:
                    suggested_former_lessons.append((lesson[0], lesson[1]))
                
        return min_topics, max_topics, suggested_new_lessons, suggested_former_lessons
    
    def plot_graph(self):
        return None


    def make_initial_prompt(self, conversation, mistakes, native_lang, target_lang, KG):

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


    def make_update_prompt(self, conversation, mistakes, native_lang, target_lang, KG):

        update_prompt = f"""
        The following conversation is from a student whose native language is {native_lang} and who is learning {target_lang}.
        The conversation is {conversation}. We have already spotted the following mistakes: {mistakes}.
        The following knowledge graph summuarises the skills set to learn {target_lang}. It has the following structure: {KG}.
        Weights are set between 0 (skill not mastered at all), to 1 (skill fully mastered). They represent the current evaluation of the student's skills in {target_lang}.
        Given the conversation and the mistakes, update the knowledge graph weights (DO NOT CHANGE THE STRUCTURE). At most, weights can change by ±0.1 and are capped by 0 and 1. 
        Output the updated graph:
        """

        return update_prompt

 