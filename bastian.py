import socket,time,threading,argparse
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
parser.add_argument("-e","--extention",help="file extension")
args = parser.parse_args()

web_loc = args.url
thrds = args.threads
out = args.output
wordlist = args.wordlist
ext = args.extention

if thrds == None:
    thrds = 200
if out == None:
    out = 1
if ext == None:
    ext = ".php"

#returns url and port from a function
sock,url,port= Web_Addr(web_loc)

print(f"url[{url}]\tport[{port}]\nthreads[{thrds}]\toutputchoice[{out}]\nwordlist[{wordlist}]\tfile extension[{ext}]")
time.sleep(5)

#Creates a wordlist
dir_list = list(Gen_words(wordlist))

for word in dir_list:
    list_.put(word)

for word in dir_list:
    list2.put(word)

#creates a thread for every number in a range given by the user and runs all the threads
for thread in range(thrds):
    if errors <= 40:
        t = threading.Thread(target=threaded,args = [sock,list_,url,port,out,ext,info,errors])
        t.daemon = True
        t.start()
        if len(good_dirs) >=1:
            t2 = threading.Thread(target=threaded2,args = [sock,list2,url,port,out,ext,info,errors])
            t2.daemon = True
            t2.start()
    else:
        print("Too many errors occured\n1 == yes 2 == no")
        choice = input("Continue?[")
        if choice == "1":
            continue
        else:
            break

list_.join()
list2.join()  

#Choice to display the data 
if info == None:
    print("No info was gathered")
else:
    for data in info:
        print(data)
