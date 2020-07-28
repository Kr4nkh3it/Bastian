import threading
from fuzz import *
from queue import Queue

web_loc = input("Enter url and port\nex: https://url,port[")
print("1 == yes and 2 == no")
out = input("output or no output when bruteforcing[")

url,sock= Web_Addr(web_loc)

wordlist = input("Enter wordlist ex: wordlist.txt[")
ext = input("Choose file extension\nex: .php[")
if ext == " " or ext == "":
    ext = ".php"

data = Send_Req(url,sock,wordlist,out)

for num in range(10):
    print(" 1 == yes, 2 == no")
    Choice = input("Would you like to see info gathered[")
    if Choice == "1":
        print(data)
        break
    elif Choice == "2":
        print("Exiting")
        break
    else:
        print("Invalid Choices")

