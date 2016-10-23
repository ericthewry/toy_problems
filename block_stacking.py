#! /usr/bin/python2

# This file contains the solution to a simple block stacking
# problem. This should run on python2.7.

import argparse
import math
import itertools

WIDTH = 0
LENGTH = 1
HEIGHT = 2

def main():
    # parse the input
    parser = argparse.ArgumentParser(description="An algorithm for the block stacking problem")
    parser.add_argument("infile",  help="The file containing the length of the input and the input")
    parser.add_argument("outfile", help="The file to which the output should be written")
    args = parser.parse_args()

    # inlist contains the lines of the input file
    inlist = []
    # read the file
    with open(args.infile) as f:
        inlist = [x.strip('\n') for x in f.readlines()]

    # Transform list of strings to list of tuples
    blocklist = [tuple([int(ch) for ch in x.split() if ch.isdigit()]) for x in inlist[1:]]

    # collect solution
    (height, stk) = stack_blocks(blocklist)

    # Print solution information
    print "The tallest tower has", len(stk), "blocks and a height of", height

    # write out data    
    outdata = [len(stk)]
    for b in stk:
        outdata.append(stringify(b))
    
    # open the destination file and write to it
    with open(args.outfile, "r+") as f:
        # empty file
        f.seek(0)
        f.truncate()
        
        # write to file
        for line in outdata:
            f.write(str(line) + "\n")

def stringify(blk):
    """
    Transform a tuple into a space-separated string

    Params: blk - a tuple (esp. a triple of width, length and height)
    Return: the space-separated string of blk
    """
    return " ".join([str(x) for x in blk])
        
def surface_area(blk):
    """
    Calculate the surface area of a block
    Params: blk - a tuple of width, length and height
    Return: the surface area of the first two dimensions
    """
    return(blk[WIDTH] * blk[LENGTH])


def can_add(blck, nextblck):
    """
    Determine if a block can be placed on top of another
    Params: 
        blck     - a tuple representing the dimension of the bottom block
        nextblck - a tuple representing the dimension of the potential block to
                   be added
    Return:
        True if can place nextblck on top of blck
    """
    return blck[WIDTH] > nextblck[WIDTH] and blck[LENGTH] > nextblck[LENGTH]
            
            
def normalize(blocks):
    """
    Sort the unique permutations with width greater than length by surface area

    Params: blocks a list of tuples representing the dimensions of the blocks
    Return: the precomputed list of tuples
    """
    # find all unique permutations
    blocks_temp = set(sum([list(itertools.permutations(b)) for b in blocks],[]))
    # remove blocks where the width is strictly smaller than the length
    blocks_temp = [blk for blk in blocks_temp if blk[WIDTH] >= blk[LENGTH]]
    # sort the remaining blocks by decreasing surface area.
    blocks_temp = sorted(blocks_temp, key = surface_area, reverse=True)
    
    return(blocks_temp)
        
            
def stack_blocks(blocks):
    """
    Calculate the tallest stacking of blocks.

    Params: blocks - a list of dimensions representing types of blocks
    Return: a tuple of the best height and a list of the blocks used (in order)
    """
    # perform precomputation
    blocks = normalize(blocks)
    # zero-initialize
    table = list(itertools.repeat(0,len(blocks)))
    soln = list(range(0,len(blocks)))

    # perform calculation
    fill_table(table, blocks, soln)
    
    # get and return the solution
    return(get_soln(table,blocks,soln))


def fill_table(table, blocks, soln):
    """
    Fill the dynamic programming table and the solution list
    Params:
      table  - the DP table to be filled
      blocks - the blocks to be used 
      soln   - the solution table to be filled
    """
    for i,b in enumerate(blocks):
        stack(table,blocks,soln,i)
            
def stack(table, blocks, soln, idx):
    """
    Params:
       table  -- the dp table containing the best heights so far
       blocks -- sorted array of block templates
       soln   -- array in which the ith index holds the index of the block on which
                 the ith block rests in the best case
       idx    -- the index of the current block under consideration
    """
    table[idx] = blocks[idx][HEIGHT]   # set the current height to be the initial goat

    # iterate through previous blocks
    for i,prev in enumerate(blocks[:idx]):
        # check if we can add it
        if can_add(prev, blocks[idx]):
            # calculate potential height
            ht = blocks[idx][HEIGHT] + table[i]
            # if the height is better make it the new goat
            if(ht > table[idx]):
                table[idx] = ht
                soln[idx] = i


def get_soln(table, blocks, soln):
    """
    Recover the optimal solution from the fille table and soltion
    Params:
      table  - the DP table 
      blocks - the blocks
      soln   - the solution list where the ith index contains the 
               index to the block on which the ith block is stacked
               in the optimal solution
    Return 
       a tuple of the height and the list of dimensions used.
    """
    height = max(table)
    idx = table.index(height)
    blocks_used = [blocks[idx]]

    # iterate untill fixpoint is found.
    while(soln[idx] != idx):
        idx = soln[idx]
        blocks_used.append(blocks[idx])

    blocks_used.reverse() # reverse the list to be in the right order
    
    return(height, blocks_used)



                
# execute if called    
if __name__ == "__main__" : main()
