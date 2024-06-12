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

URL = "http://localhost:8000/"

print("\tWelcome to Bingo")

d = []
a = []

def generate_random_matrix(rows, cols):
    numbers = list(range(1, 51))
    random.shuffle(numbers)
    matrix = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(numbers.pop())
        matrix.append(row)
    return matrix

name = input("Enter your name: ")
requests.post(URL + "addPlayer", data=json.dumps({"name": name}))
mode = input("Do you want to enter 25 numbers (1 - 50) or generate random (m/r): ")
if mode == "r":
    random_matrix = generate_random_matrix(5, 5)
    a = random_matrix
elif mode == "m":
    for i in range(5):
        b = []
        for j in range(5):
            c = int(input("Enter a number between 1 and 50: "))
            while (not (1 <= c <= 50)) or (c in d):
                if c in d:
                    print("Entered value already exists.")
                elif not (1 <= c <= 50):
                    print("Entered value is not in the range 1 to 50.")
                c = int(input("Enter a number between 1 and 50: "))
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
        resp = requests.get(URL + "players")
        p = json.loads(resp.text)
        print(p)
    if op == 1:
        resp = requests.get(URL + "start")
        p = json.loads(resp.text)
        if p.get("message") == "start":
            game = False
        else:
            print("Cannot start")
            print(p.get("message"))
    if op == 4:
        exit()
    if op == 3:
        resp = requests.post(URL + "ready", data=json.dumps({"name": name}))
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
        resp = requests.get(URL + "numbers")
        message = json.loads(resp.text).get("message")
        if isinstance(message, dict) and "numbers" in message:
            numberss = message.get("numbers")
            break
        else:
            print("===Not all players are ready.===")
            time.sleep(1)

    print(numberss)
    print()

    num = int(input("Enter a number to cross: "))
    if num != numberss:
        print("Number not matched")
        time.sleep(1)
    else:
        i, j = get_index(num)
        if i == -1 or j == -1:
            print("Number not found!")
            time.sleep(1)
        else:
            a[i][j] = f"{Fore.GREEN}{a[i][j]}{Style.RESET_ALL}"

        display_bingo()

        resp_new = requests.post(URL + "crossed", data=json.dumps({"name": name}))
        print("\n===Made a move===")
        print(resp_new.text)

        if check_cross() == "Over":
            print("GAME OVER!!!")
            break
        print("\n" + "="*100 + "\n")
        os.system("clear")

        while True:
            input("Press Enter to check for the next number...")
            next_resp = requests.post(URL + "next", data=json.dumps({"name": name}))
            status = json.loads(next_resp.text).get("message")
            if status:
                break
            else:
                print("Waiting for other players to make their move...")
                ready_resp = requests.post(URL + "ready", json={"name": name})
                print(ready_resp.text)      
                # time.sleep(1)
