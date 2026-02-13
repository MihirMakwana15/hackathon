from faster_whisper import WhisperModel

model = WhisperModel("base")

def transcribe(path):
    segments, _ = model.transcribe(path)
    text = ""
    for s in segments:
        text += s.text
    return text
