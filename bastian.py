import socket,time,threading
from queue import Queue

good_dirs = []
info = []
list_=Queue()
list2 = Queue()
print_lock = threading.Lock()

web_loc = input("Enter url and port\nex: https://url,port[")
thrds = input("Enter amount of threads[")
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
    info = {}
    good_d = []
    try:
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if "400" or "404"  in data[1] or "300" or "301" in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word:data})
            good_d.append(word)
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if "400" or "404"  in data[1] or "300" or "301" in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word+ext:data})
        return good_d,info
        addr.close()
    except socket.error or ConnectionAbortedError:
        print("Connection error")
        addr.close()
        time.sleep(5)
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if "400" or "404"  in data[1] or "300" or "301" in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word:data})
            good_d.append(word)
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if "400" or "404"  in data[1] or "300" or "301" in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word+ext:data})
        return good_d,info
        addr.close()
    except TimeoutError:
        time.sleep(20)
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if "400" or "404"  in data[1] or "300" or "301" in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word:data})
            good_d.append(word)
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if "400" or "404"  in data[1] or "300" or "301" in data[1]:
            pass
        elif data == None:
            pass
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word+ext:data})
        return good_d,info
        addr.close()
        
def Find2(word,url,db):
    good_d = []
    info = {}
    try:
        for directory in db:
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if "400" or "404"  in data[1] or "300" or "301" in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word:data})
                good_d.append(word)
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if "400" or "404"  in data[1] or "300" or "301" in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word+ext:data})
            return good_d,info
            addr.close()
    except socket.error or ConnectionAbortedError:
        print("Connection error")
        time.sleep(5)
        for directory in db:
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if "400" or "404"  in data[1] or "300" or "301" in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word:data})
                good_d.append(word)
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if "400" or "404"  in data[1] or "300" or "301" in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word+ext:data})
            return good_d,info
            addr.close()
    except TimeoutError:
        time.sleep(20)
        for directory in db:
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if "400" or "404"  in data[1] or "300" or "301" in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word:data})
                good_d.append(word)
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if "400" or "404"  in data[1] or "300" or "301" in data[1]:
                pass
            elif data == None:
                pass
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word+ext:data})
            return good_d,info
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
        for d in good_dir:
            good_dirs.append(d)
        if out == "1":
            print(f"Trying {url}/{word}\n and trying {url}/{word}{ext}")
        list_.task_done()

def threaded2():
    while True:
        word = list2.get()
        good_dir,data = Find2(word,url,good_dirs)
        for d in good_dir:
            good_dirs.append(d)
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
