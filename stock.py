#! /usr/bin/python

# This file contains the solution to a simple stock market problem, i.e. the
# nondecreasing sublist problem. This should run on python2.7* and
# python3, but was developed using python3.

import argparse
import math

def main():
    # parse the input
    parser = argparse.ArgumentParser(description="An algorithm for the stock market problem")
    parser.add_argument("infile",  help="The file containing the length of the input and the input")
    parser.add_argument("outfile", help="The file to which the output should be written")
    args = parser.parse_args()

    # inlist contains the lines of the input file
    inlist = []
    # read the file
    with open(args.infile) as f:
        inlist = [int(x.strip('\n')) for x in f.readlines()]


    # collect solution
    (length, start, seq) = nondecreasing(0,-1, -1,inlist[1:])
    outdata = [len(seq), start]
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
    start  -- the start index of this recursive call
    loat   -- an accumulator collecting the length that is Longest Of All Time
    loatSt -- an accumulator of index of the LOAT sublist
    prices -- the sequence of prices

    Return:
    a tuple of the length of the longest nondecreasing sequence,
    the start day, and the longest nondecreasing sublist
    """

    # Base Case: If we've traversed the whole list, return the solution
    if start+1 >= len(prices):
        # note the conversion of loatSt to one-indexing
        return (loat, loatSt+1, prices[loatSt : loat + loatSt])

    # Start with the solo element at prices[start] in the sequence
    # between start and end
    curLen = 1    
    end = start + curLen

    # until we finish the list or find a decreasing element, grow the sublist
    while (end < len(prices)) and prices[end-1] <= prices[end]:
        curLen += 1
        end += 1

    # if we've found a longer sublist update the accumulators
    # otherwise continue the iteration with loat and loatSt
    if curLen >= loat:
        return nondecreasing(end, curLen, start, prices)
    else:
        return nondecreasing(end, loat, loatSt, prices)
        

# execute if called    
if __name__ == "__main__" : main()
