def make_initial_prompt(conversation, mistakes, native_lang, target_lang, KG):

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


def make_update_prompt(conversation, mistakes, native_lang, target_lang, KG):

    update_prompt = f"""
    The following conversation is from a student whose native language is {native_lang} and who is learning {target_lang}.
    The conversation is {conversation}. We have already spotted the following mistakes: {mistakes}.
    The following knowledge graph summuarises the skills set to learn {target_lang}. It has the following structure: {KG}.
    Weights are set between 0 (skill not mastered at all), to 1 (skill fully mastered). They represent the current evaluation of the student's skills in {target_lang}.
    Given the conversation and the mistakes, update the knowledge graph weights (DO NOT CHANGE THE STRUCTURE). At most, weights can change by ±0.1 and are capped by 0 and 1. 
    Output the updated graph:
    """

    return update_prompt


def make_context_summary(KG):

    provide_context = """
    Given the following knowledge graph, give a summary of the current status of the language understanding. Give the level and the areas (grammaire, vocabulaire, orthographe, conjugaison) that look like strong points and those that look like weak ones. 
    """