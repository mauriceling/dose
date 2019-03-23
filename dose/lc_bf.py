'''
Loose Circular Brainfuck (LCBF) Interpreter
Date created: 15th August 2012

LCBF uses all 8 operations in standard Brainfuck with the 
following differences:
    1. The tape or array is circular (a ring list) instead of 
    linear. When the pointer is at the "end" of the tape, an 
    increment (">") will move the tape to the start. Similarly, 
    when the pointer is decremented at the "beginning" of the 
    tape, the pointer goes to the end.
    2. Operations after a start loop operator ("[") will only be 
    executed provided the loop(s) are properly closed. If the 
    loops are open, the program will terminate.
    3. However, it is possible to have an end loop operator ("]") 
    without a preceding start loop operator ("["). In this case, 
    the end loop operator ("]") will be ignored and execution continues.
    4. Unclosed or unopened loops may result in non-deterministic 
    behaviour.
    5. All inputs are pre-defined at the start of the program.
    
@see: http://esolangs.org/wiki/Loose_Circular_Brainfuck_(LCBF)
'''

import register_machine as r

def increment(array, apointer, inputdata, output, source, spointer):
    '''
    Increase value of cell by 1. Equivalent to "+" in Brainfuck.
    '''
    array[apointer] = array[apointer] + 1
    return (array, apointer, inputdata, output, source, spointer)

def decrement(array, apointer, inputdata, output, source, spointer):
    '''
    Decrease value of cell by 1. Equivalent to "-" in Brainfuck.
    '''
    array[apointer] = array[apointer] - 1
    return (array, apointer, inputdata, output, source, spointer)

def forward(array, apointer, inputdata, output, source, spointer):
    '''
    Move forward by one cell on tape. Equivalent to ">" in Brainfuck.
    '''
    return (array, apointer + 1, inputdata, output, source, spointer)

def backward(array, apointer, inputdata, output, source, spointer):
    '''
    Move backward by one cell on tape. Equivalent to "<" in Brainfuck.
    '''
    return (array, apointer - 1, inputdata, output, source, spointer)

def call_out(array, apointer, inputdata, output, source, spointer):
    '''
    Output current tape cell value and append to the end of the 
    output list. Equivalent to "." in Brainfuck.
    '''
    output.append(array[apointer])
    return (array, apointer, inputdata, output, source, spointer)

def accept_predefined(array, apointer, inputdata, output, source, spointer):
    '''
    Writes the first value of the input list into the current cell and 
    remove the value from the input list. If input list is empty, "0" 
    will be written
    '''
    if len(inputdata) > 0: array[apointer] = inputdata.pop(0)
    else: array[apointer] = 0
    return (array, apointer, inputdata, output, source, spointer)

def cbf_start_loop(array, apointer, inputdata, output, source, spointer):
    '''
    Start loop. Operations after a start loop operator ("[") will only 
    be executed provided the loop(s) are properly closed. If the loops 
    are open, the program will terminate. Note that unclosed or unopened 
    loops may result in non-deterministic behaviour. 
    '''
    if array[apointer] > 0:
        return (array, apointer, inputdata, output, source, spointer)
    else:
        count = 1
        try:
            while count > 0:
                spointer = spointer + 1
                if source[spointer] == ']':
                    count = count - 1
                if source[spointer] == '[':
                    count = count + 1
        except IndexError:
            spointer = len(source) - 1
    return (array, apointer, inputdata, output, source, spointer)

def cbf_end_loop(array, apointer, inputdata, output, source, spointer):
    '''
    End loop. However, it is possible to have an end loop operator 
    ("]") without a preceding start loop operator ("["). In this case, 
    the end loop operator ("]") will be ignored and execution continues. 
    Note that unclosed or unopened loops may result in non-deterministic 
    behaviour. 
    '''
    temp = spointer
    if array[apointer] < 1:
        return (array, apointer, inputdata, output, source, spointer + 1)
    else:
        count = 1
        try:
            while count > 0:
                spointer = spointer - 1
                if source[spointer] == ']':
                    count = count + 1
                if source[spointer] == '[':
                    count = count - 1
        except IndexError:
            spointer = temp
    return (array, apointer, inputdata, output, source, spointer)

LCBF = {'+': increment,
        '-': decrement,
        '>': forward,
        '<': backward,
        '.': call_out,
        ',': accept_predefined,
        '[': cbf_start_loop,
        ']': cbf_end_loop,
        }

if __name__ == '__main__':
    print(r.interpret('++++++++++[>+++++<.-]', LCBF))
    print(r.interpret('++[>+++++<.-]>>>+++.', LCBF))
    print(r.interpret('++>+++++<.-]>>>+++.', LCBF))
    print(r.interpret('++>[+++++<.->>>+++.', LCBF))
    print(r.interpret('+++++[>++++[>+++.<-].<-]', LCBF))
    print(r.interpret('>>>>>>++', LCBF, 1, [], None, 5))
