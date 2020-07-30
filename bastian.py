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
    return url,port

url,port= Web_Addr(web_loc)

def Find1(word,url):
    try:
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if str(range(400,500))  in data[1] or str(range(300,400)) in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            return word,data[2]
        addr.close()
    except socket.error or ConnectionAbortedError:
        print("Connection error")
        addr.close()
        time.sleep(5)
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if str(range(400,500))  in data[1] or str(range(300,400)) in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            return word,data[2]
    except TimeoutError:
        time.sleep(20)
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if str(range(400,500))  in data[1] or str(range(300,400)) in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            return word,data[2]
        
def Find2(word,url,db):
    try:
        for directory in db:
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if str(range(400,500))  in data[1] or str(range(300,400)) in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                return word,data[2]
            addr.close()
    except socket.error or ConnectionAbortedError:
        print("Connection error")
        time.sleep(5)
        for directory in db:
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if str(range(400,500))  in data[1] or str(range(300,400)) in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                return word,data[2]
            addr.close()
    except TimeoutError:
        time.sleep(20)
        for directory in db:
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if str(range(400,500))  in data[1] or str(range(300,400)) in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                return word,data[2]
            addr.close()
    
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

def threaded():
    while True:
        word = list_.get()
        good_dir,data = Find1(word,url)
        info.append(data)
        good_dirs.append(good_dir)
        if out == "1":
            print(f"Trying {url}/{word}\n and trying {url}/{word}{ext}")
        list_.task_done()

def threaded2():
    while True:
        word = list2.get()
        good_dir,data = Find2(word,url,good_dirs)
        good_dirs.append(good_dir)
        info.append(data)
        list2.task_done()

for thread in range(thrds):
    t = threading.Thread(target=threaded)
    t.daemon = True
    t.start()
list_.join()

if len(good_dirs) >=1:
    for thread in range(thrds):
        t = threading.Thread(target=threaded2)
        t.daemon = True
        t.start()
    list2.join()
else:
    pass

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
