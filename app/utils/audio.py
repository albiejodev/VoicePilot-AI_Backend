import base64


def decode_base64_audio(audio_data: str) -> bytes:
    """
    Convert a Base64 audio string from the browser
    into raw bytes.
    """

    # Remove:
    # data:audio/webm;codecs=opus;base64,

    _, encoded_audio = audio_data.split(",", 1)

    return base64.b64decode(encoded_audio)