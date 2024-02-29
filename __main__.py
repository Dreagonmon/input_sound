import os
import sys
import atexit
import simpleaudio
import shutil
import subprocess
import signal
import time

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
SOUNDS_DIR = os.path.join(APP_ROOT, "sounds")
LISTEN_KEY_SCRIPT = os.path.join(APP_ROOT, "_get_key_.py")
ASK_PASSWD_SCRIPT = os.path.join(APP_ROOT, "_ask_pwd_.py")
ASK_PASSWD_SCRIPT_EXEC = os.path.join(APP_ROOT, "_ask_pwd_.exec.py")

FAST_ALPHABET_MS = 300
ALPHABET_KEYS = [ k for k in "abcdefghijklmnopqrstuvwxyz"]
NUMBER_KEYS = [ k for k in "1234567890−-=_+/*()&^%$#@!`~[]{};:'\"\\|,.<>/?÷×" ]
SPACE_KEY = "space"
ENTER_KEY = "enter"
BACKSPACE_KEY = "backspace"
ESC_KEY = "esc"

WAV_ALP_FAST = simpleaudio.WaveObject.from_wave_file("sounds/alphabet_fast.wav")
WAV_ALP_SLOW = simpleaudio.WaveObject.from_wave_file("sounds/alphabet_slow.wav")
WAV_NUMBER = simpleaudio.WaveObject.from_wave_file("sounds/number.wav")
WAV_SPACE = simpleaudio.WaveObject.from_wave_file("sounds/space.wav")
WAV_ENTER = simpleaudio.WaveObject.from_wave_file("sounds/enter.wav")
WAV_BACKSPACE = simpleaudio.WaveObject.from_wave_file("sounds/backspace.wav")
WAV_ESC = simpleaudio.WaveObject.from_wave_file("sounds/esc.wav")

subproc = None
last_keydown_time = time.time_ns()

def init():
    atexit.register(deinit)

def process_key(name: str):
    global last_keydown_time
    if name == SPACE_KEY:
        WAV_SPACE.play()
    elif name == ENTER_KEY:
        WAV_ENTER.play()
    elif name == BACKSPACE_KEY:
        WAV_BACKSPACE.play()
    elif name == ESC_KEY:
        WAV_ESC.play()
    elif name in NUMBER_KEYS:
        WAV_NUMBER.play()
    elif name in ALPHABET_KEYS:
        now = time.time_ns()
        if (now - last_keydown_time) > (1000_000 * FAST_ALPHABET_MS):
            WAV_ALP_SLOW.play()
        else:
            WAV_ALP_FAST.play()
    else:
        print(name)
    last_keydown_time = time.time_ns()

def fetch_input():
    global subproc
    cmd_chmod = shutil.which("chmod")
    cmd_sudo = shutil.which("sudo")
    cmd_python = sys.executable
    # prepare ask password
    with open(ASK_PASSWD_SCRIPT, "rb") as inf:
        _ = inf.readline()
        remain_lines = inf.read()
        with open(ASK_PASSWD_SCRIPT_EXEC, "wb") as outf:
            outf.truncate(0)
            outf.write(b"#!")
            outf.write(cmd_python.encode("utf-8"))
            outf.write(b"\n")
            outf.write(remain_lines)
    subprocess.run([cmd_chmod, "+x", ASK_PASSWD_SCRIPT_EXEC])
    os.environ.setdefault("SUDO_ASKPASS", ASK_PASSWD_SCRIPT_EXEC)
    # run
    subproc = subprocess.Popen(
        [cmd_sudo, "-A", cmd_python, LISTEN_KEY_SCRIPT],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        env=os.environ,
    )
    # loop
    is_running = False
    out = subproc.stdout
    while True:
        line = out.readline()
        if len(line) > 0:
            text = line.decode("utf-8").strip()
            if text == "==========":
                is_running = True
                print("Listening to the keyboard...")
                continue
            if not is_running:
                print(text)
                continue
            # running
            process_key(text)

def deinit():
    global subproc
    if subproc != None:
        subproc.send_signal(signal.SIGINT)
        subproc.wait()

def main():
    init()
    try:
        fetch_input()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
 