#!/usr/bin/env python
# creator Magikon, mikayel.galyan@gmail.com
"""find requested ip's count"""
import re
import fileinput
import argparse
import gzip
import time

def dictPrintSorted(dict, min, keylen=15):
    """print sorted dictionary by value """
    for key, value in sorted(dict.items(), key=lambda kv: kv[1], reverse=True):
        if value > min: print("{:<{}}".format(key,keylen), ' - ', value)

try:
    tic = time.perf_counter() # beginning time
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True, nargs='*', help="file path/name", type= str)
    parser.add_argument('--min', '-m', help="minimal ip repeat", type= int, default= 0)
    args=parser.parse_args()
    myDict={}

    for line in fileinput.input(args.file, openhook=fileinput.hook_compressed):
        if isinstance(line, (bytes, bytearray)): line = line.decode('UTF-8')
        temp = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if temp: myDict[temp[0]] = 1 if temp[0] not in myDict else myDict[temp[0]] + 1

    dictPrintSorted(myDict, args.min)

    toc = time.perf_counter() # end time
    print(f"Processing {len(args.file)} filles - done in {toc - tic:0.4f} seconds")

except Exception as e:
    print(e)
