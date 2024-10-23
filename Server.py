import socket
import threading
import queue



massages=queue.Queue()
clients=[]
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("192.168.34.32",135))

def receive():
    while True:
        try:
            massage, addr =server.recvfrom(1024)
            massages.put((massage,addr))
        except:
            pass


def broadcast():
    while True:
        while not massages.empty():
            massage,addr = massages.get()
            print(massage.decode())
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if massage.decode().startswith("SIGNUP_TAG:"):
                        name= massage.decode()[massage.decode().index(":")+1:]
                        server.sendto(f"{name} joined!". encode(), client)
                    else: 
                        server.sendto(massage,client)
                except:
                    clients.remove(client)

t1= threading.Thread(target=receive)
t2= threading.Thread(target=broadcast)

t1.start()
t2.start()