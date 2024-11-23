from edge_llm.edge_llm import EdgeLlmStream
edge_llm = EdgeLlmStream("qwen2.5:3b")

# stream = edge_llm.chat([
#     {
#         "role":"user",
#         "content":"J'aimes la pluie et toi ?"
#     }
# ]
# )
# for chunk in stream:
#     print(chunk, end="")

# lesson = {
#     "system_prompt": "In this lesson, you will learn about the subjonctif présent in French, its usage, and conjugation rules. The subjonctif présent is used to express wishes, emotions, doubt, necessity, or possibility. You will practice creating sentences and learn to recognize and use this tense correctly.",
#     "exercices": [
#     {
#         "question": "Conjuguez le verbe 'être' au subjonctif présent à la 3ème personne du singulier (il/elle/on).",
#         "answer_expected": {
#         "model_answer": "soit",
#         "grading_guidelines": "The student should provide the correct conjugation 'soit'. Any deviation, such as 'est' or 'sait', is incorrect."
#         }
#     },
#     {
#         "question": "Écrivez une phrase exprimant un souhait avec le verbe 'venir' au subjonctif présent.",
#         "answer_expected": {
#         "model_answer": "Je souhaite qu'il vienne.",
#         "grading_guidelines": "The sentence must express a wish (e.g., 'je souhaite', 'j'aimerais') and correctly use 'vienne' as the subjonctif form of 'venir'."
#         }
#     },
#     {
#         "question": "Transformez cette phrase en utilisant le subjonctif présent : 'Tu penses qu'il est content.'",
#         "answer_expected": {
#         "grading_guidelines": "The response should replace 'est' with 'soit'. Incorrect use of the indicative (e.g., 'est content') is not acceptable."
#         }
#     },
#     {
#         "question": "Créez une phrase qui exprime une obligation avec le verbe 'faire' au subjonctif présent.",
#         "answer_expected": {
#         "model_answer": "Il faut que tu fasses tes devoirs.",
#         "grading_guidelines": "The sentence should contain an obligation expression (e.g., 'il faut que') and correctly use 'fasses' as the subjonctif form of 'faire'."
#         }
#     },
#     {
#         "question": "Conjuguez le verbe 'avoir' au subjonctif présent à la 1ère personne du pluriel (nous).",
#         "answer_expected": {
#         "model_answer": "ayons",
#         "grading_guidelines": "The student should provide the correct conjugation 'ayons'. Answers like 'avons' (indicative) are incorrect."
#         }
#     },
#     {
#         "question": "Écrivez une phrase exprimant un doute avec le verbe 'pouvoir' au subjonctif présent.",
#         "answer_expected": {
#         "model_answer": "Je doute que nous puissions le faire.",
#         "grading_guidelines": "The sentence should express doubt (e.g., 'je doute que') and correctly use 'puissions' as the subjonctif form of 'pouvoir'."
#         }
#     },
#     {
#         "question": "Transformez cette phrase en utilisant le subjonctif présent : 'Nous voulons qu'il parle.'",
#         "answer_expected": {
#         "model_answer": "Nous voulons qu'il parle.",
#         "grading_guidelines": "The response should remain unchanged as 'parle' is already in the subjonctif présent. Changes that introduce errors (e.g., 'parlons') are incorrect."
#         }
#     },
#     {
#         "question": "Créez une phrase qui exprime une émotion avec le verbe 'aller' au subjonctif présent.",
#         "answer_expected": {
#         "model_answer": "Je suis heureux qu'elle aille bien.",
#         "grading_guidelines": "The sentence should express an emotion (e.g., 'je suis heureux') and correctly use 'aille' as the subjonctif form of 'aller'."
#         }
#     },
#     {
#         "question": "Conjuguez le verbe 'savoir' au subjonctif présent à la 2ème personne du singulier (tu).",
#         "answer_expected": {
#         "model_answer": "saches",
#         "grading_guidelines": "The student should provide the correct conjugation 'saches'. Answers like 'sais' (indicative) are incorrect."
#         }
#     },
#     {
#         "question": "Écrivez une phrase exprimant une nécessité avec le verbe 'voir' au subjonctif présent.",
#         "answer_expected": {
#         "model_answer": "Il est nécessaire que tu voies ce film.",
#         "grading_guidelines": "The sentence should express necessity (e.g., 'il est nécessaire que') and correctly use 'voies' as the subjonctif form of 'voir'."
#         }
#     }
#     ]
# }

# Load model directly
from transformers import AutoModel
model = AutoModel.from_pretrained("devsheroubi/qwen2.5_7b_frenv1tkn")

# for chunk in edge_llm.teach_a_lesson(lesson):
#     print(chunk, end='', flush=True)  # flush=True ensures prompt appears immediately