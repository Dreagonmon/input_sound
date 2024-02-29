import keyboard
import sys

REPEAT = False
pressed_keys = set()

def on_key_event(evt: keyboard.KeyboardEvent):
    if evt.event_type == keyboard.KEY_DOWN:
        if (evt.scan_code not in pressed_keys) or REPEAT:
            sys.stdout.write(evt.name)
            sys.stdout.write("\n")
            sys.stdout.flush()
            pressed_keys.add(evt.scan_code)
    elif evt.event_type == keyboard.KEY_UP:
        pressed_keys.discard(evt.scan_code)

def main():
    sys.stdout.write("==========\n")
    sys.stdout.flush()
    keyboard.hook(on_key_event, suppress=False)
    keyboard.wait()

if __name__ == "__main__":
    main()
