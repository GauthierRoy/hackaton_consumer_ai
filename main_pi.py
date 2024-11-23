from transformers import VitsModel, AutoTokenizer
from torch import compile
from torch.nn import Linear
import time
import sounddevice as sd
import whisper
import sounddevice as sd
import numpy as np
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.ao.quantization import quantize_dynamic
import torch
import gc

def enfr_load_translator():
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
    return model, tokenizer
    # model = compile(model)
    model = quantize_dynamic(
        model,  # the original model
        {torch.nn.Linear},  # a set of layers to dynamically quantize
        dtype=torch.qint8)
    return model, tokenizer

def fren_load_translator():
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-fr-en")
    return model, tokenizer
    # model = compile(model)
    model = quantize_dynamic(
        model,  # the original model
        {torch.nn.Linear},  # a set of layers to dynamically quantize
        dtype=torch.qint8)
    return model, tokenizer

in_model = whisper.load_model("tiny")
fra_model = VitsModel.from_pretrained("facebook/mms-tts-fra")
fra_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-fra")
eng_model = VitsModel.from_pretrained("facebook/mms-tts-eng")
eng_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
# translation_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")
# translation_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
fren_model, fren_tokenizer = fren_load_translator()
enfr_model, enfr_tokenizer = enfr_load_translator()

# eng_model = quantize_dynamic(eng_model, {torch.nn.Linear}, dtype=torch.qint8)
# fra_model = quantize_dynamic(fra_model, {torch.nn.Linear}, dtype=torch.qint8)


def translate(model_int8, tokenizer, text):
    with torch.no_grad():
        input = tokenizer.encode(text, return_tensors="pt")
        output = model_int8.generate(input)
        return tokenizer.decode(output[0], skip_special_tokens=True)

def transcribe_audio(audio, model, fs=16000):
    with torch.no_grad():
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
            recorded_audio = [audio]
            while True:
                rec_audio = sd.rec(int(2 * fs), samplerate=fs, channels=1, dtyp>
                sd.wait()
                recorded_audio.append(rec_audio)
                if np.max(np.abs(rec_audio)) < threshold:
                    print("Recording stopped.")
                    return np.concatenate(recorded_audio)

while True:
    audio = detect_speech_and_record()
    st = time.time()
    text, lang = transcribe_audio(audio, in_model)
    print("Transcribed Text:", text)
    print(f"Time taken: {time.time() - st:.2f} seconds")
    
    
    print("Detected Language:", lang)


    if lang == "fr":
        translated_text = translate(fren_model, fren_tokenizer, text)
        print("Translated text:", translated_text)
        st = time.time()

        inputs = eng_tokenizer(translated_text, return_tensors="pt")
        with torch.no_grad():
            output = eng_model(**inputs).waveform
        print(f"Time taken: {time.time() - st:.2f} seconds")
        sd.play(output.squeeze().numpy(), eng_model.config.sampling_rate)
        sd.wait()
        del inputs, output, translated_text
    else:
        translated_text = translate(enfr_model, enfr_tokenizer, text)
        print("Translated text:", translated_text)
        st = time.time()
        inputs = fra_tokenizer(translated_text, return_tensors="pt")
        with torch.no_grad():
            output = fra_model(**inputs).waveform
        print(f"Time taken: {time.time() - st:.2f} seconds")
        sd.play(output.squeeze().numpy(), fra_model.config.sampling_rate)
        sd.wait()
        del inputs, output, translated_text
    gc.collect()