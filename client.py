import socket
import threading
import sys 
from os import _exit 

IP = "127.0.0.1"
PORT = 1234
address = (IP, PORT)

def read_input():
    global client
    global stop_event
    while True:
        data = input()
        if not stop_event.is_set():
            data_header = f"{len(data.encode()):<2048}".encode()
            bytes_sent = 0
            while bytes_sent < len(data_header + data.encode()):
                bytes_sent += client.send((data_header + data.encode())[bytes_sent:])
                print("bytes sent:", bytes_sent)
        else:
            return 
    
def parse_data(raw_data: bytes):
    data = raw_data.decode()
    data.strip()
    parsed_data = data.split(" ")
    username = parsed_data[0]
    flag = parsed_data[1]
    message = ""
    if flag == 's':
        message = parsed_data[2]
    elif flag == 'm':
        message = " ".join(parsed_data[2:])
    else:
        print('error in parse data')
    
    return username, flag, message







def recv_():
    global client
    global stop_event
    while True:
        try:
            total_data = b""
            data_header = client.recv(2048)
            if data_header:
                data_len = int(data_header.decode())
                while True:
                    if len(total_data) < data_len:
                        data = client.recv(data_len)
                        total_data += data 
                    else:
                        break  
                username, flag, message = parse_data(total_data)
                if flag=='s':
                    print(f'{username!r} is {message}')
                elif flag=='m':
                    print(f'received: {message!r} from {username}')
            else:
                client.close()
                print('disconnected from server')
                stop_event.set()
                _exit(0)

        except Exception as e:
            print(e, file=sys.stderr)





stop_event = threading.Event()

recv_thread        = threading.Thread(target=recv_, name="receive thread")
read_input_thread  = threading.Thread(target=read_input, name="read input thread")

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = input("enter your name: ")
    username_header = f"{len(username):<2048}".encode()
    client.connect(address)

    client.sendall(username_header + username.encode())

    data_header = client.recv(2048)
    data = client.recv(int(data_header.decode())).decode()

    if data=="0": # username is ok
        print('welcome to server')
        break

    elif data=="1":
        print("username is already taken")
        client.close()

    else:
        print('unknown error')
        print(data)
        client.close()

read_input_thread.start()
recv_thread.start()

recv_thread.join()
read_input_thread.join()
sys.exit(0)