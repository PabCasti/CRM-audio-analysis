
import whisper
import json


model = whisper.load_model("medium.en")
result = model.transcribe("cardiacEscenario.wav") 

with open("whisper_result.json", 'w') as f:
    json.dump(result, f)


