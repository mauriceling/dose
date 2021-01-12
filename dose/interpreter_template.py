'''
Template for New Genomic Interpreter
Date created: 12th January 2021

The interpreter environment consists of the following elements:

    1. Array/Tape: A circular tape initialized with 30 thousand cells 
    each with zero. This can be visualized as a 30,000 cell register 
    machine. The number of cells can increase or decrease during runtime.
    2. Source: The program
    3. Input List: A list of data given to the execution environment at 
    initialization.
    4. Output List: A list of output from the execution. This may also be 
    used as a secondary tape. 

When the program terminates, 4 elements (Array, Source, Input List and 
Output List) are returned, and the interpreter terminates itself. 
'''
codonLength = 3

interpreter = {'AAA': interpret_codon, 'AAT': interpret_codon}

def interpret_codon(array, apointer, inputdata, output, source, spointer):
    '''
    Boiler plate to interpret codon.
    '''
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'xxx': pass
    return (array, apointer, inputdata, output, source, spointer)
