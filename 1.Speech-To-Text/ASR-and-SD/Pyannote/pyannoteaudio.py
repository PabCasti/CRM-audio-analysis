
import time
start = time.time() # s

############ CODE ############
import torch


end = time.time() # s
runtime = (end - start)
print(f"Runtime import torch {runtime:.1f} s")
# Runtime import torch 18.1 s


print("-----------------------------------------------------------------------")

############ CODE ############
from pyannote.audio import Pipeline

end = time.time() # s
runtime = (end - start)
print(f"Runtime import pyannote {runtime:.1f} s")
start = time.time() # s

############ CODE ############
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="HUGGINGFACE_TOKEN")


end = time.time() # s
runtime = (end - start)
print(f"Runtime load pretrained {runtime:.1f} s")


print("-----------------------------------------------------------------------")

############ CODE ############
pipeline.params = {
    "max_num_speakers": 5
}
pipeline.to(torch.device("cuda"))


end = time.time() # s
runtime = (end - start)
print(f"Runtime associate to torch device cuda {runtime:.1f} s")
# Runtime associate to torch device cuda 49.7 s


print("-----------------------------------------------------------------------")

############ CODE ############
diarization = pipeline("cardiacEscenario.wav") # .wav para mayor compatibilidad. "UserWarning: The MPEG_LAYER_III subtype is unknown to TorchAudio"


end = time.time() # s
runtime = (end - start)
print(f"Runtime apply pretrained model {runtime:.1f} s")


print("-----------------------------------------------------------------------")

############ CODE ############
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")


end = time.time() # s
runtime = (end - start)
print(f"Runtime show speaker results {runtime:.1f} s")

