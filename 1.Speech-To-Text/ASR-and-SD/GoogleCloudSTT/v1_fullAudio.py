
# >> python3 -m venv venv
# >> source venv/bin/activate
# >> pip install google-cloud-speech


from google.cloud import speech_v1p1beta1 as speech



client = speech.SpeechClient()

# Enhance diarization config with more speaker counts and details
speaker_diarization_config = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=4,  # Set minimum number of speakers
    max_speaker_count=6,  # Adjust max speakers based on expected number of speakers
)

# Configure recognition with enhanced audio settings
recognition_config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code="en-US",
    sample_rate_hertz=44100,
    diarization_config=speaker_diarization_config,
)

# Set the remote path for the audio file
audio = speech.RecognitionAudio(
    uri="gs://audio-detection-bucket/cardiacEscenarioMono.wav",
)

# Use non-blocking call for getting file transcription
response = client.long_running_recognize(
    config=recognition_config, audio=audio
).result(timeout=300)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result
result = response.results[-1]
words_info = result.alternatives[0].words

# Print the output
for word_info in words_info:
    print(f"speaker_tag_{word_info.speaker_tag}: '{word_info.word}'")

print(result)

