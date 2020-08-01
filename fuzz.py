import socket,time

error_codes = range(300,500)
database = []

#takes  a url and splits it into sections then return the working url
def Web_Addr(location):
    w_a_p = list(location.split(","))
    url = w_a_p[0]
    if "https://" in url or "http://" in url:
        addr = url.replace("https://" or "http://","")
    else:
        addr = url
    if len(w_a_p) == 2:
        port = int(w_a_p[1])
    else:
        port = 80
    return addr,url,port

def Connect(addr,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((addr,port))
    return sock

#Gets http request through a dictionary type attack looks for directories and files
#returns information that it got from both file and directory or either
def Find1(db,loc,word,url,port,out,ext):
    if out == "1":
        print(f"Trying {url}/{word}\n and trying {url}/{word}{ext}")
    addr = Connect(loc,port)
    addr.send(f"HEAD /{word} HTTP/1.0\r\nHost:{url}\r\n\r\n".encode("utf-8"))
    status = addr.recv(1024).decode().split("\n")[0].split(" ")
    if len(status) < 2:
        addr.close()
        if out == "1":
            print("site returned nothing")
    else:
        status_code = int(status[1])
    if status_code in error_codes:
        if out == "1":
            print(f"status code[{status_code}] bad dir[{word}]")
        addr.close()
    else:
        if out == "1":
            print(f"status code[{status_code}] good dir[{word}]")
        db.append(word)
        addr.close()
    addr = Connect(loc,port)
    addr.send(f"HEAD /{word}{ext} HTTP/1.0\r\nHost:{url}\r\n\r\n".encode("utf-8"))
    status2 = addr.recv(1024).decode().split("\n")[0].split(" ")
    if len(status2) < 2:
        addr.close()
        if out == "1":
            print("site returned nothing")
        return None
    else:
        status_code = int(status2[1])
    if status_code in error_codes:
        if out == "1":
            print(f"status code[{status_code}] bad file[{word}{ext}]")
        addr.close()
        return None
    else:
        if out == "1":
            print(f"status code[{status_code}] good file[{word}{ext}]")
            time.sleep(5)
        addr.close()
        return db.append(word+ext)

#same thing as the last one but it uses good directories gotten from the last one to look for more directories and files inside of the good one
def Find2(loc,word,url,port,db,out,ext):
    for directory in db:
        addr = Connect(loc,port)
        addr.send(f"HEAD /{directory}/{word} HTTP/1.0\r\nHost:{url}\r\n\r\n".encode("utf-8"))
        status = addr.recv(1024).decode().split("\n")[0].split(" ")
        if out == "1":
            print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
        if len(status) < 2:
            addr.close()
            if out == "1":
                print("site returned nothing")
        else:
            status_code = int(status[1])
        if status_code in error_codes:
            if out == "1":
                print(f"status code[{status_code}] bad dir[{directory}/{word}]")
            addr.close()
        else:
            if out == "1":
                print(f"status code[{status_code}] good dir[{directory}/{word}]")
            db.append(f"{directory}/{word}")
            addr.close()
        addr = Connect(loc,port)
        addr.send(f"HEAD /{directory}/{word}{ext} HTTP/1.0\r\nHost:{url}\r\n\r\n".encode("utf-8"))
        status2 = addr.recv(1024).decode().split("\n")[0].split(" ")
        if out == "1":
            print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
        if len(status2) < 2:
            addr.close()
            if out == "1":
                print("site returned nothing")
            return None
        else:
            status_code = int(status2[1])
        if status_code in error_codes:
            if out == "1":
                print(f"status code[{status_code}] bad file[{directory}/{word}{ext}")
            addr.close()
            return None
        else:
            if out == "1":
                print(f"status code[{status_code}] good file[{directory}/{word}{ext}]")
            addr.close()
            return db.append(f"{directory}/{word}{ext}")

#Generates a list of words gotten from a wordlist file
def Gen_words(file):
    with open(file,"r") as f:
        for line in f:
            line = line.strip()
            yield line

#runs find1 through each word in the wordlist
def threaded(loc,list_,url,port,out,ext,errors):
    while True:
        word = list_.get()
        try:
            Find1(database,loc,word,url,port,out,ext)
        except TypeError:
            continue
        except socket.error or ConnectionAbortedError or ConnectionResetError:
            errors+1
            time.sleep(20)
            try:
                Find1(database,loc,word,url,port,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                Find1(database,loc,word,url,port,out,ext)
            except TypeError:
                continue
        list_.task_done()

#runs find2 through each word in the wordlist
def threaded2(loc,list2,url,port,out,ext,errors):
    while True:
        word = list2.get()
        try:
            Find2(loc,word,url,port,database,out,ext)
        except TypeError:
            continue
        except socket.error or ConnectionAbortedError or ConnectionResetError:
            errors+1
            time.sleep(20)
            try:
                Find2(loc,word,url,port,database,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                Find2(loc,word,url,port,database,out,ext)
            except TypeError:
                continue
        list2.task_done()

