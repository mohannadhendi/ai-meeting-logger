import torch # type: ignore
import whisper # type: ignore

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base", device=device)

def transcribe_audio(audio_file):
    result = model.transcribe(audio_file)
    return result["text"]

print("Model device:", model.device)