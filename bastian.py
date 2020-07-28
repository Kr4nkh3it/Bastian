import socket,threading,time
from queue import Queue

web_loc = input("Enter url and port\nex: https://url:port[")
print("1 == yes and 2 == no")
out = input("output or no output when bruteforcing[")

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

sock =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect((url.replace("https://" or "http://",""),port))
except:
    sock.connect((url,port))
    
wordlist = input("Enter wordlist ex: wordlist.txt[")
ext = input("Choose file extension\nex: .php[")
if ext == " " or ext == "":
    ext = ".php"

def Remove(text):
    text_list = list(text.split("GET"))
    try:
        txt = text_list[1]
    except:
        txt = text_list[0]
    txt = txt.replace("\n" and "\r","")

def Find_Dirs(addr,wordlist,db,db2,db3):
    with open(wordlist,'r') as f:
        for directory in f:
            addr.send(f"GET /{directory} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            if out == "1":
                print(f"checking {url}/{directory}")
            data = addr.recv(1000)
            data = data.decode("utf-8")
            if "404" and "Error" in data or "400" and "Error" in data:
                db3.append(directory)
            elif Remove(data) == None:
                pass
            else:
                db.append(directory)
                db2.append(Remove(data))

def Find_Files(addr,wordlist,db,db2,db3):
    with open(wordlist,'r') as f:
        for directory in db:
            for file in f:
                addr.send(f"GET /{directory}/{file}.{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
                if out == "1":
                    print(f"checking {url}/{directory}/{file}.{ext}")
                data = addr.recv(1000)
                data = data.decode("utf-8")
                if "404" and "Error" in data or "400" and "Error" in data:
                    db3.append(file)
                elif Remove(data) == None:
                    pass
                else:
                    db2.append(Remove(data))

def Send_Req(addr,file):
    counter = 0
    bad_files = []
    bad_dirs = []
    good_dirs = []
    info = []

    while counter <= 20:
        try:
            Find_Dirs(addr,file,good_dirs,info,bad_dirs)
        except socket.error:
            print("There must of been a connection error")
            time.sleep(5)
            addr.close()
            print("Trying reconnection...")
            addr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url.replace("https://" or "http://",""),port))
            counter +=1
        try:
            Find_Files(addr,file,good_dirs,info,bad_files)
        except socket.error:
            print("There must of been a connection error")
            time.sleep(5)
            addr.close()
            print("Trying reconnection...")
            addr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url.replace("https://" or "http://",""),port))
            counter+=1
    if counter >= 20:
        print("There were too many connection errors")
    
    addr.close()
    return good_dirs, info


dirs_used,data = Send_Req(sock,wordlist)

for dr in dirs_used:
    if dr.count() >= 2:
        dirs_used.remove(dr)

for num in range(10):
    print(" 1 == yes, 2 == no")
    Choice = input("Would you like to see dirs used[")
    Choice2 = input("Would you like to see info gathered[")

    if data == None:
        data = "No info was gathered"

    if Choice == "1" and Choice2 == "1":
        for i in dirs_used:
            print(i)
        print(data)
        break
    
    elif Choice == "2" and Choice2 == "2":
        print("Bye")
        break
    
    elif Choice == "1" and Choice2 == "2":
        for i in dirs_used:
            print(i)
        break
    
    elif Choice == "2" and Choice2 == "1":
        print(data)
        break
    else:
        print("Invalid Choices")


