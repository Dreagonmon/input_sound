# input sound

Play sounds when typing with keyboard.

# requirement

You need sudo, to capture input from the linux kernel.

You need tk (python-tk) package in order to input sudo password.

You also need to install the packages in the `requirements.txt`

**Do not** directly run as `root`, in most of case it will lack of audio output device.

# run

```bash
# install package: python3 python-is-python3 python3-venv python-tk
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python .
# and input your sudo password.
```

# wav format

```bash
ffmpeg -i "<input_file>" -c:a pcm_u8 -ar 22050 -ac 2 "<output_file.wav>"

# e.g.
# ffmpeg -i "esc.mp3" -c:a pcm_u8 -ar 22050 -ac 2 "esc.wav" -y
```
