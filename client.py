import socket
import threading
import random

client= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000,9000)))

name= input ("nickname: ")

def receive():
    while True:
        try:
            massage, _ = client.recvfrom(1024)
            print(massage.decode())
        except:
            pass


t= threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.34.32", 135))

while True:
    massage = input("")
    if massage == "!q":
        exit()
    else:
        client.sendto(f"{name}: {massage}".encode(), ("192.168.34.32", 135))

