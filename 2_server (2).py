import socket
import threading
import queue

# Configuration for the server
SERVER_IP = input("Enter server IP: ") or '127.0.0.1'
SERVER_PORT = int(input("Enter server port: ") or 9090)

# Set up the UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))

messages = queue.Queue()
clients = {}

def handle_client(message, client_address):
    """Process client messages and handle ACKs, broadcasting to other clients."""
    global clients
    
    decoded_message = message.decode()

    if decoded_message.startswith("SIGNUP_TAG:"):
        name = decoded_message.split(":")[1]
        if name in clients.values():
            server_socket.sendto("Username already taken, please use another.".encode(), client_address)
        else:
            clients[client_address] = name
            print(f"{name} joined from {client_address}")
            for client in clients:
                server_socket.sendto(f"{name} joined the chat.".encode(), client)
        return

    elif decoded_message.startswith("LOGOUT_TAG:"):
        name = decoded_message.split(":")[1]
        if client_address in clients:
            del clients[client_address]
            print(f"{name} left from {client_address}")
            for client in clients:
                server_socket.sendto(f"{name} has left.".encode(), client)
        return

    # Handle regular message with sequence number
    if "|" in decoded_message:
        seq_number, client_msg = decoded_message.split("|", 1)
        seq_number = int(seq_number)
        
        # Send ACK for the received message to the sender
        ack_message = f"ACK|{seq_number}"
        server_socket.sendto(ack_message.encode(), client_address)

        # Broadcast the message to all other clients
        for client in clients:
            if client != client_address:
                server_socket.sendto(client_msg.encode(), client)

def receive():
    """Receive messages from clients and add them to the queue."""
    print("Server is running...")
    while True:
        message, client_address = server_socket.recvfrom(1024)
        messages.put((message, client_address))
        handle_client(message, client_address)

# Start the server thread
threading.Thread(target=receive, daemon=True).start()

# Keep the server running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nServer shutting down.")