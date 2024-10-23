import socket
import threading
import queue

messages = queue.Queue()
clients = {}
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("192.168.106.32", 135))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            decoded_message = message.decode()

            if decoded_message.startswith("SIGNUP_TAG:"):
                name = decoded_message.split(":")[1]
                if name in clients.values():
                    server.sendto("Nama sudah dipakai, gunakan yang lain!".encode(), addr)
                else:
                    clients[addr] = name
                    print(f"{name} joined from {addr}") 
                    for client in clients:
                        server.sendto(f"{name} joined the chat. [Pengguna yang sedang aktif: {len(clients)}]".encode(), client)
                continue

            elif decoded_message.startswith("LOGOUT_TAG:"):
                name = decoded_message.split(":")[1]
                if addr in clients:
                    del clients[addr]
                    print(f"{name} left from {addr}")

                    for client in clients:
                        server.sendto(f"{name} has left! [Pengguna yang sedang aktif: {len(clients)}]".encode(), client)
                continue


            print(f"Received from {clients.get(addr, 'Unknown')}: {decoded_message}")
            for client in clients:
                try:
                    server.sendto(message, client)
                except:
                    clients.pop(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
