
"""
import whisper

# Load the Whisper model (choose a model size: tiny, base, small, medium, large, or turbo)
model = whisper.load_model("turbo")  # Replace "turbo" with your desired model size

# Path to your audio file
audio_file = "audio.mp3"  # Replace with the path to your audio file (e.g., .mp3, .wav, .flac)

# Transcribe the audio
result = model.transcribe(audio_file)

# Print the transcribed text
print("Transcription:")
print(result["text"])

"""

import subprocess
import sys
import threading

def record_audio():
    """Function to start ffmpeg recording."""
    print("Recording... Press Enter again to stop.")
    global recording_process
    recording_process = subprocess.Popen(
        ["ffmpeg", "-f", "avfoundation", "-i", ":0", "output.wav"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    recording_process.communicate()

def stop_recording():
    """Function to stop ffmpeg recording."""
    print("Stopping recording...")
    if recording_process:
        recording_process.stdin.write(b"q\n")
        recording_process.stdin.flush()
        recording_process.terminate()

if __name__ == "__main__":
    try:
        print("Press Enter to start recording...")
        input()  # Wait for the first Enter key press
        threading.Thread(target=record_audio).start()

        input()  # Wait for the second Enter key press
        stop_recording()

        print("Recording saved as 'output.wav'.")
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
