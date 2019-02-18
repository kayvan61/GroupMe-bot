import socket
import json
import bot as botter

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


client_socket.bind(('0.0.0.0', 8082))

botter.init()

while 1:
    try:
        client_socket.listen(2)
        conn, addr = client_socket.accept()
        data = conn.recv(4096)
        data = data.decode('utf8')
        #print(data)
        jsonData = json.loads(data[data.index('{'):])
        #print(data)
        print(jsonData['text'])
        botter.checkReg(jsonData['text'], data)
    except KeyboardInterrupt:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        exit(1)
    except socket.error:
        pass
    except ValueError as ex:
        print(str(ex))
        pass
