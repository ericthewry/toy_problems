#! /usr/bin/python

import argparse
import math

def main():
    # parse the input
    parser = argparse.ArgumentParser(description="An algorithm for the stock market problem")
    parser.add_argument("infile", help="The file containing the length of the input and the input")
    parser.add_argument("outfile", help="The file to which the output should be written")
    args = parser.parse_args()

    # inlist contains the lines of the input file
    inlist = []
    # read the file
    with open(args.infile) as f:
        inlist = [int(x.strip('\n')) for x in f.readlines()]


    # write to output
    (length, start, seq) = nondecreasing(0,-1, -1,inlist[1:])
    outdata = [len(seq), start]
    print(seq)
    for s in seq:
        outdata.append(s)

    # open the destination file and write to it
    with open(args.outfile, "r+") as f:
        # empty file
        f.seek(0)
        f.truncate()
        # write to file
        for line in outdata:
            f.write(str(line) + "\n")


            
def nondecreasing(start, loat, loatSt, prices):
    """Find the longest sequence of elements that do not decrease

    Keyword Arguments:
    prices -- the sequence of prices

    Return:
    a tuple of the length of the longest nondecreasing sequence,
    the start day, and the longest sequence of nondecreasing
    """
    print(start)
    if start+1 >= len(prices):
        print(loat, loatSt)
        return (loat, loatSt+1, prices[loatSt : loat + loatSt])
    
    i = start + 1
    curLen = 1
    while (i < len(prices)) and prices[i-1] <= prices[i]:
        print(prices[i-1], "<=", prices[i])
        curLen += 1
        i+=1

    print(prices[start:(start+curLen)], prices[loatSt:(loatSt + loat)])
        
    if curLen >= loat:
        print("longer!")
        return nondecreasing(i, curLen, start, prices)
    else:
        return nondecreasing(i, loat, loatSt, prices)
        
    
    

            
if __name__ == "__main__" : main()
