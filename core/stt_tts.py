import subprocess

WHISPER_PATH = "../models/ggml-tiny.en.bin"

def listen():
    subprocess.run("arecord -d 5 -f S16_LE -r 16000 input.wav", shell=True)
    text = subprocess.check_output(
        f"../whisper.cpp/main -m {WHISPER_PATH} -f input.wav",
        shell=True
    ).decode().split("]")[-1].strip()
    return text

def speak(text):
    subprocess.run(
        f'echo "{text}" | piper --model en_US-lessac-medium.onnx | aplay',
        shell=True
    )
