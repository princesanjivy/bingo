from prettytable import PrettyTable
import requests
import json
import random
import os, time

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


URL = "http://localhost:8000/"

print("\tWelcome to Bingo")

d=[]
a=[]

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

name = input("Enter you name: ")
requests.post(URL+"addPlayer", data=json.dumps({"name":name}))
mode = input("Do you want to enter 25 numbers (1 - 50) or generate random (m/r): ")
if mode == "r": # random mode
    random_matrix = generate_random_matrix(5, 5)
    a = random_matrix
elif mode == "m":
    for i in range(5):
        b = []
        for j in range(5):
            c = int(input("Enter a number between 1 and 50: "))
            while (not (1 <= int(c) <= 50)) or (c in d):
                if c in d:
                    print("Entered value already exists.")
                elif not (1 <= int(c) <= 50):
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
    pass
    print("1. Start\n2. Show Players\n3. Ready\n4. Exit")
    op = int(input("Enter your option: "))
    if op == 2:
        resp = requests.get(URL+"players")
        p = json.loads(resp.text)
        print(p)
    if op == 1:
        resp = requests.get(URL+"start")
        p = json.loads(resp.text)
        if p.get("message") == "start":
            game = False
        else:
            print("Cannot start")
            print(p.get("message"))
    if op == 4:
        exit()
    if op == 3:
        resp = requests.post(URL+"ready", data=json.dumps({"name":name}))
        print(resp.text)



def display_bingo():
    table=PrettyTable()
    table.field_names=["B","I","N","G","O"]
    for i in range(5):
        table.add_row(a[i],divider=True)
    print(table)

def get_index(num):
    for i in range(5):
        for j in range(5):
            if a[i][j] == num:
                return i, j
    return -1, -1

def check_cross():
    d = []
    d.append(a[0]) # row  1
    d.append(a[1]) # row 2
    d.append(a[2]) # row 3
    d.append(a[3]) # row 4
    d.append(a[4]) # row 5

    t = []
    for i in range(5):
        for j in range(5):
            if j == 0:
                t.append(a[i][j])
    d.append(t) # col 1

    t = []
    for i in range(5):
        for j in range(5):
            if j == 1:
                t.append(a[i][j])
    d.append(t) # col 2

    t = []
    for i in range(5):
        for j in range(5):
            if j == 2:
                t.append(a[i][j])
    d.append(t) # col 3

    t = []
    for i in range(5):
        for j in range(5):
            if j == 3:
                t.append(a[i][j])
    d.append(t) # col 4

    t = []
    for i in range(5):
        for j in range(5):
            if j == 4:
                t.append(a[i][j])
    d.append(t) # col 5

    t = []
    for i in range(5):
        for j in range(5):
            if i == j:
                t.append(a[i][j])
    d.append(t) # diag 1

    t = []
    for i in range(5):
        for j in range(5):
            if i + j == 5-1:
                t.append(a[i][j])
    d.append(t) # diag 2

    crossed = [0]*len(d)

    # for index in range(len(d)):
    #     t = 0
    #     for num in d[index]:
    #         if num.endswith("X"):
    #             t += 1
    #     if t == 5:
    #         crossed[index] = 1

    # print(crossed)
    # print(crossed.count(1))
    if crossed.count(1) == 5:
        return "Over"
    return "InProgress"

def get_num_from_server():
    resp = requests.get(URL+"num")
    num_data = json.loads(resp.text)
    print(num_data)
    m = num_data.get("message")
    if "num" in m:
        return "r", m.get("num")
    
    return "n", m

# def strike(text):
#     result = ""
#     for c in text:
#         result = result + c + "\u0336"
#     return result

# print("Player made ready")
# ready_resp = requests.post(URL+"ready", json={"name": name})
# print(ready_resp.text)

while True:
    display_bingo()

    ready_resp = requests.post(URL+"ready", json={"name": name})
    print(ready_resp.text)

    while True:
        resp = requests.get(URL + "numbers")
        print(resp.text)
        message = json.loads(resp.text).get("message")
        if isinstance(message, dict) and "numbers" in message:
            numberss = message.get("numbers")
            break
        else:
            print("Not all players are ready.")
            time.sleep(1)


    print(numberss)
    print()

    num =int(input("Enter a number to cross: "))
    if num !=  numberss:
        print("Number not matched")
        time.sleep(1)
        resp_new = requests.post(URL+"crossed", data=json.dumps({"name":name}))
        print("Not Crossed but moving next")
        print(resp_new.text)
        # os.system("clear")
    else:
        i, j = get_index(num)
        if i == -1 or j == -1:
            print("Number not found!")
            time.sleep(1)
            resp_new = requests.post(URL+"crossed", data=json.dumps({"name":name}))
            print("Not Crossed but moving next")
            print(resp_new.text)
        else:
            # a[i][j] = strike(str(a[i][j]))
            a[i][j] = f"{Fore.GREEN}{a[i][j]}{Style.RESET_ALL}"
            resp_new = requests.post(URL+"crossed", data=json.dumps({"name":name}))
            print(resp_new.text)


        display_bingo()


        resp_new = requests.post(URL+"crossed", data=json.dumps({"name":name}))
        print("Not Crossed but moving next")
        print(resp_new.text)

        # get next number
        # loop until all players made a turn
        # show msg saying all player not made a turn

        # resp_new = requests.post(URL+"next", data=json.dumps({"name":name}))
        # print(resp_new.text)


        # acknowledging server my turn is complete
        # resp = requests.post(URL+"name",data=json.dumps({"name":name}))
        # print(resp.text)

        v= check_cross()
        if v == "Over":
            print("GAME OVER!!!")
            break
        print()
        print("="*100)
        print()
        # os.system("clear")
        
        while True:
            next_resp = requests.post(URL+"next")
            next_message = json.loads(next_resp.text).get("message")
            print(next_message)

            if next_message == "continue":
                break
            else:
                print(next_message)
                time.sleep(1)



        