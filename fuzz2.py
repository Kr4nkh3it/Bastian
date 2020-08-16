import time
import http.client

error_codes = range(300,500)
database = []

#Gets http request through a dictionary type attack looks for directories and files
#returns information that it got from both file and directory or either
def Find1(method,db,db2,word,url,port,prtcl,out,ext):
    if out == "1":
        print(f"Trying {url}/{word}\nand trying {url}/{word}{ext}")
    if prtcl == "http":
        addr = http.client.HTTPConnection(url,port)
    elif prtcl == "https":
        addr = http.client.HTTPSConnection(url,port)
    else:
        addr = http.client.HTTPSConnection(url,port)
    if method == "1":
        addr.request("HEAD",f"/{word}")
        recv = addr.getresponse()
    else:
        addr.request("GET",f"/{word}")
        recv = addr.getresponse()
    status_code = int(recv.status)
    if status_code in db2:
        if out == "1":
            print(f"status code[{status_code}] bad dir[{word}]")
    else:
        if out == "1":
            print(f"status code[{status_code}] good dir[{word}]")
        db.append(word)
    addr.close()
    if prtcl == "http":
        addr2 = http.client.HTTPConnection(url,port)
    elif prtcl == "https":
        addr2 = http.client.HTTPSConnection(url,port)
    if method == "1":
        addr2.request("HEAD",f"/{word}{ext}")
        recv2 = addr2.getresponse()
    else:
        addr2.request("GET",f"/{word}{ext}")
        recv2 = addr2.getresponse()
    status_code2 = int(recv2.status)
    if status_code2 in db2:
        if out == "1":
            print(f"status code[{status_code2}] bad file[{word}{ext}]")
        addr2.close()
        return None
    else:
        if out == "1":
            print(f"status code[{status_code2}] good file[{word}{ext}]")
        addr2.close()
        return db.append(word+ext)
    
#same thing as the last one but it uses good directories gotten from the last one to look for more directories and files inside of the good one
def Find2(method,word,url,port,prtcl,db,db2,out,ext):
    for directory in db:
        if prtcl == "http":
            addr = http.client.HTTPConnection(url,port)
        elif prtcl == "https":
            addr = http.client.HTTPSConnection(url,port)
        if method == "1":
            addr.request("HEAD",f"/{directory}/{word}")
            recv = addr.getresponse()
        else:
            addr.request("GET",f"/{directory}/{word}")
            recv = addr.getresponse()
        status_code = int(recv.status)
        if out == "1":
            print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
        if status_code in db2:
            if out == "1":
                print(f"status code[{status_code}] bad dir[{directory}/{word}]")
        else:
            if out == "1":
                print(f"status code[{status_code}] good dir[{directory}/{word}]")
            db.append(f"{directory}/{word}")
        if prtcl == "http":
            addr2 = http.client.HTTPConnection(url,port)
        elif prtcl == "https":
            addr2 = http.client.HTTPSConnection(url,port)
        if method == "1":
            addr2.request("HEAD",f"/{directory}/{word}{ext}")
            recv2 = addr2.getresponse()
        else:
            addr2.request("GET",f"/{directory}/{word}{ext}")
            recv2 = addr2.getresponse()
        status_code2 = int(recv.status)
        if out == "1":
            print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
        if status_code2 in db2:
            if out == "1":
                print(f"status code[{status_code2}] bad file[{directory}/{word}{ext}")
            return None
        else:
            if out == "1":
                print(f"status code[{status_code2}] good file[{directory}/{word}{ext}]")
            return db.append(f"{directory}/{word}{ext}")

#Generates a list of words gotten from a wordlist file
def Gen_words(file):
    with open(file,"r") as f:
        for line in f:
            line = line.strip()
            yield line

#runs find1 through each word in the wordlist
def threaded(prtcl,port,method,list_,url,out,ext,errors):
    while True: 
        word = list_.get()
        try:
            Find1(method,database,error_codes,word,url,port,prtcl,out,ext)
        except TypeError:
            continue
        except http.client.RemoteDisconnected or http.client.ResponseNotReady:
            errors+1
            time.sleep(20)
            try:
                Find1(method,database,error_codes,word,url,port,prtcl,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                Find1(method,database,error_codes,word,url,port,prtcl,out,ext)
            except TypeError:
                continue
        except:
            print("[SSL Error]:Change ports")
            break
        list_.task_done()
        
#runs find2 through each word in the wordlist
def threaded2(prtcl,port,method,list2,url,out,ext,errors):
    while True:
        word = list2.get()
        try:
            Find2(word,url,port,prtcl,database,error_codes,out,ext)
        except TypeError:
            continue
        except http.client.RemoteDisconnected or http.client.ResponseNotReady:
            errors+1
            time.sleep(20)
            try:
                Find2(word,url,port,prtcl,database,error_codes,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                Find2(word,url,port,prtcl,database,error_codes,out,ext)
            except TypeError:
                continue
    list2.task_done()

