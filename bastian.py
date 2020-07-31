import socket,time,threading
from queue import Queue

error_codes = list(range(300,500))
good_dirs = []
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

def Web_Addr(location):
    w_a_p = list(location.split(","))
    url = w_a_p[0]
    if "https://" in url or "http://" in url:
        url = url.replace("https://" or "http://","")
    if len(w_a_p) == 2:
        port = int(w_a_p[1])
    else:
        port = 80
    return url,port

url,port= Web_Addr(web_loc)

print(f"url[{url}]\tport[{port}]\nthreads[{thrds}]\toutputchoice[{out}]\nwordlist[{wordlist}]\tfile extension[{ext}]")

def Find1(word,url):
    info = {}
    good_d = []
    try:
        if out == "1":
            print(f"Trying {url}/{word}\n and trying {url}/{word}{ext}")
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if int(data[1]) in error_codes:
            addr.close()
        else:
            if out == "1":
                print(data[2])
            info.update({word:data})
            good_d.append(word)
            addr.close()
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        recv = addr.recv(1024).decode().split("\n")[0].split(" ")
        if int(recv[1]) in error_codes:
            if len(info) < 0 and len(good_d) <0:
                addr.close()
                return None
            else:
                addr.close()
                return good_d,info
        else:
            if out == "1":
                print(recv[2])
            info.update({word+ext:recv})
            addr.close()
            return good_d,info
    except socket.error or ConnectionAbortedError:
        print("Connection error")
        addr.close()
        time.sleep(5)
        if out == "1":
            print(f"Trying {url}/{word}\n and trying {url}/{word}{ext}")
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if int(data[1]) in error_codes:
            addr.close()
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word:data})
            good_d.append(word)
            addr.close()
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        recv = addr.recv(1024).decode().split("\n")[0].split(" ")
        if int(recv[1]) in error_codes:
            if len(info) < 0 and len(good_d) <0:
                addr.close()
                return None
            else:
                addr.close()
                return good_d,info
        else:
            if out == "1":
                print(recv[2])
            info.update({word+ext:recv})
            addr.close()
            return good_d,info
    except TimeoutError:
        time.sleep(20)
        if out == "1":
            print(f"Trying {url}/{word}\n and trying {url}/{word}{ext}")
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        data = addr.recv(1024).decode().split("\n")[0].split(" ")
        if int(data[1]) in error_codes:
            addr.close()
        else:
            if out == "1" and data[2] != "Moved":
                print(data[2])
            info.update({word:data})
            good_d.append(word)
            addr.close()
        addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr.connect((url,port))
        addr.send(f"GET /{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
        recv = addr.recv(1024).decode().split("\n")[0].split(" ")
        if int(recv[1]) in error_codes:
            if len(info) < 0 and len(good_d) <0:
                addr.close()
                return None
            else:
                addr.close()
                return good_d,info
        else:
            if out == "1":
                print(recv[2])
            info.update({word+ext:recv})
            addr.close()
            return good_d,info
        
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
            if int(data[1]) in error_codes:
                addr.close()
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word:data})
                good_d.append(word)
                addr.close()
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            db.remove(directory)
            recv = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if int(recv[1]) in error_codes:
                if len(info) < 0 and len(good_d) <0:
                    addr.close()
                    return None
                else:
                    addr.close()
                    return good_d,info
            else:
                if out == "1":
                    print(recv[2])
                info.update({word+ext:recv})
                addr.close()
                return good_d,info
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
            if int(data[1]) in error_codes:
                addr.close()
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word:data})
                good_d.append(word)
                addr.close()
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            db.remove(directory)
            recv = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if int(recv[1]) in error_codes:
                if len(info) < 0 and len(good_d) <0:
                    addr.close()
                    return None
                else:
                    addr.close()
                    return good_d,info
            else:
                if out == "1":
                    print(recv[2])
                info.update({word+ext:recv})
                addr.close()
                return good_d,info
    except TimeoutError:
        time.sleep(20)
        for directory in db:
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            data = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if int(data[1]) in error_codes:
                addr.close()
            else:
                if out == "1" and data[2] != "Moved":
                    print(data[2])
                info.update({word:data})
                good_d.append(word)
                addr.close()
            addr =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            addr.send(f"GET /{directory}/{word}{ext} HTTP/1.0\r\nHost: {url}\r\n\r\n".encode("utf-8"))
            db.remove(directory)
            recv = addr.recv(1024).decode().split("\n")[0].split(" ")
            if out == "1":
                print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
            if int(recv[1]) in error_codes:
                if len(info) < 0 and len(good_d) <0:
                    addr.close()
                    return None
                else:
                    addr.close()
                    return good_d,info
            else:
                if out == "1":
                    print(recv[2])
                info.update({word+ext:recv})
                addr.close()
                return good_d,info
    
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
        try:
            good_dir,data = Find1(word,url)
        except TypeError:
            continue
        info.append(data)
        for d in good_dir:
            good_dirs.append(d)
        list_.task_done()

def threaded2():
    while True:
        word = list2.get()
        try:
            good_dir,data = Find2(word,url,good_dirs)
        except TypeError:
            continue
        for d in good_dir:
            good_dirs.append(d)
        info.append(data)
        list2.task_done()

for thread in range(thrds):
    t = threading.Thread(target=threaded)
    t.daemon = True
    t.start()
    if len(good_dirs) >=1:
        t2 = threading.Thread(target=threaded2)
        t2.daemon = True
        t2.start()

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
