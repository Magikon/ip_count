#!/usr/bin/env python
# create Magikon mikayel.galyan@gmail.com

import re           # regular expression
import fileinput    # open large files
import argparse     # arguments parser
import gzip         # open gzip files
import time         # time operations

tic = time.perf_counter() # beginning time
# arguments processing
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', required=True, nargs='*', help="file path/name", type= str)
parser.add_argument('--min', '-m', help="minimal ip repeat", type= int, default= 0)
args=parser.parse_args()
# create empty dictionary
myDict={}
# find handler for file
def get_open_handler(compressed):
    if compressed:
        # mode comes in as 'r' by defualt, but that means binary to `gzip`
        return lambda file_name, mode: gzip.open(file_name, mode='rt')
    else:
        # the default mode of 'r' means text for `open`
        return open
# regex find ip in line
def find_ip_in_line(str):
    if isinstance(str, (bytes, bytearray)): str = str.decode('UTF-8')
    ip_pat=re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    temp = ip_pat.search(str)
    return temp[0] if temp else None
# open file and find ip, counts
try:
    for file_name in args.file:
        for line in fileinput.input(file_name, openhook=get_open_handler(file_name.endswith("gz"))):
            temp = find_ip_in_line(line)
            if temp:
                myDict[temp] = 1 if temp not in myDict else myDict[temp]+1
except:
    print("file not found " + file_name)
# print dictionary
for key, value in sorted(myDict.items(), key=lambda kv: kv[1], reverse=True):
    if value > args.min:
        print("{:<15}".format(key), ' - ', value)

toc = time.perf_counter() # end time 
# processed files count and time of work
print(f"Processing {len(args.file)} filles - done in {toc - tic:0.4f} seconds")
