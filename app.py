from modules.voice_input import Recorder


if __name__ == '__main__':
    rec = Recorder()
    res = rec.record_audio()
    rec.terminate()
    print(res)
