'''
One dimensional tape/register machine
Date created: 15th August 2012

The machine consists of the following elements:
    1. Array/Tape: A circular tape for operations to occur
    2. Source: The program
    3. Input List: A list of data given to the machine at initialization.
    4. Output List: A list of output from the execution. This may also be 
    used as a secondary tape. 

When the program terminates, all 4 elements are returned, and the 
machine terminates itself. 
'''

def interpret(source, functions,
             function_size=1, inputdata=[],
             array=None, size=30, max_instructions=1000):
    '''
    Interpreter loop.
    
    @param source: Instructions to execute.
    @type source: string
    @param functions: Dictionary of functions / operations.
    @param function_size: Length of each instruction. Default = 1
    @type function_size: integer
    @param inputdata: Any input data that the function may need.
    @type inputdata: list
    @param array: The endless tape in a Turing machine which is implemented
    as a circular list, making it virtually limitless.
    @type array: list
    @param size: Length of the type (array). Default = 30
    @type size: integer
    @param max_instructions: The maximum number of instructions to execute. 
    Default = 1000
    @type max_instructions: integer
    '''
    spointer = 0
    apointer = 0
    output = list()
    if array == None:
        array = [0] * size
    if len(array) > size:
        array = array[0:size]
    if len(source) % function_size != 0:
        source = source + '!'*(function_size - \
                               len(source) % function_size)
	tokens = functions.keys()
	source = ''.join([x for x in source if x in tokens])
    instruction_count = 0
    while spointer < len(source):
        instruction_count = instruction_count + 1
        
        try:
            cmd = source[spointer:spointer+function_size]
            #print instruction_count, cmd
            (array, apointer, inputdata, output,
                source, spointer) = functions[cmd](array, apointer,
                                                   inputdata, output,
                                                   source, spointer)
        except KeyError:
            print(' '.join(['Unknown function: ', cmd,
                            'at source position', str(spointer)]))
        if apointer > size - 1:
            apointer = apointer - size
        if apointer < 0:
            apointer = size + apointer
        spointer = spointer + function_size
        if instruction_count > max_instructions:
            return (array, apointer, inputdata, output, source, spointer)
    return (array, apointer, inputdata, output, source, spointer)
