import socket
import threading

# Client configuration
SERVER_IP = input("Enter server IP: ") or '127.0.0.1'
SERVER_PORT = int(input("Enter server port: ") or 9090)
RETRANSMISSION_TIMEOUT = 2  # seconds

# Set up UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(RETRANSMISSION_TIMEOUT)

# Login credentials
password = "JARKOM YES"
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    user_password = input("Enter password: ")
    if user_password == password:
        username = input("Enter your username: ")
        client_socket.sendto(f"SIGNUP_TAG:{username}".encode(), (SERVER_IP, SERVER_PORT))
        
        # Wait for server's response on username availability
        try:
            response, _ = client_socket.recvfrom(1024)
            if response.decode() == "Username already taken, please use another.":
                print("Username already taken, please choose another.")
            else:
                print("Connected to chat server!")
                break
        except socket.timeout:
            print("Could not connect to server: timeout")
            exit()
    else:
        attempts += 1
        print(f"Incorrect password. Attempts remaining: {max_attempts - attempts}")

if attempts == max_attempts:
    print("Maximum attempts reached. Exiting...")
    exit()

def receive_messages():
    """Receive messages from the server."""
    while True:
        try:
            data, _ = client_socket.recvfrom(1024)
            message = data.decode()
            
            # Check if the message is an ACK
            if message.startswith("ACK|"):
                ack_sequence = int(message.split("|")[1])
                if ack_sequence == sequence_number:
                    print("[Server] Message acknowledged.")
                    ack_received.set()
            else:
                print(message)  # Display broadcasted messages from other clients

        except socket.timeout:
            continue

def send_messages():
    """Send messages to the server, with retransmission on timeout."""
    global sequence_number
    sequence_number = 0
    while True:
        message_content = input("Your message: ")
        full_message = f"{sequence_number}|{username}: {message_content}"
        
        # Use an event to wait for ACK
        global ack_received
        ack_received = threading.Event()
        
        # Attempt retransmission until acknowledged
        while not ack_received.is_set():
            client_socket.sendto(full_message.encode(), (SERVER_IP, SERVER_PORT))
            if not ack_received.wait(RETRANSMISSION_TIMEOUT):
                print(f"[TIMEOUT] Resending message '{message_content}'...")
        sequence_number += 1

# Start receiving and sending threads
threading.Thread(target=receive_messages, daemon=True).start()
threading.Thread(target=send_messages, daemon=True).start()

# Keep client running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nLogging out...")
    client_socket.sendto(f"LOGOUT_TAG:{username}".encode(), (SERVER_IP, SERVER_PORT))
    client_socket.close()
    print("Disconnected.")