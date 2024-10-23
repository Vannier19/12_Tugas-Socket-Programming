import socket

def scan(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # Mengatur timeout koneksi ke 1 detik

    try:
        con = s.connect((host, port))
        print("Port", port, "Terbuka")
        con.close()
    except:
        print("Port", port, "Tertutup")

host = input("Masukan domain atau IP address: ")
target = range(1, 1000)  # Scan port dari 1 sampai 999

for port in target:
    scan(host, port)
