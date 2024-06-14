from prettytable import PrettyTable
import requests
import json
import random
import os
import time

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

URL = "https://bingo-server-rjq4aqttlq-uc.a.run.app/"

print("\tWelcome to Bingo")

d = []
a = []

def generate_random_matrix(rows, cols):
    numbers = list(range(1, 26))
    random.shuffle(numbers)
    matrix = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(numbers.pop())
        matrix.append(row)
    return matrix

def request_get (msg):
    resp = requests.get(URL + msg)
    p = json.loads(resp.text)
    return p

def send_request(endpoint, data):
    response = requests.post(URL + endpoint, data=json.dumps(data))
    return response

name = input("Enter your name: ")
send_request("addPlayer", {"name": name})
mode = input("Do you want to enter 25 numbers (1 - 25) or generate random (m/r): ")
if mode == "r":
    random_matrix = generate_random_matrix(5, 5)
    a = random_matrix
elif mode == "m":
    for i in range(5):
        b = []
        for j in range(5):
            c = int(input("Enter a number between 1 and 25: "))
            while (not (1 <= c <= 25)) or (c in d):
                if c in d:
                    print("Entered value already exists.")
                elif not (1 <= c <= 25):
                    print("Entered value is not in the range 1 to 25.")
                c = int(input("Enter a number between 1 and 25: "))
            d.append(c)
            b.append(c)
        a.append(b)
else:
    print("Invalid mode; Exiting...")
    exit()

game = True
while game:
    print("\n1. Start\n2. Show Players\n3. Ready\n4. Exit")
    op = int(input("Enter your option: "))
    if op == 2:
        request_get("players")
    if op == 1:
        p = request_get("start")
        if p.get("message") == "start":
            game = False
        else:
            print("Cannot start")
            print(p.get("message"))
    if op == 4:
        exit()
    if op == 3:
        resp = send_request("ready", {"name": name})
        print(resp.text)

def display_bingo():
    print()
    table = PrettyTable()
    table.field_names = ["B", "I", "N", "G", "O"]
    for row in a:
        table.add_row(row, divider=True)
    print(table)

def get_index(num):
    for i in range(5):
        for j in range(5):
            if a[i][j] == num:
                return i, j
    return -1, -1

def check_cross():
    d = []
    for i in range(5):
        d.append(a[i])  # rows
        d.append([a[j][i] for j in range(5)])  # columns

    d.append([a[i][i] for i in range(5)])  # diagonal 1
    d.append([a[i][4 - i] for i in range(5)])  # diagonal 2

    crossed = [all(isinstance(x, str) for x in row) for row in d]

    if crossed.count(True) >= 5:
        return "Over"
    return "InProgress"

while True:
    display_bingo()

    while True:
        message = request_get("numbers").get("message")
        if isinstance(message, dict) and "numbers" in message:
            numberss = message.get("numbers")
            break
        else:
            print("===Not all players are ready.===")
            time.sleep(1)

    print("Your number to cross is:", f"{Fore.GREEN}{numberss}{Style.RESET_ALL}")
    print()

    try:
        num = int(input("Enter a number to cross: "))
    except:
        print("Enter The given valid number to cross",end="")
    if num != numberss:
        print("Number not matched!")
        print("Please retry after few seconds...")
        time.sleep(2)
        os.system("clear")
    else:
        i, j = get_index(num)
        if i == -1 or j == -1:
            print("Wait for other players to make their move...")
            print("Please retry after few seconds...") 
            time.sleep(2)
            os.system("clear") 
        else:
            a[i][j] = f"{Fore.GREEN}{a[i][j]}{Style.RESET_ALL}"
            os.system("clear")

        display_bingo()

        resp_new = send_request("crossed", {"name": name})
        print("\n===Made a move===")
        print(resp_new.text)

        if check_cross() == "Over":
            print("GAME OVER!!!")
            break
            
        # print("\n" + "="*100 + "\n")

        while True:
            input("Press Enter to check for the next number...")
            next_resp = send_request("next", {"name": name})
            status = json.loads(next_resp.text).get("message")
            if status:
                os.system("clear")
                break
            else:
                print("Waiting for other players to make their move...")
                ready_resp = send_request("ready", {"name": name})
                print(ready_resp.text) 
                time.sleep(2)
                os.system("clear")
                # time.sleep(1)
 



    
    