# import torch
# from parler_tts import ParlerTTSForConditionalGeneration
# from transformers import AutoTokenizer
# # import soundfile as sf
# import sounddevice as sd
# import time

# # device = "cuda:0" if torch.cuda.is_available() else "cpu"
# device = "cpu"

# print("Loading model...")
# model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
# tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")

# prompt = "Bonjour, Vous aimez le soleil?"
# description = "A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."


# print("Tokenizing...")
# st = time.time()
# input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
# prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

# print("Generating Audio...")
# generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
# audio_arr = generation.cpu().numpy().squeeze()
# print(f"Time taken: {time.time() - st:.2f} seconds")
# # sf.write("parler_tts_out.wav", audio_arr, model.config.sampling_rate)
# sd.play(audio_arr, model.config.sampling_rate)
# sd.wait()

from transformers import VitsModel, AutoTokenizer
import torch
import time
import sounddevice as sd

fra_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
fra_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

st = time.time()
text = "bonjour, je m'appelle John Doe. Comment ça va?"
inputs = fra_tokenizer(text, return_tensors="pt")

with torch.no_grad():
    output = fra_model(**inputs).waveform

print(f"Time taken: {time.time() - st:.2f} seconds")

sd.play(output.squeeze().numpy(), fra_model.config.sampling_rate)
sd.wait()