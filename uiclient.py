import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST ="192.168.137.88"
PORT = 9999

class Client:

    def __init__(self, host, port):
        self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg=tkinter.Tk()
        msg.withdraw()

        self.nickname=simpledialog.askstring("Nickname"," Pilih nickname kamu", parent= msg)

        self.gui_done = False
        self.running = True

        gui_thread= threading.Thread(target=self.gui_loop)
        receive_thread= threading.Thread(target=self.receive_loop)

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="blue")

        self.chat_label =tkinter.Label(self.win, text="Chat: ", bg="lightgray")
        self.chat_label.config(font=("Times", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area= tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Massage: ", bg= "lightgray")
        self.msg_label.config(font=("Times", 12))
        self.msg_label.pack(padx=22, pady=7)

        self.input_area = tkinter.Text(self.win, height=4)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Times",12))
        self.send_button.pack(padx=20,pady=5)

        self.gui_done=True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        massage= f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.scok.send(massage.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running= False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                massage=self.sock.recv(1024)
                if massage == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else: 
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',massage)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("ada eror")
                self.sock.close()
                break

client= Client(HOST, PORT)
