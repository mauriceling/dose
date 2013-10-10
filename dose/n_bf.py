'''
NucleotideBF (nBF) Interpreter
Date created: 15th August 2012

NucleotideBF is a derivative of Brainfuck based on IUPAC 
nucleotide code. It uses only 5 of the 8 operations in 
Brainfuck, and there is no loop operations.

The commands for nBF can be divided into 2 classes - 
deterministic operations and random operations. The 
deterministic operations are A (increment, equivalent to '+'), 
T (decrement, equivalent to '-'), C (backward, equivalent to 
'<'), G (forward, equivalent to '>') and '.' (call out).

Based on the same interpreter as Loose Circular Brainfuck (LCBF), 
the tape or array is circular (a ring list) instead of linear. 
When the pointer is at the "end" of the tape, an increment ("A") 
will move the tape to the start. Similarly, when the pointer is 
decremented at the "beginning" of the tape, the pointer goes to 
the end. 

@see: http://esolangs.org/wiki/NucleotideBF_(nBF)
'''

import random
import register_machine as r
from lc_bf import increment, decrement, forward, backward, call_out

def random_op(array, apointer, inputdata, output, source, spointer):
    '''
    Random operations / commands to simulate ambiguous DNA 
    nucleotides. Allowable ambiguous nucleotides are:
    R: Random between A or G
    Y: Random between C or T
    S: Random between G or C
    W: Random between A or T
    K: Random between G or T
    M: Random between A or C
    B: Random between C or G or T
    D: Random between A or G or T
    H: Random between A or C or T
    V: Random between A or C or G
    N: Random between A or T or C or G 
    '''
    r = random.random()
    if source[spointer] == 'R' and r < 0.5:
        return increment(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'R' and r >= 0.5:
        if (apointer + 1) == len(array): 
            return (array, 0, inputdata, output, source, spointer)
        else:
            return forward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'Y' and r < 0.5:
        return decrement(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'Y' and r >= 0.5:
        if apointer == 0: 
            return (array, len(array) - 1, inputdata, output, source, spointer)
        else:
            return backward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'S' and r < 0.5:
        if (apointer + 1) == len(array): 
            return (array, 0, inputdata, output, source, spointer)
        else:
            return forward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'S' and r >= 0.5:
        if apointer == 0:
            return (array, len(array) - 1, inputdata, output, source, spointer)
        else:
            return backward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'W' and r < 0.5:
        return increment(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'W' and r >= 0.5:
        return decrement(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'K' and r < 0.5:
        return decrement(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'K' and r >= 0.5:
        if (apointer + 1) == len(array): 
            return (array, 0, inputdata, output, source, spointer)
        else:
            return forward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'M' and r < 0.5:
        return increment(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'M' and r >= 0.5:
        if apointer == 0: 
            return (array, len(array) - 1, inputdata, output, source, spointer)
        else:
            return backward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'B' and r < 0.33:
        if (apointer + 1) == len(array): 
            return (array, 0, inputdata, output, source, spointer)
        else:
            return forward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'B' and r >= 0.33 and r < 0.67:
        return decrement(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'B' and r >= 0.67:
        if apointer == 0:
            return (array, len(array) - 1, inputdata, output, source, spointer)
        else:
            return backward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'D' and r < 0.33:
        return increment(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'D' and r >= 0.33 and r < 0.67:
        return decrement(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'D' and r >= 0.67:
        if (apointer + 1) == len(array):
            return (array, 0, inputdata, output, source, spointer)
        else:
            return forward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'H' and r < 0.33:
        return increment(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'H' and r >= 0.33 and r < 0.67:
        return decrement(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'H' and r >= 0.67:
        if apointer == 0:
            return (array, len(array) - 1, inputdata, output, source, spointer)
        else:
            return backward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'V' and r < 0.33:
        return increment(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'V' and r >= 0.33 and r < 0.67:
        if (apointer + 1) == len(array):
            return (array, 0, inputdata, output, source, spointer)
        else:
            return forward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'V' and r >= 0.67:
        if apointer == 0:
            return (array, len(array) - 1, inputdata, output, source, spointer)
        else:
            return backward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'N' and r < 0.25:
        return increment(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'N' and r >= 0.25 and r < 0.5:
        return decrement(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'N' and r >= 0.5 and r < 0.75:
        if (apointer + 1) == len(array): 
            return (array, 0, inputdata, output, source, spointer)
        else:
            return forward(array, apointer, inputdata, output, source, spointer)
    elif source[spointer] == 'N' and r >= 0.75:
        if apointer == 0:
            return (array, len(array) - 1, inputdata, output, source, spointer)
        else:
            return backward(array, apointer, inputdata, output, source, spointer)


nBF = {'A': increment,
       'T': decrement,
       'G': forward,
       'C': backward,
       'R': random_op,
       'Y': random_op,
       'S': random_op,
       'W': random_op,
       'K': random_op,
       'M': random_op,     
       'B': random_op,
       'D': random_op,
       'H': random_op,
       'V': random_op,
       'N': random_op,
       '.': call_out
       }

if __name__ == '__main__':
    print r.interpret('AAAAGGTTTCAAA', nBF)
    print r.interpret('AAAAGGTTTCAAARRYYSKVDVDBBHVNVH', nBF)
