import torch
import soundfile as sf
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

MODEL_NAME = "facebook/mms-1b-all"

# Load once (important for performance)
processor = Wav2Vec2Processor.from_pretrained(MODEL_NAME)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_NAME)
model.eval()

def transcribe_audio(audio_path):
    # Load audio
    audio, sample_rate = sf.read(audio_path)

    # Mono check
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    # Process
    inputs = processor(
        audio,
        sampling_rate=sample_rate,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]

    return {
        "text": transcription,
        "language": "ug",   # TRUE Uyghur
        "model": "mms-1b-all"
    }