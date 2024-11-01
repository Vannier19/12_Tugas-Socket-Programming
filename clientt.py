import socket
import threading
import random
import tkinter as tk
from tkinter import messagebox

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))  # Tidak diubah

# Password check and max attempts
password = "JARKOM YES"
max_attempts = 3
attempts = 0
server_ip = "192.168.106.32"  # Placeholder, akan diubah oleh input user
server_port = 135  # Port tetap
is_logged_in = False  # Flag to track login status

def login():
    global attempts, server_ip, server_port, is_logged_in
    user_password = password_entry.get()
    name = username_entry.get()
    ip = ip_entry.get()

    # Ambil port dari input pengguna
    try:
        server_port = int(port_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Masukkan nomor port yang valid.")
        return

    if user_password != password:
        attempts += 1
        messagebox.showerror("Error", f"Password salah. Percobaanmu tinggal {max_attempts - attempts} kali")
        if attempts == max_attempts:
            messagebox.showerror("Error", "Kesempatanmu habis. Program tertutup...")
            root.quit()
        return
    else:
        if name:
            server_ip = ip  # Set IP dari input pengguna
            client.sendto(f"SIGNUP_TAG:{name}".encode(), (server_ip, server_port))
            try:
                message, _ = client.recvfrom(1024)
                response = message.decode()
                if response == "Nama sudah dipakai, gunakan yang lain!":
                    messagebox.showerror("Error", "Nama sudah dipakai, gunakan yang lain!")
                    return
                else:
                    root.withdraw()
                    is_logged_in = True  # Set flag to True when logged in
                    start_chat(name)
            except socket.error:
                messagebox.showerror("Error", "Tidak bisa terhubung ke server di IP dan port tersebut!")
        else:
            messagebox.showerror("Error", "Nama tidak boleh kosong!")
        return

def start_chat(name):
    global is_logged_in

    chat_window = tk.Tk()
    chat_window.title("Chat Room")
    chat_window.geometry("400x500")

    text_area = tk.Text(chat_window)
    text_area.pack()

    def receive():
        while is_logged_in:  # Only run if user is logged in
            try:
                message, _ = client.recvfrom(1024)
                text_area.insert(tk.END, message.decode() + "\n")
            except:
                pass

    receive_thread = threading.Thread(target=receive, daemon=True)
    receive_thread.start()

    def send_message():
        message = message_entry.get()
        if message:
            client.sendto(f"{name}: {message}".encode(), (server_ip, server_port))
            message_entry.delete(0, tk.END)

    message_entry = tk.Entry(chat_window)
    message_entry.pack()

    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack()

    def logout():
        global is_logged_in
        is_logged_in = False  # Stop the receive loop
        client.sendto(f"LOGOUT_TAG:{name}".encode(), (server_ip, server_port))
        chat_window.destroy()
        root.deiconify()  # Show login window after logout

    logout_button = tk.Button(chat_window, text="Logout", command=logout)
    logout_button.pack()

    chat_window.protocol("WM_DELETE_WINDOW", logout)  # Handle window close event
    chat_window.mainloop()

# Tkinter GUI untuk Login
root = tk.Tk()
root.title("Welcome To -_-")
root.geometry("300x300")

tk.Label(root, text="Server IP Address").pack()
ip_entry = tk.Entry(root)
ip_entry.insert(0, "192.168.106.32")  # Default IP server
ip_entry.pack()

tk.Label(root, text="Server Port").pack()
port_entry = tk.Entry(root)
port_entry.insert(0, "135")  # Default Port
port_entry.pack()

password_label = tk.Label(root, text="Password")
password_label.pack()
password_entry = tk.Entry(root, show='*')
password_entry.pack()

username_label = tk.Label(root, text="Username")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

root.mainloop()
