import socket
import threading
import random
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

# Set up the socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))

# Password
password = "JARKOM YES"

# Function to check password
def check_password():
    for attempt in range(3):
        user_password = simpledialog.askstring("Password", "Enter the password:")
        if user_password == password:
            return True
        else:
            remaining_attempts = 2 - attempt
            messagebox.showinfo("Password Error", f"Incorrect password. {remaining_attempts} attempts left.")
    messagebox.showerror("Access Denied", "No attempts left. Program will close.")
    root.destroy()
    return False

# Function to receive messages
def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            messages_area.config(state=tk.NORMAL)
            messages_area.insert(tk.END, message.decode() + '\n')
            messages_area.config(state=tk.DISABLED)
        except:
            break

# Function to send messages
def send_message(event=None):
    message = message_entry.get()
    if message:
        client.sendto(f"{name}: {message}".encode(), ("192.168.34.32", 135))
        message_entry.delete(0, tk.END)

# Set up the main window
root = tk.Tk()
root.title("Chat Client")

# Check password before proceeding
if not check_password():
    exit()

# Ask for nickname
name = simpledialog.askstring("Nickname", "Enter your nickname:")

# Notify server about new user
client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.34.32", 135))

# Create UI elements
messages_area = scrolledtext.ScrolledText(root, state=tk.DISABLED)
messages_area.pack(padx=10, pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(padx=10, pady=10)
message_entry.bind("<Return>", send_message)  # Send message on Enter

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Start the thread for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Run the Tkinter event loop
root.mainloop()
