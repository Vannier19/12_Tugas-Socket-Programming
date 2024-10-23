import socket
import threading
import queue

massages = queue.Queue()
clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("192.168.34.32", 135))
#supaya nanti gausah ganti-ganti IP address, bisa pakai
#IP=socket.gethostbyname(socket.gethostname())
#Menambah fitur uutk ngasih tau brp yang aktif line 37

# Function to receive messages
def receive():
    while True:
        try:
            massage, addr = server.recvfrom(1024)
            massages.put((massage, addr))
        except:
            pass

# Function to broadcast messages
def broadcast():
    while True:
        while not massages.empty():
            massage, addr = massages.get()
            print(massage.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    # Handle SIGNUP_TAG for new users
                    if massage.decode().startswith("SIGNUP_TAG:"):
                        name = massage.decode().split(":")[1]
                        # Notify all clients that a new user has joined
                        server.sendto(f"{name} joined the chat!".encode(), client)
                        print(f"[Pengguna yang sedang Aktif ] {threading.activeCount()-1}")
                    else:
                        # Broadcast normal messages
                        server.sendto(massage, client)
                except:
                    clients.remove(client)

# Start receiving and broadcasting threads
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
