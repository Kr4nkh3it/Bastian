# Bastian
#basic url fuzzer 
#Made by untoterarzt on insta
#Most of the code should be basic and easy to read but if not the read me is here

import socket,threading
from queue import Queue

#Gets the website addr and port 
web_loc = input("Enter url and port\nex: https://url:port[")
#Check for verbose or not
print("1 == yes and 2 == no")
out = input("output or no output when bruteforcing[")

#modifies the web addr so it will seperate the port and the url then it fixes the url 
def Web_Addr(location):
    web_addr_port = list(location.split(":"))
    addr = ""
    try:
        addr+= web_addr_port[0] + ":"
        addr+= web_addr_port[1]
    except:
        addr+=web_addr_port[0]
    try:
        port = int(web_addr_port[2])
    except:
        port = 80
    return addr,port

url, port = Web_Addr(web_loc)
#Sets up a socket to connect to the site
sock =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
#replaces the protocol declaration so that it will get the addr properly
    sock.connect((url.replace("https://" or "http://",""),port))
except:
    sock.connect((url,port))
#Gets a file to read    
wordlist = input("Enter wordlist ex: wordlist.txt[")
#Removes certain symbols and text from the text gotten from the http request
def Remove(text):
    text_list = list(text.split("GET"))
    try:
        txt = text_list[1]
    except:
        txt = text_list[0]
    txt = txt.replace("\n" and "\r","")
#Sends the request by opening up a file and sending a request to the url using each line as a could be directory
def Send_Req(addr,file):
    errors = 0
    good_dirs = []
    info = []
    with open(file,'r') as f:
        for line in f:
            try:
                addr.send(f"GET /{line} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
                if out == "1":
                    print(f"trying {line} as directory")
                data = addr.recv(1000)
                data = data.decode("utf-8")
                if "404" in data:
                    errors+=1
                else:
                    good_dirs.append(line)
                    info.append(Remove(data))
                    if out == "1":
                        print(data)
            except:
                print("There must of been a connection error")
                addr.close()
                addr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                addr.connect((url.replace("https://" or "http://",""),port))
    addr.close()
    return good_dirs, info


dirs_used,data = Send_Req(sock,wordlist)

for num in range(10):
    print(" 1 == yes, 2 == no")
    Choice = input("Would you like to see dirs used[")
    Choice2 = input("Would you like to see info gathered[")

    if Choice == "1" and Choice2 == "1":
        for i in dirs_used:
            print(i)
        print(data)

    elif Choice == "2" and Choice2 == "2":
        print("Bye")

    elif Choice == "1" and Choice2 == "2":
        for i in dirs_used:
            print(i)

    elif Choice == "2" and Choice2 == "1":
        print(data)

    else:
        print("Invalid Choices")
