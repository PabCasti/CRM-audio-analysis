#     >> conda activate whisperx-web-ui & python 1.0.code_detectAudio.py

# WhisperX: 
#   https://github.com/m-bain/whisperX/tree/main
#   Paper: https://www.robots.ox.ac.uk/~vgg/publications/2023/Bain23/bain23.pdf

import datetime

print(datetime.datetime.now().time())

import whisperx
import json
import gc 

audio_file = "cardiacEscenario.wav" # cardiacEscenario_filter_specific2.wav    ClinicalScenario
results_diarization_file = "results_whisperx_diariz_cardiac_large.txt" # results_whisperx_diarization_filter_specific2.txt
results_speakers_file = "results_whisperx_speaker_cardiac_large.txt" # results_whisperx_speaker_filter_specific2.txt

device = "cpu" #"cuda" 
batch_size = 16 # reduce if low on GPU mem
compute_type = "float32" # change to "int8" if low on GPU mem (may reduce accuracy)
language = "en"

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("large-v2", device, compute_type=compute_type, language=language,
                            asr_options={"patience":0.2}, vad_onset = 0.4, vad_offset = 0.263)
print("Model loaded")

# save model to local path (optional)
# model_dir = "/path/"
# model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
# print(result["segments"]) # before alignment
print("Transcription completed")

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
print("Segments aligned")
# print(result["segments"]) # after alignment


# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

# 3. Assign speaker labels
diarize_model = whisperx.DiarizationPipeline(use_auth_token="HUGGINGFACE_TOKEN", device=device)

# add min/max number of speakers if known
# diarize_segments = diarize_model(audio)
diarize_segments = diarize_model(audio, min_speakers=4, max_speakers=6)
# diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

result = whisperx.assign_word_speakers(diarize_segments, result)
print("Speakers assigned")

with open(results_diarization_file, 'w') as f:
    json.dump(diarize_segments.to_json(), f)

# print(diarize_segments)

with open(results_speakers_file, 'w') as f:
    json.dump(result, f)

# print(result["segments"]) # segments are now assigned speaker IDs

print(datetime.datetime.now().time())


