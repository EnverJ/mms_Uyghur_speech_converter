from transcribe_mms import transcribe_audio

# if __name__ == "__main__":
#     audio_file = "../audio/sample.wav"
#     result = transcribe_audio(audio_file)
#
#     print("Language:", result["language"])
#     print("Text:")
#     print(result["text"])

# Uyghur Arabic
import os
import sounddevice as sd
import soundfile as sf
from transcribe_mms import transcribe_audio

# Simple Latin → Uyghur Arabic mapping
latin_to_arabic = {
    "a": "ا",
    "b": "ب",
    "d": "د",
    "e": "ە",
    "f": "ف",
    "g": "گ",
    "h": "ھ",
    "i": "ى",
    "j": "ژ",
    "k": "ك",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "o": "و",
    "p": "پ",
    "q": "ق",
    "r": "ر",
    "s": "س",
    "t": "ت",
    "u": "ۇ",
    "v": "ۋ",
    "x": "خ",
    "y": "ي",
    "z": "ز",
    "sh": "ش",
    "ch": "چ",
}

def latin_to_uyghur_arabic(text):
    # Handle multi-letter combos first
    text = text.replace("sh", "ش").replace("ch", "چ")
    # Replace remaining single letters
    for latin, arabic in latin_to_arabic.items():
        text = text.replace(latin, arabic)
    return text

def record_audio(filename="../audio/recorded.wav", duration=10, sample_rate=16000):
    """Record audio from mic and save as WAV"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"Recording for {duration} seconds... Speak now!")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    sf.write(filename, audio, sample_rate)
    print(f"Saved recording to {filename}")
    return filename

if __name__ == "__main__":
    # Step 1: Record
    audio_file = record_audio(duration=10)

    # Step 2: Transcribe with MMS
    result = transcribe_audio(audio_file)
    latin_text = result["text"]

    # Step 3: Convert to Uyghur Arabic script
    arabic_text = latin_to_uyghur_arabic(latin_text)

    # Step 4: Print results
    print("\n--- Transcription ---")
    print("Language:", result["language"])
    print("Latin:", latin_text)
    print("Arabic:", arabic_text)