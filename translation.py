from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from torch.ao.quantization import quantize_dynamic

def load_translator():
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    compiled_model = torch.compile(model)


    model_int8 = quantize_dynamic(
        compiled_model,  # the original model
        {torch.nn.Linear},  # a set of layers to dynamically quantize
        dtype=torch.qint8)
    return model_int8, tokenizer

def translate(model_int8, tokenizer, text):
    input = tokenizer.encode(text, return_tensors="pt")
    output = model_int8.generate(input)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

if __name__ == '__main__':
    model_int8, tokenizer = load_translator()

    text = """A spirit who claims to be the ghost of Hamlet’s father describes his
murder at the hands of Claudius and demands that Hamlet avenge the
killing. When the councilor Polonius learns from his daughter,
Ophelia, that Hamlet has visited her in an apparently distracted state,
Polonius attributes the prince’s condition to lovesickness, and he sets
a trap for Hamlet using Ophelia as bait"""

    translated_sentence = translate(model_int8, tokenizer, text)
    print(translated_sentence)