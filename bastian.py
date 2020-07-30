import socket,time,threading
from queue import Queue
good_dirs = []
info = []
list_=Queue()
list2 = Queue()

web_loc = input("Enter url and port\nex: https://url,port[")
thrds = input("Enter amount of threads[")
if thrds == "" or thrds == " ":
    thrds = 80
else:
    thrds = int(thrds)
print("1 == yes and 2 == no")
out = input("output or no output when bruteforcing[")

wordlist = input("Enter wordlist ex: wordlist.txt[")
ext = input("Choose file extension\nex: .php[")
if ext == " " or ext == "":
    ext = ".php"

def Web_Addr(location):
    w_a_p = list(location.split(","))
    url = w_a_p[0]
    if "https://" in url or "http://" in url:
        url = url.replace("https://" or "http://","")
    if len(w_a_p) == 2:
        port = int(w_a_p[1])
    else:
        port = 80
    print(url,port)
    s =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((url,port))
    return url,s,port

url,sock,port= Web_Addr(web_loc)

def Remove(text):
    text_list = list(text.split("GET"))
    try:
        txt = text_list[1]
    except:
        txt = text_list[0]
    txt = txt.replace("\n" and "\r","")
    return txt

def Find_Dirs(word,url,addr):
    try:
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode()
        if "404" and "Error" in data or "400" and "Error" in data:
            pass
        elif Remove(data) == None:
            pass
        else:
            return word,Remove(data)
    except socket.error or TimeoutError or ConnectionAbortedError:
        print("Connection error")
        addr.close()
        time.sleep(10)
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode()
        if "404" and "Error" in data or "400" and "Error" in data:
            pass
        elif Remove(data) == None:
            pass
        else:
            return word,Remove(data)

def Find_Files(word,url,addr,db):
    try:
        for directory in db:
            addr.send(f"GET /{directory}/{word}.{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode()
            if out == "1":
                print(f"trying {url}/{directory}/{word}")
            if "404" and "Error" in data or "400" and "Error" in data:
                pass
            elif Remove(data) == None:
                pass
            else:
                return Remove(data)
    except socket.error or TimeoutError or ConnectionAbortedError:
        print("Connection error")
        addr.close()
        time.sleep(10)
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        for directory in db:
            addr.send(f"GET /{directory}/{word}.{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode()
            if out == "1":
                print(f"trying {url}/{directory}/{word}")
            if "404" and "Error" in data or "400" and "Error" in data:
                pass
            elif Remove(data) == None:
                pass
            else:
                return Remove(data)

def Gen_words(file):
    with open(file,"r") as f:
        for line in f:
            line = line.strip()
            yield line
            
dir_list = list(Gen_words(wordlist))

for word in dir_list:
    list_.put(word)

for word in dir_list:
    list2.put(word)

def threaded(addr):
    while True:
        word = list_.get()
        data,good_dir = Find_Dirs(word,url,addr)
        info.append(data)
        good_dirs.append(good_dir)
        if out == "1":
            print(f"Trying {url}/{word}")
        list_.task_done()

def threaded2(addr):
    while True:
        word = list2.get()
        data = Find_Files(word,url,addr,good_dirs)
        info.append(data)
        list2.task_done()

for thread in range(thrds):
    t = threading.Thread(target=threaded,args = [sock])
    t.daemon = True
    t.start()
list_.join()

for thread in range(thrds):
    t = threading.Thread(target=threaded2,args = [sock])
    t.daemon = True
    t.start()
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
