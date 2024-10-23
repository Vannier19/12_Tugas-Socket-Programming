import socket
import threading


HOST ="192.168.137.88"
PORT = 9999
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost",9999))

server.listen()


clients = []
nicknames= []

def broadcast (massage):
    for client in clients:
        client.send(massage)

def handle(client):
    while True: 
        try: 
            massage = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}")
            broadcast(massage)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Terhubung ke {str(address)}")


        client.send("NICK".encode('utf-8'))
        nickname=client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print("Namamu di chat ini adalah {nickname}")
        broadcast(f"{nickname} masuk ke chat\n".encode('utf-8'))
        client.send("Terhubung ke chat".encode('utf-8'))

        thread = threading.Thread(target= handle, args=(client, ))
        thread.start()

print("Grup chat telah dibuat")