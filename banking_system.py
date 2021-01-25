import random
import sqlite3

class CardClass:

    def __init__(self, num, pin):
        self.num = num
        self.pin = pin
        self.balance = 0
        


def print_menu():
    print("\n1. Create an account")
    print("2. Log into account")
    print("0. Exit\n")
    a = 3
    try:
        a = int(input())
    except TypeError:
        print("Incorrect type!")
    if a < 0 and a > 2:
        print("Choose correct number!")
        a = 3
    return a

def luhn(num):
    lst = []
    i = 0
    check = 0
    s = 0
    for digit in num:
        lst.append(int(digit))
    for l in lst:
        if i == 0 or i % 2 == 0:
            lst[i] *= 2
            if lst[i] > 9:
                lst[i] -= 9
        i += 1
    s = sum(lst)
    if s % 10 == 0:
        return '0'
    else:
        check = ((s // 10 + 1) * 10) - s
        return str(check)



def creator(con, cur, i):
    print("Your card has been created")
    num = str(random.randrange(400000000000000, 400000099999999))
    num = num + luhn(num)
    pin = str(random.randint(1000, 9999))
    card = CardClass(num, pin)
    data = i, num, pin
    cur.execute('INSERT INTO card(id, number, pin) VALUES(?, ?, ?)', data)
    con.commit()
    print("Your card number:")
    print(card.num)
    print("Your card PIN:")
    print(card.pin)

def second_page():
    print("\n1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit\n")
    a = 6
    try:
        a = int(input())
    except TypeError:
        print("Incorrect type!")
    if a < 0 and a > 5:
        print("Choose correct number!")
        a = 6
    return a

def transfer(cur, result):
    to_card = 0
    money = 0
    print("Transfer \nEnter card number: ")
    number = input()
    if number == result[1]:
        print("You can't transfer money to the same account!")
    elif luhn(number[:15]) != number[15]:
        print("Probably you made a mistake in the card number. Please try again!")
    else:
        cur.execute("SELECT * FROM card WHERE number=?", (number,))
        to_card = cur.fetchall()
        if to_card == None:
            print("Such a card does not exist.")
        else:
            to_card = list(to_card[0])
            print("Enter how much money you want to transfer: ")
            money = int(input())
            if money > result[3]:
                print("Not enough money!")
            else:
                cur.execute("UPDATE card SET balance=? WHERE number=?", (result[3] - money, result[1]))
                cur.execute("UPDATE card SET balance=? WHERE number=?", (to_card[3] + money, to_card[1]))
                print("Success!")



        


def login():
    inc = 0
    print("Enter your card number:")
    number = input()
    print("Enter your PIN:")
    pin = input()
    cur.execute('SELECT * FROM card WHERE number =?', (number,))
    result = cur.fetchall()
    if result == None:
        print("\nWrong card number or PIN!\n")
    else:
        cur.execute('SELECT * FROM card WHERE number =?', (number,))
        result = cur.fetchall()
        result = list(result[0])
        if result[2] != pin:
            print("\nWrong card number or PIN!\n")
        else:
            print("\nYou have successfully logged in!\n")
            while True:
                cur.execute('SELECT * FROM card WHERE number =?', (number,))
                result = cur.fetchall()
                result = list(result[0])
                r = second_page()
                if r == 0:
                    return 0
                elif r == 1:
                    print("Balance: " + str(result[3]))
                elif r == 2:
                    print("Enter income: ")
                    inc = int(input())
                    cur.execute("UPDATE card SET balance=? WHERE number=?", (inc, result[1],))
                    
                    print("Income was added!")
                elif r == 3:
                    transfer(cur, result)
                elif r == 5:
                    print("\nYou have successfully logged out!\n")
                    return 3


con = sqlite3.connect('card.s3db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS card (
                id      INTEGER,
                number  TEXT,
                pin     TEXT,
                balance INTEGER DEFAULT 0
                )
            ;''')
random.seed()
res = 3
i = 1
while True:
    res = print_menu()
    if res == 0:
        print("\nBye!")
        break
    elif res == 1:
        creator(con, cur, i)
        i += 1
    elif res == 2:
        res = login()
        if res == 0:
            print("Bye!")
            con.close()
            break
