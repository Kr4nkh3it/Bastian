#fuzzing functions
import socket,time

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
    print(url,port)
    s =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((addr,port))
    return url,s,port


def Remove(text):
    text_list = list(text.split("GET"))
    try:
        txt = text_list[1]
    except:
        txt = text_list[0]
    txt = txt.replace("\n" and "\r","")


def Find_Dirs(url,addr,wordlist,db,db2,db3,out):
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


def Find_Files(url,addr,wordlist,db,db2,db3,out):
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



def Send_Req(url,addr,port,file,choice):
    counter = 0
    bad_files = []
    bad_dirs = []
    good_dirs = []
    info = []

    while counter <= 20:
        try:
            Find_Dirs(url,addr,file,good_dirs,info,bad_dirs,choice)
        except socket.error:
            print("There must of been a connection error")
            time.sleep(5)
            addr.close()
            print("Trying reconnection...")
            addr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            counter +=1
        try:
            Find_Files(url,addr,file,good_dirs,info,bad_files,choice)
        except socket.error:
            print("There must of been a connection error")
            time.sleep(5)
            addr.close()
            print("Trying reconnection...")
            addr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            addr.connect((url,port))
            counter+=1
        if counter >= 20:
            print("There were too many connection errors")
    
    addr.close()
    return info

