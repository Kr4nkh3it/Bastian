import socket,time

error_codes = list(range(300,500))
good_dirs = []

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

def Find1(word,url,port,out,ext):
    info = {}
    good_d = []
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
            time.sleep(5)
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
            time.sleep(5)
        info.update({word+ext:recv})
        addr.close()
        return good_d,info

def Find2(word,url,port,db,out,ext):
    good_d = []
    info = {}
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
            if out == "1":
                print(data[2])
                time.sleep(5)
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
                time.sleep(5)
            info.update({word+ext:recv})
            addr.close()
            return good_d,info

def Gen_words(file):
    with open(file,"r") as f:
        for line in f:
            line = line.strip()
            yield line

def threaded(list_,url,port,out,ext,info,errors):
    while True:
        word = list_.get()
        try:
            good_dir,data = Find1(word,url,port,out,ext)
        except TypeError:
            continue
        except socket.error or ConnectionAbortedError or ConnectionResetError:
            errors+1
            time.sleep(20)
            try:
                good_dir,data = Find1(word,url,port,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                good_dir,data = Find1(word,url,port,out,ext)
            except TypeError:
                continue
        info.append(data)
        for d in good_dir:
            good_dirs.append(d)
        list_.task_done()

def threaded2(list2,url,port,out,ext,info,errors):
    while True:
        word = list2.get()
        try:
            good_dir,data = Find2(word,url,port,good_dirs,out,ext)
        except TypeError:
            continue
        except socket.error or ConnectionAbortedError or ConnectionResetError:
            errors+1
            time.sleep(20)
            try:
                good_dir,data = Find2(word,url,port,good_dirs,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                good_dir,data = Find2(word,url,port,good_dirs,out,ext)
            except TypeError:
                continue
        for d in good_dir:
            good_dirs.append(d)
        info.append(data)
        list2.task_done()

