import socket, sys
import time
import http.server

HOST, PORT = '10.0.0.21', 3000

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

try:
    listen_socket.bind((HOST, PORT))
except socket.error as msg:
    print("Bind failed. Error Code: %s / 'Message' %s" % msg[0], msg[1])
    listen_socket.close()
    listen_socket.bind((HOST, PORT))
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
                    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                    if data[1].split('.')[1] == "html":
                        this = open(data[1][1:], "r")
                        client_connection.send(bytes("HTTP/1.1 200 OK\nContent-Type: text/html\nDate: " + current_date + "\nServer: Simple-Python-HTTP-Server\nConnection: Close\n\n" + this.read(), 'utf-8'))
                    elif data[1].split('.')[1] == "png":
                        this = open(data[1][1:], "rb")
                        client_connection.send(bytes("HTTP/1.1 200 OK\nContent-Type: image/png\nDate: " + current_date + "\nServer: Simple-Python-HTTP-Server\nConnection: Close\n\n", 'utf-8').join(this.read()))
                        
                    client_connection.close()
                except Exception as e:
                    print(e)
                    this = open("index404.html", "r")
                    current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                    client_connection.send(bytes("HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\nDate: " + current_date + "\nServer: Simple-Python-HTTP-Server\nConnection: Keep-Alive\n\n" + this.read(), 'utf-8'))
                    client_connection.close()

except KeyboardInterrupt:
    print("Exiting...")
    client_connection.close()
    listen_socket.close()

client_connection.close()
listen_socket.close()
