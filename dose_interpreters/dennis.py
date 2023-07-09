'''
Dennis Genomic Interpreter
Date created: 25th January 2021

The interpreter environment consists of the following elements:

    1. Array/Tape: A circular tape initialized with 25 cells representing 
    25 metabolites.
    2. Source: The program, representing the genome
    3. Input List: A list of data given to the execution environment at 
    initialization.
    4. Output List: A list of output from the execution. This may also be 
    used as a secondary tape. 

When the program terminates, 4 elements (Array, Source, Input List and 
Output List) are returned, and the interpreter terminates itself. 
'''
codonLength = 2


def interpret_codon(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    if cmd == '01': 
        # R1: 1 + 24 => 4 + 22
        min_M = min(array[1], array[24])
        array[4], array[22] = min_M, minM
        array[1] = array[1] - min_M
        array[24] = array[24] - min_M
    if cmd == '02': 
        # R2: 2 + 16 => 17 + 3
        min_M = min(array[2], array[16])
        array[17], array[3] = min_M, minM
        array[2] = array[2] - min_M
        array[16] = array[16] - min_M
    if cmd == '03': 
        # R3: 2 + 3 => 13 + 6
        min_M = min(array[2], array[3])
        array[13], array[6] = min_M, min_M
        array[2] = array[2] - min_M
        array[3] = array[3] - min_M
    if cmd == '04': 
        # R4: 2 + 22 => 18 + 11
        min_M = min(array[2], array[22])
        array[18], array[11] = min_M, min_M
        array[2] = array[2] - min_M
        array[22] = array[22] - min_M
    if cmd == '05': 
        # R5: 2 + 20 => 6 + 12
        min_M = min(array[2], array[20])
        array[6], array[12] = min_M, min_M
        array[2] = array[2] - min_M
        array[20] = array[20] - min_M
    if cmd == '06': 
        # R6: 2 + 21 => 4 + 15
        min_M = min(array[2], array[21])
        array[4], array[15] = min_M, min_M
        array[2] = array[2] - min_M
        array[21] = array[21] - min_M
    if cmd == '07': 
        # R7: 2 + 1 => 12 + 23
        min_M = min(array[2], array[1])
        array[12], array[23] = min_M, min_M
        array[2] = array[2] - min_M
        array[1] = array[1] - min_M
    if cmd == '08': 
        # R8: 5 + 15 => 4 + 1
        min_M = min(array[5], array[15])
        array[4], array[1] = min_M, min_M
        array[5] = array[5] - min_M
        array[15] = array[15] - min_M
    if cmd == '09': 
        # R9: 6 + 12 => 13 + 10
        min_M = min(array[6], array[12])
        array[13], array[10] = min_M, min_M
        array[6] = array[6] - min_M
        array[12] = array[12] - min_M
    if cmd == '10': 
        # R10: 9 + 18 => 4 + 12
        min_M = min(array[9], array[18])
        array[4], array[12] = min_M, min_M
        array[9] = array[9] - min_M
        array[18] = array[18] - min_M
    if cmd == '11': 
        # R11: 10 + 3 => 22 + 11
        min_M = min(array[10], array[3])
        array[22], array[11] = min_M, min_M
        array[10] = array[10] - min_M
        array[3] = array[3] - min_M
    if cmd == '12': 
        # R12: 10 + 5 => 6 + 12
        min_M = min(array[10], array[5])
        array[6], array[12] = min_M, min_M
        array[6] = array[6] - min_M
        array[12] = array[12] - min_M
    if cmd == '13': 
        # R13: 10 + 11 => 4 + 22
        min_M = min(array[10], array[11])
        array[4], array[22] = min_M, min_M
        array[10] = array[10] - min_M
        array[11] = array[11] - min_M
    if cmd == '14': 
        # R14: 11  +   12  =>   4   +   13
        min_M = min(array[11], array[12])
        array[4], array[13] = min_M, min_M
        array[11] = array[11] - min_M
        array[12] = array[12] - min_M
    if cmd == '15': 
        # R15: 11  +   7   =>   9   +   13
        min_M = min(array[11], array[17])
        array[9], array[13] = min_M, min_M
        array[11] = array[11] - min_M
        array[7] = array[7] - min_M
    if cmd == '16': 
        # R16: 12  +   18  =>   7   +   19
        min_M = min(array[12], array[18])
        array[7], array[19] = min_M, min_M
        array[12] = array[12] - min_M
        array[18] = array[18] - min_M
    if cmd == '17': 
        # R17: 12  +   8   =>   0   +   22
        min_M = min(array[12], array[8])
        array[0], array[22] = min_M, min_M
        array[12] = array[12] - min_M
        array[8] = array[8] - min_M
    if cmd == '18': 
        # R18: 14  +   17  =>   22  +   5
        min_M = min(array[14], array[17])
        array[22], array[5] = min_M, min_M
        array[14] = array[14] - min_M
        array[17] = array[17] - min_M
    if cmd == '19': 
        # R19: 14  +   8   =>   9   +   12
        min_M = min(array[14], array[9])
        array[9], array[12] = min_M, min_M
        array[14] = array[14] - min_M
        array[8] = array[8] - min_M
    if cmd == '20': 
        # R20: 14  +   2   =>   23  +   24
        min_M = min(array[14], array[2])
        array[23], array[24] = min_M, min_M
        array[14] = array[14] - min_M
        array[2] = array[2] - min_M
    if cmd == '21': 
        # R21: 16  +   7   =>   9   +   12
        min_M = min(array[16], array[7])
        array[9], array[12] = min_M, min_M
        array[16] = array[16] - min_M
        array[7] = array[7] - min_M
    if cmd == '22': 
        # R22: 17  +   23  =>   4   +   24
        min_M = min(array[17], array[23])
        array[4], array[24] = min_M, min_M
        array[17] = array[17] - min_M
        array[23] = array[23] - min_M
    if cmd == '23': 
        # R23: 18  +   23  =>   10  +   1
        min_M = min(array[18], array[23])
        array[10], array[1] = min_M, min_M
        array[18] = array[18] - min_M
        array[23] = array[23] - min_M
    if cmd == '24': 
        # R24: 19  +   5   =>   23  +   0
        min_M = min(array[19], array[5])
        array[23], array[0] = min_M, min_M
        array[19] = array[19] - min_M
        array[5] = array[5] - min_M
    if cmd == '25': 
        # R25: 19  +   20  =>   4   +   10
        min_M = min(array[19], array[20])
        array[4], array[10] = min_M, min_M
        array[19] = array[19] - min_M
        array[20] = array[20] - min_M
    if cmd == '26': 
        # R26: 20  +   6   =>   9   +   1
        min_M = min(array[20], array[6])
        array[9], array[1] = min_M, min_M
        array[20] = array[10] - min_M
        array[6] = array[6] - min_M
    if cmd == '27': 
        # R27: 20  +   5   =>   17  +   12
        min_M = min(array[20], array[5])
        array[17], array[12] = min_M, min_M
        array[20] = array[20] - min_M
        array[5] = array[5] - min_M
    if cmd == '28': 
        # R28: 12  +   18  =>   4   +   17
        min_M = min(array[12], array[18])
        array[4], array[17] = min_M, min_M
        array[12] = array[12] - min_M
        array[18] = array[18] - min_M
    if cmd == '29': 
        # R29: 21  +   10  =>   18  +   5
        min_M = min(array[21], array[10])
        array[18], array[5] = min_M, min_M
        array[21] = array[21] - min_M
        array[10] = array[10] - min_M
    if cmd == '30': 
        # R30: 21  +   23  =>   4   +   5
        min_M = min(array[21], array[23])
        array[4], array[5] = min_M, min_M
        array[21] = array[21] - min_M
        array[23] = array[23] - min_M
    if cmd == '31': 
        # R31: 22  +   17  =>   9   +   18
        min_M = min(array[22], array[17])
        array[9], array[18] = min_M, min_M
        array[22] = array[22] - min_M
        array[17] = array[17] - min_M
    if cmd == '32': 
        # R32: 22  +   1   =>   24  +   20
        min_M = min(array[22], array[1])
        array[24], array[20] = min_M, min_M
        array[22] = array[22] - min_M
        array[1] = array[1] - min_M
    if cmd == '33': 
        # R33: 24  +   16  =>   15  +   0
        min_M = min(array[24], array[16])
        array[15], array[0] = min_M, min_M
        array[24] = array[24] - min_M
        array[16] = array[16] - min_M
    if cmd == '34': 
        # R34: 24  +   15  =>   1   +   13
        min_M = min(array[24], array[15])
        array[1], array[13] = min_M, min_M
        array[24] = array[24] - min_M
        array[15] = array[15] - min_M
    if cmd == '35': 
        # R35: 24  +   5   =>   1   +   17
        min_M = min(array[24], array[5])
        array[1], array[17] = min_M, min_M
        array[24] = array[24] - min_M
        array[5] = array[5] - min_M
    if cmd == '36': 
        # R36: eO2 =>  14 + eO2
        array[14] = array[14] + inputdata[0]
    if cmd == '37': 
        # R37: eC => 2 + eC
        array[2] = array[2] + inputdata[1]
    return (array, apointer, inputdata, output, source, spointer)

interpreter = {'01': interpret_codon, '02': interpret_codon,
               '03': interpret_codon, '04': interpret_codon, 
               '05': interpret_codon, '06': interpret_codon, 
               '07': interpret_codon, '08': interpret_codon, 
               '09': interpret_codon, '10': interpret_codon, 
               '11': interpret_codon, '12': interpret_codon, 
               '13': interpret_codon, '14': interpret_codon, 
               '15': interpret_codon, '16': interpret_codon, 
               '17': interpret_codon, '18': interpret_codon, 
               '19': interpret_codon, '20': interpret_codon, 
               '21': interpret_codon, '22': interpret_codon, 
               '23': interpret_codon, '24': interpret_codon, 
               '25': interpret_codon, '26': interpret_codon, 
               '27': interpret_codon, '28': interpret_codon, 
               '29': interpret_codon, '30': interpret_codon, 
               '31': interpret_codon, '32': interpret_codon, 
               '33': interpret_codon, '34': interpret_codon, 
               '35': interpret_codon, '36': interpret_codon,
               '37': interpret_codon}
