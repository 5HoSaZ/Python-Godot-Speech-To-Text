class Client:
    """
    Represents a websocket client connected to the text-to-sign server.

    This class maintains the state for each connected client, including their
    unique identifier, audio buffer, configuration, and a counter for processed
    audio files.

    Attributes:
        client_id (str): A unique identifier for the client.
        buffer (bytearray): A buffer to store incoming audio data.
        config (dict): Configuration settings for the client, like chunk length
                       and offset.
        total_samples (int): Total number of audio samples received from this
                             client.
        sampling_rate (int): The sampling rate of the audio data in Hz.
    """

    def __init__(self) -> None:
        self.buffer = bytearray()
