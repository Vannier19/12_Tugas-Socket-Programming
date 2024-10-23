import socket
import threading
import random
import tkinter as tk
from tkinter import messagebox

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("0.0.0.0", random.randint(8000, 9000)))

# Password check
password = "JARKOM YES"
max_attempts = 3
attempts = 0

def login():
    global attempts
    user_password = password_entry.get()
    name = username_entry.get()

    if user_password != password:
        attempts += 1
        messagebox.showerror("Error", f"Password salah. Percobaanmu tinggal {max_attempts - attempts} kali")
        if attempts == max_attempts:
            messagebox.showerror("Error", "Kesempatanmu habis. Program tertutup...")
            root.quit()
        return  # Berikan kesempatan untuk mencoba lagi.
    else:
        if name:  # Pastikan nama tidak kosong
            client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.106.32", 135))
            # Tunggu respons dari server apakah nama diterima atau sudah dipakai
            try:
                message, _ = client.recvfrom(1024)
                response = message.decode()
                if response == "Nama sudah dipakai, gunakan yang lain!":
                    messagebox.showerror("Error", "Nama sudah dipakai, gunakan yang lain!")
                    return  # Kembali ke login, beri kesempatan untuk retry
                else:
                    root.withdraw()  # Sembunyikan jendela login
                    start_chat(name)
            except:
                messagebox.showerror("Error", "Tidak bisa terhubung ke server!")
        else:
            messagebox.showerror("Error", "Nama tidak boleh kosong!")
        return

def start_chat(name):
    chat_window = tk.Tk()
    chat_window.title("Chat Room")
    chat_window.geometry("400x500")

    text_area = tk.Text(chat_window)
    text_area.pack()

    def receive():
        while True:
            try:
                message, _ = client.recvfrom(1024)
                text_area.insert(tk.END, message.decode() + "\n")
            except:
                pass

    threading.Thread(target=receive, daemon=True).start()

    def send_message():
        message = message_entry.get()
        if message:
            client.sendto(f"{name}: {message}".encode(), ("192.168.106.32", 135))
            message_entry.delete(0, tk.END)

    message_entry = tk.Entry(chat_window)
    message_entry.pack()

    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack()

    def logout():
        client.sendto(f"LOGOUT_TAG:{name}".encode(), ("192.168.106.32", 135))
        chat_window.destroy()
        root.deiconify()  # Tampilkan jendela login setelah logout.

    logout_button = tk.Button(chat_window, text="Logout", command=logout)
    logout_button.pack()

    chat_window.mainloop()

# Tkinter GUI untuk Login
root = tk.Tk()
root.title("Welcome To -_-")
root.geometry("300x200")

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
