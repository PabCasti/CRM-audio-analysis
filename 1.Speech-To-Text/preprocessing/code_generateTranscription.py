
import json


# It is necessary the speakers_file.txt

results_speakers_file = "results_whisperx_speaker_filter_600hz"
results_speakers_file = "results_whisperx_speaker_filter_800hz"
results_speakers_file = "results_whisperx_speaker_filter_1300hz"
results_speakers_file = "results_whisperx_speaker_filter_1500hz"
results_speakers_file = "results_whisperx_speaker_filter_noise1"
results_speakers_file = "results_whisperx_speaker_filter_noise2"
results_speakers_file = "results_whisperx_speaker_filter_noise3"
results_speakers_file = "results_whisperx_speaker_filter_noise4"
results_speakers_file = "results_whisperx_speaker_filter_specific2"
dumpTimestamps = True


# Load Diarization from DetectAudio.py
with open(results_speakers_file+".txt") as f:
    transcription = json.load(f)

# print(transcription["segments"])

# # Dump .txt into .json
# out_file = open(results_speakers_file+".json", "w")
# json.dump(transcription, out_file, indent = 6, sort_keys=True)
# out_file.close()

# Generate transcription based on segments and speakers
outputTranscription = ""
oldSpeaker = ""
for segment in transcription["segments"]:
    if "speaker" in segment:
        if segment["speaker"] != oldSpeaker:
            oldSpeaker = segment["speaker"]
            outputTranscription = outputTranscription + "\n" + oldSpeaker + ":\n"
            if dumpTimestamps == True:
                outputTranscription = outputTranscription + "["+str(segment["start"])+"] "
            outputTranscription = outputTranscription + segment["text"]
            outputTranscription = outputTranscription 
        else:
            if dumpTimestamps == True:
                outputTranscription = outputTranscription + "["+str(segment["start"])+"] "
            outputTranscription = outputTranscription + segment["text"] + " "
    else:
        oldSpeaker = "Not recognized"
        outputTranscription = outputTranscription + "\n" + oldSpeaker + ":\n"
        if dumpTimestamps == True:
            outputTranscription = outputTranscription + "["+str(segment["start"])+"] "
        outputTranscription = outputTranscription + segment["text"]
        outputTranscription = outputTranscription 


text_file = open("transcription_"+results_speakers_file+".txt", "w")
text_file.write(outputTranscription)
text_file.close()

