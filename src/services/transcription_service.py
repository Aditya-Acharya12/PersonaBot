"""
Handles audio transcription logic (e.g., Whisper)
"""

async def transcribe_audio(file_path: str) -> dict:
    """
    Transcribes an audio file and returns transcript + metadata.
    """
    # TODO: integrate Whisper here later
    return {
        "transcript": "sample transcription",
        "language": "en",
        "duration": 12.3
    }
