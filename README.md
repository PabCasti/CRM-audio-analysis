# CRM-audio-analysis
1.code_detectAudio: Runs WhisperX model to generate speech recognition and speaker diarization results
2.code_showResults: Generate RTTM timeline based on speaker diarization results
3.code_generateTranscription: Uses results from speaker diarization and speech recognition to convert from JSON into transcription text
4.0.code_extractActions: Uses NTS Model and OPENAI prompts to extract structured outputs from transcriptions
4.1.JoinResults: Merge results from several iterations of structured outputs
5.code_neo4jKG: Convert structured data into nodes and edges and ingest into Neo4j sandbox
