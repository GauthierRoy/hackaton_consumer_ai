# General Functioning

## EdgeLLM

EdgeLLM takes lessons as input from BigLLM.  
Example of a lesson:  
```json
{
    "system_message": "Introductory message for the lesson, e.g., an introduction to passé composé",
    "exercises": [
        {
            "question": "",
            "answer_expected": {
                "model_answer": "Example of a valid answer",
                "grading_guidelines": "Guidelines for evaluating the response"
            }
        }
    ]
}
```

EdgeLLM includes multiple instructions to interact with the user, as it is not intelligent enough to handle tasks independently.  

**Features:**  
- Uses *Grammalecte* to detect French mistakes, converting them into sentences with Qwen2.5 0.5B.  
- Returns a history of mistakes and conversations to BigLLM after filtering sensitive information.  
- Leverages *Qwen2.5 7B* with Ollama and is fine-tuned with synthetic data created in-house.  

---

## BigLLM

BigLLM processes conversations and mistake histories. It updates the user’s knowledge graph and identifies weak areas in their language skills. These weaknesses are used to query the smaller EdgeLLM to generate the next set of lessons.

**Features:**  
- Operates using *Llama 70B* hosted on Scaleway.

---

## Architecture

The system integrates six models to handle Text-to-Speech (TTS), Speech-to-Text (STT), and translation tasks. Each task uses two models, which are precompiled and quantized to run concurrently on a Raspberry Pi.  

**Knowledge Graph:**  
The knowledge graph represents French language skills, categorized by levels (A1, A2, B1, B2) and divided into four main areas:  
- Vocabulary (*Vocabulaire*)  
- Grammar (*Grammaire*)  
- Conjugation (*Conjugaison*)  
- Spelling (*Orthographe*)  

Knowledge graphs are visualized using NetworkX for plotting.
