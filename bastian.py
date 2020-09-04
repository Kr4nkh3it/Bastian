import time,threading,argparse,http.client
from queue import Queue

#Generates a list of words gotten from a wordlist file
def Gen_words(file):
    with open(file,"r") as f:
        for line in f:
            line = line.strip()
            yield line

#runs find1 through each word in the wordlist
def threaded(db,db2,prtcl,port,method,list_,url,out,ext,errors,file,choice):   
    while True:
        word = list_.get()
        try:
            Find(method,db,db2,word,url,port,prtcl,out,ext,file,choice)
        except TypeError:
            continue
        except http.client.RemoteDisconnected or http.client.ResponseNotReady:
            errors+1
            time.sleep(20)
            try:
                Find(method,db,db2,word,url,port,prtcl,out,ext,file,choice)
            except TypeError:
                continue
        except TimeoutError:
            errors+1
            time.sleep(50)
            try:
                Find(method,db,db2,word,url,port,prtcl,out,ext,file,choice)
            except TypeError:
                continue
        except:
            print("[SSL Error]:Change ports")
            break
        list_.task_done()
        
def Find(method,db,db2,wrd,url,port,prtcl,out,ext,file,choice):
    send_head = f"/{wrd}"
    send_get = f"/{wrd}"
    directory = ""
    sendf_head = f"/{wrd}{ext}"
    sendf_get = f"/{wrd}{ext}"
    files = ""
    init = 0
    count = 0
    while count!= 100:
        count+=1
        if init == 1:
            files = ""
        if out == "1":
            print(f"Trying {url}/{directory}\nand trying {url}/{files}{ext}")
        if prtcl == "http":
            addr = http.client.HTTPConnection(url,port)
        elif prtcl == "https":
            addr = http.client.HTTPSConnection(url,port)
        else:
            addr = http.client.HTTPSConnection(url,port)
        if method == "1":
            directory+=send_head
            addr.request("HEAD",directory)
            recv = addr.getresponse()
        else:
            directory+=send_head
            addr.request("GET",directory)
            recv = addr.getresponse()
        status_code = int(recv.status)
        if status_code in db2:
            if out == "1":
                print(f"status code[{status_code}] bad dir[{directory}]")
        else:
            if out == "1":
                print(f"status code[{status_code}] good dir[{directory}]")
                good_dir = directory
            if choice == 1:
                file.write(good_dir)
            db.append(good_dir)
        addr.close()
        if prtcl == "http":
            addr2 = http.client.HTTPConnection(url,port)
        elif prtcl == "https":
            addr2 = http.client.HTTPSConnection(url,port)
        if method == "1":
            init+=1
            if init >= 1:
                files+=send_head
                addr2.request("HEAD",files+sendf_head)
            else:
                files+=sendf_head
                addr2.request("HEAD",files)
            recv2 = addr2.getresponse()
        else:
            init+=1
            if init >= 1:
                files+=send_get
                addr2.request("GET",files+sendf_get)
            else:
                files+=sendf_get
                addr2.request("GET",files)
            recv2 = addr2.getresponse()
        status_code2 = int(recv2.status)
        if status_code2 in db2:
            if out == "1":
                print(f"status code[{status_code2}] bad file[{files}{ext}]")
            addr2.close()
        else:
            if out == "1":
                print(f"status code[{status_code2}] good file[{files}{ext}]")
                good_file = files
            addr2.close()
            if choice == 1:
                file.write(good_file)
            db.append(good_file)

errors = 0
info = []
error_codes = range(300,500)
database = []
#wordlist queue
list_=Queue()
list2 = Queue()
list3 = Queue()
print_lock = threading.Lock()

parser = argparse.ArgumentParser(description="Get specifications")
parser.add_argument("-u","--url",help="specifies the url")
parser.add_argument("-p","--port",help="specifies the port")
parser.add_argument("-t","--threads",type=int,help="specifies threads")
parser.add_argument("-o","--output",help="output choice\n do 1 = yes 2 = no")
parser.add_argument("-w","--wordlist",help="specifies wordlist")
parser.add_argument("-e","--extension",help="file extension")
parser.add_argument("-m","--method",help="choose between request methods\n1 = head, 2 = get")
parser.add_argument("-T","--textfile",help="choose textfile writing or not\n1=yes, 2=no")
args = parser.parse_args()

url = args.url
port = args.port
threads = args.threads
out = args.output
wordlist = args.wordlist
ext = args.extension
method = args.method
textfile = args.textfile

def url_parse(url):
    if "https://" in url or "http://" in url:
        urllist = url.split(":")
        protocol = urllist[0]
        url = urllist[1].replace("//","")
        return url,protocol
    else:
        print("invalid url")
url,prt = url_parse(url)

port = int(port)
if threads == None:
    threads = 200
else:
    threads = int(threads)
if out == None:
    out = "1"
if ext == None:
    ext = ".php"
if method == None:
    method = "2"
op = ""
if out == "1":
    op+="yes"
else:
    op+="no"
mth = ""
if method == "1":
    mth+="head"
else:
    mth+="get"
if  textfile == None:
    tchoice = 2
else:
    tchoice = int(textfile)

if tchoice == 1:
    file = open(f"{url}dirs.txt","w")
else:
    file = None

"""
you have found the all mighty bastian
he will grant you one wish message @untoterarzt on instagram 
        /\__/\
      /`          '\
 === 0     0 ===
      \     ----    /
      /             \
    /                 \
  |                     |
  |   ||     ||    |
   \_oo__oo_ /===+
"""
print(f"url[{url}]\tthreads[{threads}]\noutputchoice[{op}]\twordlist[{wordlist}]\nfile extension[{ext}]\tmethod [{mth}]")

#Creates a wordlist
dir_list = list(Gen_words(wordlist))

for word in dir_list:
    list_.put(word)


#creates a thread for every number in a range given by the user and runs all the threads
for thread in range(threads):
    if errors <= 40:
        t = threading.Thread(target=threaded,args = [database,error_codes,prt,port,method,list_,url,out,ext,errors,file,tchoice])
        t.daemon = True
        t.start()
    else:
        print("Too many errors occured")
    

list_.join()
#Choice to display the data 
if info == None:
    print("No info was gathered")
else:
    for data in info:
        print(data)
if tchoice == 1:
    file.close()
