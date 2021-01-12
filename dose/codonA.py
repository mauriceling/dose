'''
Codon A Genome Interpreter
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

stackA = []
stackB = []

def push(x, stack):
    if stack.upper() == "A":
        stackA.append(x)
        return stackA
    elif stack.upper() == "B":
        stackB.append(x)
        return stackB

def pop(stack):
    if stack.upper() == "A":
        try: x = stackA.pop()
        except IndexError: x = 0
        return (x, stackA)
    elif stack.upper() == "B":
        try: x = stackB.pop()
        except IndexError: x = 0
        return (x, stackB)



def accumulator(array, apointer, inputdata, output, source, spointer):
    '''
    Boiler plate to interpret codon.
    '''
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'ATG': pass
    if cmd == 'TGG': pass
    if cmd == 'ATT':
        i = random.randint(0, 3)
        array[i] = array[i] + 1
    if cmd == 'ATC':
        i = random.randint(0, 3)
        array[i] = array[i] + 1
    if cmd == 'ATA':
        i = random.randint(0, 3)
        array[i] = array[i] + 1
    if cmd == 'CCT': array[0] = array[0] - 1
    if cmd == 'CCC': array[1] = array[1] - 1
    if cmd == 'CCA': array[2] = array[2] - 1
    if cmd == 'CCG': array[3] = array[3] - 1
    if cmd == 'GGT': array[0] = array[0] + 1
    if cmd == 'GGC': array[1] = array[1] + 1
    if cmd == 'GGA': array[2] = array[2] + 1
    if cmd == 'GGG': array[3] = array[3] + 1
    if cmd == 'GAA': array[1] = array[2] - array[3]
    if cmd == 'GAG': array[3] = array[0] - array[1]
    if cmd == 'AGA': array[1] = array[2] + array[3]
    if cmd == 'CGT': array[0] = array[0] + array[1]
    if cmd == 'CGC': array[2] = array[2] + array[3]
    if cmd == 'CGA': array[0] = array[0] - array[1]
    if cmd == 'CGG': array[2] = array[2] - array[3]
    if cmd == 'TAA': 
        array[0] = 0
        array[1] = 0
    if cmd == 'TAG': 
        array[2] = 0
        array[3] = 0
    if cmd == 'TGA': 
        array[0] = 0
        array[1] = 0
        array[2] = 0
        array[3] = 0
    if cmd == 'AAT' and array[2] > array[3]: array[1] = array[0] - array[1]
    if cmd == 'AAC' and array[0] > array[1]: array[3] = array[2] - array[3]
    if cmd == 'AAA' and array[2] > array[3]: array[1] = array[0] + array[1]
    if cmd == 'AAC' and array[0] > array[1]: array[3] = array[2] + array[3]
    return (array, apointer, inputdata, output, source, spointer)

def swap(array, apointer, inputdata, output, source, spointer):
    '''
    Boiler plate to interpret codon.
    '''
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'CAT': array[0], array[1] = array[1], array[0]
    if cmd == 'CAC': array[2], array[3] = array[3], array[2]
    if cmd == 'CAA': array[0], array[2] = array[2], array[0]
    if cmd == 'CAG': array[1], array[3] = array[3], array[1]
    if cmd == 'TGT' and array[2] > array[3]: array[0], array[1] = array[1], array[0]
    if cmd == 'TGC' and array[0] > array[1]: array[2], array[3] = array[3], array[2]
    if cmd == 'GCT': array[1] = max(array[0], array[1])
    if cmd == 'GCC': array[3] = min(array[2], array[3])
    if cmd == 'GCA': array[1] = max(array[0], array[1])
    if cmd == 'GCG': array[3] = min(array[2], array[3])
    if cmd == 'ATG': 
        x = max(array[0], array[1], array[2], array[3])
        array[0], array[1], array[2], array[3] = x, x, x, x
    if cmd == 'TGG': 
        x = min(array[0], array[1], array[2], array[3])
        array[0], array[1], array[2], array[3] = x, x, x, x
    return (array, apointer, inputdata, output, source, spointer)

def inputOp(array, apointer, inputdata, output, source, spointer):
    '''
    Boiler plate to interpret codon.
    '''
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'CTT': array[0] = array[0] + inputdata[0]
    if cmd == 'CTC': array[1] = array[1] + inputdata[1]
    if cmd == 'CTA': array[2] = array[2] + inputdata[2]
    if cmd == 'CTG': array[3] = array[3] + inputdata[3] 
    if cmd == 'TAT': stackA = push(inputdata[0] + inputdata[1], "A")
    if cmd == 'TAC': stackB = push(inputdata[2] + inputdata[3], "B")   
    return (array, apointer, inputdata, output, source, spointer)

def outputOp(array, apointer, inputdata, output, source, spointer):
    '''
    Boiler plate to interpret codon.
    '''
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'TCT': ouput[0] = ouput[0] + array[0]
    if cmd == 'TCC': ouput[1] = ouput[1] + array[1]
    if cmd == 'TCA': ouput[2] = ouput[2] + array[2]
    if cmd == 'TCG': ouput[3] = ouput[3] + array[3]
    if cmd == 'AGT':
        (x, stackA) = pop("A")
        output[0] = x
        (x, stackA) = pop("A")
        output[1] = x
    if cmd == 'AGC':
        (x, stackB) = pop("B")
        output[2] = x
        (x, stackB) = pop("B")
        output[3] = x
    if cmd == 'GAT':
        (x, stackA) = pop("A")
        output[0] = x
        output[1] = x
    if cmd == 'GAC':
        (x, stackB) = pop("B")
        output[2] = x
        output[3] = x
    return (array, apointer, inputdata, output, source, spointer)

def stack(array, apointer, inputdata, output, source, spointer):
    '''
    Boiler plate to interpret codon.
    '''
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'TTT': 
        (x, stackA) = pop("A")
        stackB = push(x, "B")
    if cmd == 'TTC': 
        (x, stackB) = pop("B")
        stackA = push(x, "A")
    if cmd == 'TTA':
        stackA = push(inputdata[0], "A")
        stackA = push(inputdata[1], "A")
    if cmd == 'TTG':
        stackB = push(inputdata[2], "B")
        stackB = push(inputdata[3], "B")
    if cmd == 'GTT': stackA = push(array[0], "A")
    if cmd == 'GTC': stackA = push(array[1], "A")
    if cmd == 'GTA': stackB = push(array[2], "B")
    if cmd == 'GTG': stackB = push(array[3], "B")
    if cmd == 'ACT': 
        (x, stackA) = pop("A")
        array[0] = x
    if cmd == 'ACC': 
        (x, stackA) = pop("A")
        array[1] = x
    if cmd == 'ACA': 
        (x, stackB) = pop("B")
        array[2] = x
    if cmd == 'ACG': 
        (x, stackB) = pop("B")
        array[3] = x
    return (array, apointer, inputdata, output, source, spointer)

interpreter = {'TTT': stack, 'TTC': stack,
               'TTA': stack, 'TTG': stack,
               'CTT': inputOp, 'CTC': inputOp,
               'CTA': inputOp, 'CTG': inputOp,
               'ATT': accumulator, 'ATC': accumulator,
               'ATA': accumulator, 'ATG': swap,
               'GTT': stack, 'GTC': stack,
               'GTA': stack, 'GTG': stack,
               'TGG': swap, 'TCT': outputOp,
               'TCC': outputOp, 'TCA': outputOp,
               'TCG': outputOp, 'AGT': outputOp,
               'AGC': outputOp, 'CCT': accumulator,
               'CCC': accumulator, 'CCA': accumulator,
               'CCG': accumulator, 'ACT': stack,
               'ACC': stack, 'ACA': stack,
               'ACG': stack, 'GCT': swap,
               'GCC': swap, 'GCA': swap,
               'GCG': swap, 'TAT': inputOp,
               'TAC': inputOp, 'TAA': accumulator,
               'TAG': accumulator, 'TGA': accumulator,
               'CAT': swap, 'CAC': swap,
               'CAA': swap, 'CAG': swap,
               'AAT': accumulator, 'AAC': accumulator,
               'AAA': accumulator, 'AAG': accumulator,
               'GAT': outputOp, 'GAC': outputOp,
               'GAA': accumulator, 'GAG': accumulator,
               'TGT': swap, 'TGC': swap,
               'CGT': accumulator, 'CGC': accumulator,
               'CGA': accumulator, 'CGG': accumulator,
               'AGA': accumulator, 'AGG': accumulator,
               'GGT': accumulator, 'GGC': accumulator,
               'GGA': accumulator, 'GGG': accumulator}
               