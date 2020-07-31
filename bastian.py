import socket,time,threading
from queue import Queue
from fuzz import *

errors = 0
info = []
list_=Queue()
list2 = Queue()
print_lock = threading.Lock()

web_loc = input("Enter url and port\nex: https://url,port[")
thrds = input("Enter amount of threads\ndefault is 200[")
if thrds == "" or thrds == " ":
    thrds = 200
else:
    thrds = int(thrds)
print("1 == yes and 2 == no")
out = input("output or no output when bruteforcing[")

wordlist = input("Enter wordlist ex: wordlist.txt[")
ext = input("Choose file extension\nex: .php[")
if ext == " " or ext == "":
    ext = ".php"

url,port= Web_Addr(web_loc)

print(f"url[{url}]\tport[{port}]\nthreads[{thrds}]\toutputchoice[{out}]\nwordlist[{wordlist}]\tfile extension[{ext}]")
time.sleep(5)
            
dir_list = list(Gen_words(wordlist))

for word in dir_list:
    list_.put(word)

for word in dir_list:
    list2.put(word)

for thread in range(thrds):
    if errors <= 40:
        t = threading.Thread(target=threaded,args = [list_,url,port,out,ext,info,errors])
        t.daemon = True
        t.start()
        if len(good_dirs) >=1:
            t2 = threading.Thread(target=threaded2,args = [list2,url,port,out,ext,info,errors])
            t2.daemon = True
            t2.start()
    else:
        print("Too many errors occured\n1 == yes 2 == no")
        choice = input("Continue?[")
        if choice == "1":
            continue
        else:
            break

list_.join()
list2.join()  

while True:
    print(" 1 == yes, 2 == no")
    Choice = input("Would you like to see info gathered[")
    if Choice == "1":
        if info == None:
            print("No info was gathered")
        else:
            for data in info:
                print(data)
        break
    elif Choice == "2":
        print("Exiting")
        break
    else:
        print("Invalid Choices")
