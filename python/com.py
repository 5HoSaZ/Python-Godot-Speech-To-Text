import asyncio
import os
from asr import ASR_VOSK, ASR_WAV2VEC
from audio import MicAudio


model_path = os.path.abspath("./python/models/vosk-model-en-us-0.22")
asr = ASR_VOSK(model_path, sample_rate=44100)
# asr = ASR_WAV2VEC(sample_rate=44100)


async def main():
    audio = MicAudio()
    audio_queue = audio.get_queue()

    async def audio_receiver():
        await audio.receive()

    async def audio_process():
        await asr.transcribe(audio_queue)

    await asyncio.gather(audio_receiver(), audio_process())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Terminating...")
