import time,threading,argparse
from queue import Queue
from fuzz2 import *

errors = 0
#info gotten from find1 and find2
info = []
#wordlist queue
list_=Queue()
list2 = Queue()
print_lock = threading.Lock()

parser = argparse.ArgumentParser(description="Get specifications")
parser.add_argument("-u","--url",help="specifies the url")
parser.add_argument("-p","--port",help="specifies the port")
parser.add_argument("-t","--threads",type=int,help="specifies threads")
parser.add_argument("-o","--output",help="output choice\n do 1 = yes 2 = no")
parser.add_argument("-w","--wordlist",help="specifies wordlist")
parser.add_argument("-e","--extension",help="file extension")
parser.add_argument("-m","--method",help="choose between request methods\n1 = head, 2 = get")
args = parser.parse_args()

url = args.url
port = args.port
threads = args.threads
out = args.output
wordlist = args.wordlist
ext = args.extension
method = args.method

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
    list2.put(word)

#creates a thread for every number in a range given by the user and runs all the threads
for thread in range(threads):
    if errors <= 40:
        t = threading.Thread(target=threaded,args = [prt,port,method,list_,url,out,ext,errors])
        t.daemon = True
        t.start()
        if len(database) >=1:
            t2 = threading.Thread(target=threaded2,args = [prt,port,method,list2,url,out,ext,errors])
            t2.daemon = True
            t2.start()
    else:
        print("Too many errors occured")

list_.join()
list2.join()  

#Choice to display the data 
if info == None:
    print("No info was gathered")
else:
    for data in info:
        print(data)

