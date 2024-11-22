import whisper
import sounddevice as sd
import numpy as np
import time

model = whisper.load_model("small")

def record_audio(duration, fs=16000):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    return audio

def transcribe_audio(audio, model, fs=16000):
    print("Transcribing...")
    audio = np.squeeze(audio)
    result = model.transcribe(audio)
    return result['text']


# print("Say something...")
# audio = record_audio(30)
# st = time.time()
# text = transcribe_audio(audio, model)
# print("Transcribed Text:", text)
# print(f"Time taken: {time.time() - st:.2f} seconds")

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
                
audio = detect_speech_and_record()
st = time.time()
text = transcribe_audio(audio, model)
print("Transcribed Text:", text)
print(f"Time taken: {time.time() - st:.2f} seconds")

# TODO: Create a second thread to listen for speech while the first thread transcribes the audio