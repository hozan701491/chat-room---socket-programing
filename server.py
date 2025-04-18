from socket_customing import Client
import socket
import select
import re 

def parse_tagged_users(message):
    match = re.findall(b"(@\\S+)", message)
    return match

def validate_username(username): 
    global clients
    return True if username not in clients and " " not in username else False



def get_username(client):
    handle_sender(client)
    data = client.recv_buff.get().decode()
    username = " ".join(data.split()[1:])
    is_username_valid = validate_username(username)
    if not is_username_valid:
        data = "1" 
        client.send_buff.put(data.encode())
        print(f'{client} chose a bad name')
    else:
        print(f"{client} is called {username!r}")
        client.username = username
        data = "0"
        client.send_buff.put(data.encode())


def notify_clients(user, clients, status):
    for client in clients:
        data = user.username.encode() + b" " + b"s" + b" " + f"{status}".encode()
        client.send_buff.put(data)


def send_online_users(new_user, online_users):
    for online_user in online_users:
        data = online_user.username.encode() + b" " + b"s" + b" " + b"1"
        new_user.send_buff.put(data)


def handle_new_connection(server, clients):
    client, _ = server.accept()
    print(f"{_} connected")
    client.setblocking(False)
    get_username(client)
    notify_clients(client, clients, 1)
    send_online_users(client, clients)
    clients.add(client)


def broadcast_message(sender, receivers):
    message = sender.recv_buff.get()
    tagged_users = parse_tagged_users(message)
    if tagged_users:
        print(f"{sender!r} tagged {tagged_users}")

    for receiver in receivers:
        if (
            not tagged_users
            or b"@" + receiver.username.encode() in tagged_users
            or receiver == sender
        ):
            data = sender.username.encode() + b" " + message
            receiver.send_buff.put(data)


def handle_receiver(receiver):
    while not receiver.send_buff.empty():
        try:
            data = receiver.send_buff.get()
            data_header = f"{len(data):<2048}".encode()
            receiver.sendall(data_header + data)
            print(f"{data} sent to {receiver}")
        except Exception as e:
            print("sending failed")
            print(e)


def handle_sender(sender):
    total_data  = b""
    status_code = 0
    try:
        while True:
            data_header = sender.recv(2048)
            if data_header:
                data = sender.recv(int(data_header))
                total_data += data
                if total_data:
                    status_code = 0
                    break 
                else:
                    status_code = 1
                    break
            else:
                if total_data:
                    status_code = 0
                    break
                else:
                    status_code = 1
                    break
    except ConnectionResetError:
        status_code = 1

    except Exception as e:
        print("recv failed")
        status_code = -1

    finally:
        sender.recv_buff.put(b"m " + total_data)
        print(f"{total_data} received from {sender}")
        return status_code


IP = "localhost"
PORT = 1234

clients = set()
senders = set()

server = Client(socket.AF_INET, socket.SOCK_STREAM)

server.setblocking(False)
server.bind((IP, PORT))
server.listen()

while True:
    print("Clients:", *clients, sep="\n")

    senders, _, broken_clients = select.select(clients | {server}, [], clients)

    for waiting_socket in senders:
        if waiting_socket == server:
            handle_new_connection(server, clients)
        else:
            success_receive = handle_sender(waiting_socket)
            if success_receive == 0:
                broadcast_message(waiting_socket, clients)
            elif success_receive == 1:
                broken_clients.append(waiting_socket)


    for broken_socket in broken_clients:
        clients.remove(broken_socket)
        notify_clients(broken_socket, clients, 0)
        broken_socket.close()

    for receiver in clients:
        if not receiver.send_buff.empty():
            handle_receiver(receiver)


