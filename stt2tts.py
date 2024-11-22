from transformers import VitsModel, AutoTokenizer
import torch
import time
import sounddevice as sd
import whisper
import sounddevice as sd
import numpy as np
import time
from transformers import AutoTokenizer, AutoModelForCausalLM

in_model = whisper.load_model("small")
fra_model = VitsModel.from_pretrained("facebook/mms-tts-fra")
fra_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-fra")
eng_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
eng_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")

def transcribe_audio(audio, model, fs=16000):
    print("Transcribing...")
    audio = np.squeeze(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    lang = max(probs, key=probs.get)

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text, lang

def detect_speech_and_record(threshold=0.2, duration=5, fs=16000):
    print("Listening for speech...")
    while True:
        audio = sd.rec(int(1 * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        if np.max(np.abs(audio)) > threshold:
            print("Detected speech! Recording...")
            while True:
                rec_audio = sd.rec(int(2 * fs), samplerate=fs, channels=1, dtype='float32')
                sd.wait()
                audio = np.concatenate((audio, rec_audio))
                if np.max(np.abs(rec_audio)) < threshold:
                    print("Recording stopped.")
                    return audio

def translate_text(text, model, tokenizer, target_lang="fr"):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

while True:
    audio = detect_speech_and_record()
    st = time.time()
    text, lang = transcribe_audio(audio, in_model)
    print("Transcribed Text:", text)
    print(f"Time taken: {time.time() - st:.2f} seconds")
    print("Detected Language:", lang)

    # Translate the transcribed text
    translated_text = translate_text(text, translation_model, translation_tokenizer)
    print("Translated Text:", translated_text)

    inputs = fra_tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        output = fra_model(**inputs).waveform

    print(f"Time taken: {time.time() - st:.2f} seconds")

    sd.play(output.squeeze().numpy(), fra_model.config.sampling_rate)
    sd.wait()
    