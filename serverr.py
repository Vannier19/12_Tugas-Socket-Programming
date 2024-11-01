import socket
import threading
import queue
import tkinter as tk
from tkinter import messagebox

# Tkinter setup for IP and port input
def start_server():
    ip = ip_entry.get()
    try:
        port = int(port_entry.get())
        server.bind((ip, port))
        messagebox.showinfo("Info", f"Server started at {ip}:{port}")
        t1.start()
        t2.start()
        root.destroy()  # Close the Tkinter window after starting the server
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid port number.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

messages = queue.Queue()
clients = {}
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Receive and broadcast functions as before
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

# Threads to handle receiving and broadcasting
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

# Tkinter interface for IP and Port input
root = tk.Tk()
root.title("Server Configuration")
root.geometry("300x150")

tk.Label(root, text="IP Address:").pack()
ip_entry = tk.Entry(root)
ip_entry.insert(0, "192.168.106.32")  # Default IP
ip_entry.pack()

tk.Label(root, text="Port:").pack()
port_entry = tk.Entry(root)
port_entry.insert(0, "135")  # Default Port
port_entry.pack()

start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.pack()

root.mainloop()
