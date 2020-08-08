import requests,time

error_codes = range(300,500)
database = []

#Gets http request through a dictionary type attack looks for directories and files
#returns information that it got from both file and directory or either
def Find1(method,db,db2,word,url,out,ext):
    if out == "1":
        print(f"Trying {url}/{word}\nand trying {url}/{word}{ext}")
    if method == "1":
        rec = requests.head(f"{url}/{word}")
    else:
        rec = requests.get(f"{url}/{word}")
    status_code = int(rec.status_code)
    if status_code in db2:
        if out == "1":
            print(f"status code[{status_code}] bad dir[{word}]")
    else:
        if out == "1":
            print(f"status code[{status_code}] good dir[{word}]")
        db.append(word)
    if method == "1":
        rec2 = requests.head(f"{url}/{word}{ext}")
    else:
        rec2 = requests.get(f"{url}/{word}{ext}")
    status_code2 = int(rec2.status_code)
    if status_code2 in db2:
        if out == "1":
            print(f"status code[{status_code2}] bad file[{word}{ext}]")
        return None
    else:
        if out == "1":
            print(f"status code[{status_code2}] good file[{word}{ext}]")
            time.sleep(5)
        return db.append(word+ext)

#same thing as the last one but it uses good directories gotten from the last one to look for more directories and files inside of the good one
def Find2(method,word,url,db,db2,out,ext):
    for directory in db:
        if method == "1":
            rec = requests.head(f"{url}/{directory}/{word}")
        else:
            rec = requests.get(f"{url}/{directory}/{word}")
        status_code = int(rec.status_code)
        if out == "1":
            print(f"trying {url}/{directory}/{word}{ext}\nand trying {url}/{directory}/{word}")
        if status_code in db2:
            if out == "1":
                print(f"status code[{status_code}] bad dir[{directory}/{word}]")
        else:
            if out == "1":
                print(f"status code[{status_code}] good dir[{directory}/{word}]")
            db.append(f"{directory}/{word}")
        if method == "1":
            rec2 = requests.head(f"{url}/{directory}/{word}{ext}")
        else:
            rec2 = requests.get(f"{url}/{directory}/{word}{ext}")
        status_code2 = int(rec2.status_code)
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
def threaded(method,list_,url,out,ext,errors):
    while True:
        word = list_.get()
        try:
            Find1(method,database,error_codes,word,url,out,ext)
        except TypeError:
            continue
        except ConnectionAbortedError or ConnectionResetError:
            errors+1
            time.sleep(20)
            try:
                Find1(method,database,error_codes,word,url,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                Find1(method,database,error_codes,word,url,out,ext)
            except TypeError:
                continue
        list_.task_done()

#runs find2 through each word in the wordlist
def threaded2(method,list2,url,out,ext,errors):
    while True:
        word = list2.get()
        try:
            Find2(method,word,url,database,error_codes,out,ext)
        except TypeError:
            continue
        except ConnectionAbortedError or ConnectionResetError:
            errors+1
            time.sleep(20)
            try:
                Find2(method,word,url,database,error_codes,out,ext)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                Find2(method,word,url,database,error_codes,out,ext)
            except TypeError:
                continue
        list2.task_done()
