import socket, sys
import time

HOST, PORT = 'localhost', 3000

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

try:
    listen_socket.bind((HOST, PORT))
except socket.error as msg:
    print("Bind failed. Error Code: %s / 'Message' %s" % msg[0], msg[1])
    sys.exit()
print("Socket bind complete")
try:
    while True:
        listen_socket.listen(10)
        print("Socket now listening")

        client_connection, client_address = listen_socket.accept()
        print("Connected with:" + str(client_address[0]) + ":" + str(client_address[1]))
        data = bytes.decode(client_connection.recv(1024))
        print(data)
        data = data.split()
        if len(data) > 0:
            if data[0] == "GET":
                try:
                    file = open(data[1][1:], "r")
                    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                    client_connection.send(bytes("HTTP/1.1 200 OK\nContent-Type: text/html\nDate: " + current_date + "\nServer: Simple-Python-HTTP-Server\nConnection: Close\n\n" + file.read(), 'utf-8'))
                    client_connection.close()
                except:
                    file = open("index404.html", "r")
                    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                    client_connection.send(bytes("HTTP/1.1 404 OK\nContent-Type: text/html\nDate: " + current_date + "\nServer: Simple-Python-HTTP-Server\nConnection: Keep-Alive\n\n" + file.read(), 'utf-8'))
                    client_connection.close()

except KeyboardInterrupt:
    print("Exiting...")

client_connection.close()
listen_socket.close()
