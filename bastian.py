import time,threading,argparse
from queue import Queue
from fuzz import *

errors = 0
#info gotten from find1 and find2
info = []
#wordlist queue
list_=Queue()
list2 = Queue()
print_lock = threading.Lock()

parser = argparse.ArgumentParser(description="Get specifications")
parser.add_argument("-u","--url",help="specifies the url")
parser.add_argument("-t","--threads",type=int,help="specifies threads")
parser.add_argument("-o","--output",help="output choice\n do 1 = yes 2 = no")
parser.add_argument("-w","--wordlist",help="specifies wordlist")
parser.add_argument("-e","--extension",help="file extension")
args = parser.parse_args()

url = args.url
thrds = args.threads
out = args.output
wordlist = args.wordlist
ext = args.extension

if thrds == None:
    thrds = 200
if out == None:
    out = "1"
if ext == None:
    ext = ".php"

print(f"url[{url}]\tthreads[{thrds}]\noutputchoice[{out}]\twordlist[{wordlist}]\nfile extension[{ext}]")

#Creates a wordlist
dir_list = list(Gen_words(wordlist))

for word in dir_list:
    list_.put(word)
    list2.put(word)

#creates a thread for every number in a range given by the user and runs all the threads
for thread in range(thrds):
    if errors <= 40:
        t = threading.Thread(target=threaded,args = [list_,url,out,ext,errors])
        t.daemon = True
        t.start()
        if len(database) >=1:
            t2 = threading.Thread(target=threaded2,args = [list2,url,out,ext,errors])
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
