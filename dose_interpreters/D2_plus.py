'''
D2+ Interpreter - An Improved Version of D2 Interpreter
Date created: 24th May 2023

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
p = 1e-9    # proportion of DO size to ecological cell
codonLength = 2


def null_codon(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    if cmd == '00': pass
    return (array, apointer, inputdata, output, source, spointer)

def undefined_codon(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    if cmd in ['71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']: pass
    return (array, apointer, inputdata, output, source, spointer)

def interpret_codon(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    if cmd == '00': pass
    if cmd == '01': 
        # R1: 1 + 24 => 4 + 22
        min_M = min(array[1], array[24])
        array[1], array[24] = array[1] - min_M, array[24] - min_M
        array[4], array[22] = array[4] + min_M, array[22] + minM
    if cmd == '02': 
        # R2: 2 + 16 => 3 + 17
        min_M = min(array[2], array[16])
        array[2], array[16] = array[2] - min_M, array[16] - min_M
        array[3], array[17] = array[3] + min_M, array[17] + minM
    if cmd == '03': 
        # R3: 2 + 3 => 6 + 13
        min_M = min(array[2], array[3])
        array[2], array[3] = array[2] - min_M, array[3] - min_M
        array[6], array[13] = array[6] + min_M, array[13] + min_M
    if cmd == '04': 
        # R4: 2 + 22 => 11 + 18
        min_M = min(array[2], array[22])
        array[2], array[22] = array[2] - min_M, array[22] - min_M
        array[11], array[18] = array[11] + min_M, array[18] + min_M
    if cmd == '05': 
        # R5: 2 + 20 => 6 + 12
        min_M = min(array[2], array[20])
        array[2], array[20] = array[2] - min_M, array[20] - min_M
        array[6], array[12] = array[6] + min_M, array[12] + min_M
    if cmd == '06': 
        # R6: 2 + 21 => 4 + 15
        min_M = min(array[2], array[21])
        array[2], array[21] = array[2] - min_M, array[21] - min_M
        array[4], array[15] = array[4] + min_M, array[15] + min_M
    if cmd == '07': 
        # R7: 1 + 2 => 12 + 23
        min_M = min(array[1], array[2])
        array[1], array[2] = array[1] - min_M, array[2] - min_M
        array[12], array[23] = array[12] + min_M, array[23] + min_M
    if cmd == '08': 
        # R8: 5 + 15 => 1 + 4
        min_M = min(array[5], array[15])
        array[5], array[15] = array[5] - min_M, array[15] - min_M
        array[1], array[4] = array[1] + min_M, array[4] + min_M
    if cmd == '09': 
        # R9: 6 + 12 => 10 + 13
        min_M = min(array[6], array[12])
        array[6], array[12] = array[6] - min_M, array[12] - min_M
        array[10], array[13] = array[10] + min_M, array[13] + min_M
    if cmd == '10': 
        # R10: 9 + 18 => 4 + 12
        min_M = min(array[9], array[18])
        array[9], array[18] = array[9] - min_M, array[18] - min_M
        array[4], array[12] = array[4] + min_M, array[12] + min_M
    if cmd == '11': 
        # R11: 3 + 10 => 11 + 22
        min_M = min(array[3], array[10])
        array[3], array[10] = array[3] - min_M, array[10] - min_M
        array[11], array[22] = array[11] + min_M, array[22] + min_M
    if cmd == '12': 
        # R12: 5 + 10 => 6 + 12
        min_M = min(array[5], array[10])
        array[5], array[10] = array[5] - min_M, array[10] - min_M
        array[6], array[12] = array[6] + min_M, array[12] + min_M
    if cmd == '13': 
        # R13: 10 + 11 => 4 + 22
        min_M = min(array[10], array[11])
        array[10], array[11] = array[10] - min_M, array[11] - min_M
        array[4], array[22] = array[4] + min_M, array[22] + min_M
    if cmd == '14': 
        # R14: 11 + 12 => 4 + 13
        min_M = min(array[11], array[12])
        array[11], array[12] = array[11] - min_M, array[12] - min_M
        array[4], array[13] = array[4] + min_M, array[13] + min_M
    if cmd == '15': 
        # R15: 7 + 11 => 9 + 13
        min_M = min(array[7], array[11])
        array[7], array[11] = array[7] - min_M, array[11] - min_M
        array[9], array[13] = array[9] + min_M, array[13] + min_M
    if cmd == '16': 
        # R16: 12 + 18 => 7 + 19
        min_M = min(array[12], array[18])
        array[12], array[18] = array[12] - min_M, array[18] - min_M
        array[7], array[19] = array[7] + min_M, array[19] + min_M
    if cmd == '17': 
        # R17: 8 + 12 => 0 + 22
        min_M = min(array[8], array[12])
        array[8], array[12] = array[8] - min_M, array[12] - min_M
        array[0], array[22] = array[0] + min_M, array[22] + min_M
    if cmd == '18': 
        # R18: 14 + 17 => 5 + 22
        min_M = min(array[14], array[17])
        array[14], array[17] = array[14] - min_M, array[17] - min_M
        array[5], array[22] = array[5] + min_M, array[22] + min_M
    if cmd == '19': 
        # R19: 8 + 14 => 9 + 12
        min_M = min(array[8], array[14])
        array[8], array[14] = array[8] - min_M, array[14] - min_M
        array[9], array[12] = array[9] + min_M, array[12] + min_M
    if cmd == '20': 
        # R20: 2 + 14 => 23 + 24
        min_M = min(array[2], array[14])
        array[2], array[14] = array[2] - min_M, array[14] - min_M
        array[23], array[24] = array[23] + min_M, array[24] + min_M
    if cmd == '21': 
        # R21: 7 + 16 => 9 + 12
        min_M = min(array[7], array[16])
        array[7], array[16] = array[7] - min_M, array[16] - min_M
        array[9], array[12] = array[9] + min_M, array[12] + min_M
    if cmd == '22': 
        # R22: 17 + 23 => 4 + 24
        min_M = min(array[17], array[23])
        array[17], array[23] = array[17] - min_M, array[23] - min_M
        array[4], array[24] = array[4] + min_M, array[24] + min_M
    if cmd == '23': 
        # R23: 18 + 23 => 1 + 10
        min_M = min(array[18], array[23])
        array[18], array[23] = array[18] - min_M, array[23] - min_M
        array[1], array[10] = array[1] + min_M, array[10] + min_M
    if cmd == '24': 
        # R24: 5 + 19 => 0 + 23
        min_M = min(array[5], array[19])
        array[5], array[19] = array[5] - min_M, array[19] - min_M
        array[0], array[23] = array[0] + min_M, array[23] + min_M
    if cmd == '25': 
        # R25: 19 + 20 => 4 + 10
        min_M = min(array[19], array[20])
        array[19], array[20] = array[19] - min_M, array[20] - min_M
        array[4], array[10] = array[4] + min_M, array[10] + min_M
    if cmd == '26': 
        # R26: 6 + 20 => 1 + 9
        min_M = min(array[6], array[20])
        array[6], array[20] = array[6] - min_M, array[20] - min_M
        array[1], array[9] = array[1] + min_M, array[9] + min_M
    if cmd == '27': 
        # R27: 5 + 20 => 12 + 17
        min_M = min(array[5], array[20])
        array[5], array[20] = array[5] - min_M, array[20] - min_M
        array[12], array[17] = array[12] + min_M, array[17] + min_M
    if cmd == '28': 
        # R28: 12 + 18 => 4 + 17
        min_M = min(array[12], array[18])
        array[12], array[18] = array[12] - min_M, array[18] - min_M
        array[4], array[17] = array[4] + min_M, array[17] + min_M
    if cmd == '29': 
        # R29: 10 + 21 => 5 + 18
        min_M = min(array[10], array[21])
        array[10], array[21] = array[10] - min_M, array[21] - min_M
        array[5], array[18] = array[5] + min_M, array[18] + min_M
    if cmd == '30': 
        # R30: 21 + 23 => 4 + 5
        min_M = min(array[21], array[23])
        array[21], array[23] = array[21] - min_M, array[23] - min_M
        array[4], array[5] = array[4] + min_M, array[5] + min_M
    if cmd == '31': 
        # R31: 17 + 22 => 9 + 18
        min_M = min(array[17], array[22])
        array[17], array[22] = array[17] - min_M, array[22] - min_M
        array[9], array[18] = array[9] + min_M, array[18] + min_M
    if cmd == '32': 
        # R32: 1 + 22 => 20 + 24
        min_M = min(array[1], array[22])
        array[1], array[22] = array[1] - min_M, array[22] - min_M
        array[20], array[24] = array[20] + min_M, array[24] + min_M
    if cmd == '33': 
        # R33: 16 + 24 => 0 + 15
        min_M = min(array[16], array[24])
        array[16], array[24] = array[16] - min_M, array[24] - min_M
        array[0], array[15] = array[0] + min_M, array[15] + min_M
    if cmd == '34': 
        # R34: 15 + 24 => 1 + 13
        min_M = min(array[15], array[24])
        array[15], array[24] = array[15] - min_M, array[24] - min_M
        array[1], array[13] = array[1] + min_M, array[13] + min_M
    if cmd == '35': 
        # R35: 5 + 24 => 1 + 17
        min_M = min(array[5], array[24])
        array[5], array[24] = array[5] - min_M, array[24] - min_M
        array[1], array[17] = array[1] + min_M, array[17] + min_M
    if cmd == '36': 
        # R36: eA =>  0 + p * eA
        array[0] = array[0] + (p * inputdata[0])    
    if cmd == '37': 
        # R37: eC => 2 + p * eC
        array[2] = array[2] + (p * inputdata[2]) 
    if cmd == '38': 
        # R38: eE => 4 + p * eE
        array[4] = array[4] + (p * inputdata[4]) 
    if cmd == '39': 
        # R39: eG => 6 + p * eG
        array[6] = array[6] + (p * inputdata[6]) 
    if cmd == '40': 
        # R40: eI => 8 + p * eI
        array[8] = array[8] + (p * inputdata[8]) 
    if cmd == '41': 
        # R41: eK => 10 + p * eK
        array[10] = array[10] + (p * inputdata[10]) 
    if cmd == '42': 
        # R42: eM => 12 + p * eM
        array[12] = array[12] + (p * inputdata[12]) 
    if cmd == '43': 
        # R43: eO => 14 + p * eO
        array[14] = array[14] + (p * inputdata[14]) 
    if cmd == '44': 
        # R44: eQ => 16 + p * eQ
        array[16] = array[16] + (p * inputdata[16]) 
    if cmd == '45': 
        # R45: eS => 18 + p * eS
        array[18] = array[18] + (p * inputdata[18]) 
    if cmd == '46': 
        # R46: eU => 20 + p * eU
        array[20] = array[20] + (p * inputdata[20]) 
    if cmd == '47': 
        # R47: eW => 22 + p * eW
        array[22] = array[22] + (p * inputdata[22]) 
    if cmd == '48': 
        # R48: eY => 24 + p * eY
        array[24] = array[24] + (p * inputdata[24]) 
    if cmd == '49': 
        # R49: 0 ==> 50% of 0
        r = 0.5 * array[0]
        array[0], inputdata[0] = r, inputdata[0] + r
    if cmd == '50': 
        # R50: 1 ==> 50% of 1
        r = 0.5 * array[1]
        array[1], inputdata[1] = r, inputdata[1] + r
    if cmd == '51': 
        # R51: 4 ==> 50% of 4
        r = 0.5 * array[4]
        array[4], inputdata[4] = r, inputdata[4] + r
    if cmd == '52': 
        # R52: 5 ==> 50% of 5
        r = 0.5 * array[5]
        array[5], inputdata[5] = r, inputdata[5] + r
    if cmd == '53': 
        # R53: 8 ==> 50% of 8
        r = 0.5 * array[8]
        array[8], inputdata[8] = r, inputdata[8] + r
    if cmd == '54': 
        # R54: 9 ==> 50% of 9
        r = 0.5 * array[9]
        array[9], inputdata[9] = r, inputdata[9] + r 
    if cmd == '55': 
        # R55: 12 ==> 50% of 12
        r = 0.5 * array[12]
        array[12], inputdata[12] = r, inputdata[12] + r
    if cmd == '56': 
        # R56: 13 ==> 50% of 13
        r = 0.5 * array[13]
        array[13], inputdata[13] = r, inputdata[13] + r
    if cmd == '57': 
        # R57: 16 ==> 50% of 16
        r = 0.5 * array[16]
        array[16], inputdata[16] = r, inputdata[16] + r
    if cmd == '58': 
        # R58: 17 ==> 50% of 17
        r = 0.5 * array[17]
        array[17], inputdata[17] = r, inputdata[17] + r 
    if cmd == '59': 
        # R59: 20 ==> 50% of 20
        r = 0.5 * array[20]
        array[20], inputdata[20] = r, inputdata[20] + r
    if cmd == '60': 
        # R60: 21 ==> 50% of 21
        r = 0.5 * array[21]
        array[21], inputdata[21] = r, inputdata[20] + r
    if cmd == '61': 
        # R61: 0 + 13 => 14 + 21
        min_M = min(array[0], array[13])
        array[0], array[13] = array[0] - min_M, array[13] - min_M
        array[14], array[21] = array[14] + min_M, array[21] + min_M
    if cmd == '62': 
        # R62: 3 + 4 => 8 + 16
        min_M = min(array[3], array[4])
        array[3], array[4] = array[3] - min_M, array[4] - min_M
        array[8], array[16] = array[8] + min_M, array[16] + min_M
    if cmd == '63': 
        # R63: 13 + 19 => 2 + 7
        min_M = min(array[13], array[19])
        array[13], array[19] = array[13] - min_M, array[19] - min_M
        array[2], array[7] = array[2] + min_M, array[7] + min_M
    if cmd == '64': 
        # R64: 4 + 13 => 2 + 19
        min_M = min(array[4], array[13])
        array[4], array[13] = array[4] - min_M, array[13] - min_M
        array[2], array[19] = array[2] + min_M, array[19] + min_M
    if cmd == '65': 
        # R65: 0 + 22 => 3 + 16
        min_M = min(array[0], array[22])
        array[0], array[22] = array[0] - min_M, array[22] - min_M
        array[3], array[16] = array[3] + min_M, array[16] + min_M
    if cmd == '66': 
        # R66: 4 + 17 => 21 + 24
        min_M = min(array[4], array[17])
        array[4], array[17] = array[4] - min_M, array[17] - min_M
        array[21], array[24] = array[21] + min_M, array[24] + min_M
    if cmd == '67': 
        # R67: 1 + 4 => 2 + 20
        min_M = min(array[1], array[4])
        array[1], array[4] = array[1] - min_M, array[4] - min_M
        array[2], array[20] = array[2] + min_M, array[20] + min_M
    if cmd == '68': 
        # R68: 12 + 13 => 14 + 20
        min_M = min(array[12], array[13])
        array[12], array[13] = array[12] - min_M, array[13] - min_M
        array[14], array[20] = array[14] + min_M, array[20] + min_M
    if cmd == '69': 
        # R69: 9 + 22 => 2 + 8
        min_M = min(array[9], array[22])
        array[9], array[22] = array[9] - min_M, array[22] - min_M
        array[2], array[8] = array[2] + min_M, array[8] + min_M
    if cmd == '70': 
        # R70: 6 + 9 => 3 + 19
        min_M = min(array[6], array[9])
        array[6], array[9] = array[6] - min_M, array[9] - min_M
        array[3], array[19] = array[3] + min_M, array[19] + min_M
    return (array, apointer, inputdata, output, source, spointer)

interpreter = \
{'01': interpret_codon, '02': interpret_codon, '03': interpret_codon, 
 '04': interpret_codon, '05': interpret_codon, '06': interpret_codon, 
 '07': interpret_codon, '08': interpret_codon, '09': interpret_codon, 
 '10': interpret_codon, '11': interpret_codon, '12': interpret_codon, 
 '13': interpret_codon, '14': interpret_codon, '15': interpret_codon, 
 '16': interpret_codon, '17': interpret_codon, '18': interpret_codon, 
 '19': interpret_codon, '20': interpret_codon, '21': interpret_codon, 
 '22': interpret_codon, '23': interpret_codon, '24': interpret_codon, 
 '25': interpret_codon, '26': interpret_codon, '27': interpret_codon, 
 '28': interpret_codon, '29': interpret_codon, '30': interpret_codon, 
 '31': interpret_codon, '32': interpret_codon, '33': interpret_codon, 
 '34': interpret_codon, '35': interpret_codon, '36': interpret_codon, 
 '37': interpret_codon, '38': interpret_codon, '39': interpret_codon, 
 '40': interpret_codon, '41': interpret_codon, '42': interpret_codon, 
 '43': interpret_codon, '44': interpret_codon, '45': interpret_codon, 
 '46': interpret_codon, '47': interpret_codon, '48': interpret_codon, 
 '49': interpret_codon, '50': interpret_codon, '51': interpret_codon, 
 '52': interpret_codon, '53': interpret_codon, '54': interpret_codon, 
 '55': interpret_codon, '56': interpret_codon, '57': interpret_codon, 
 '58': interpret_codon, '59': interpret_codon, '60': interpret_codon, 
 '61': interpret_codon, '62': interpret_codon, '63': interpret_codon, 
 '64': interpret_codon, '65': interpret_codon, '66': interpret_codon, 
 '67': interpret_codon, '68': interpret_codon, '69': interpret_codon, 
 '70': interpret_codon,
 '00': null_codon, 
 '71': undefined_codon, '72': undefined_codon, '73': undefined_codon, 
 '74': undefined_codon, '75': undefined_codon, '76': undefined_codon, 
 '77': undefined_codon, '78': undefined_codon, '79': undefined_codon, 
 '80': undefined_codon, '81': undefined_codon, '82': undefined_codon, 
 '83': undefined_codon, '84': undefined_codon, '85': undefined_codon, 
 '86': undefined_codon, '87': undefined_codon, '88': undefined_codon, 
 '89': undefined_codon, '90': undefined_codon, '91': undefined_codon, 
 '92': undefined_codon, '93': undefined_codon, '94': undefined_codon, 
 '95': undefined_codon, '96': undefined_codon, '97': undefined_codon, 
 '98': undefined_codon, '99': undefined_codon}
