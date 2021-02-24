#!/usr/bin/env python
# creator Magikon, mikayel.galyan@gmail.com
"""find requested ip's count"""
import re           # regular expression
import fileinput    # open large files
import argparse     # arguments parser
import gzip         # open gzip files
import time         # time operations

def findRe(strfind, strre=r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'):
    """create pattern and search it in given line"""
    if isinstance(strfind, (bytes, bytearray)): strfind = strfind.decode('UTF-8')
    temp = re.compile(strre).search(strfind)
    return temp[0] if temp else None

def dictPrintSorted(dict, min, keylen=15):
    """print sorted dictionary by value """
    for key, value in sorted(dict.items(), key=lambda kv: kv[1], reverse=True):
        if value > min: print("{:<{}}".format(key,keylen), ' - ', value)

def get_open_handler(file):
     """get openhook for file"""
     return (lambda file, mode: gzip.open(file, mode='rt')) if file.endswith(".gz") else open

try:
    tic = time.perf_counter() # beginning time
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True, nargs='*', help="file path/name", type= str)
    parser.add_argument('--min', '-m', help="minimal ip repeat", type= int, default= 0)
    args=parser.parse_args()
    myDict={}

    for file_name in args.file:
        for line in fileinput.input(file_name, openhook=get_open_handler(file_name)):
            temp = findRe(line)
            if temp: myDict[temp] = 1 if temp not in myDict else myDict[temp]+1

    dictPrintSorted(myDict, args.min)
except Exception as e:
    print(e)

toc = time.perf_counter() # end time
print(f"Processing {len(args.file)} filles - done in {toc - tic:0.4f} seconds")