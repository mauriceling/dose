'''
D3 Interpreter - An Improved Version of D2 Interpreter
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

chromosomeBases1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

chromosomeBases2 = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV', 'BW', 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN', 'CO', 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'DG', 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'EO', 'EP', 'EQ', 'ER', 'ES', 'ET', 'EU', 'EV', 'EW', 'EX', 'EY', 'EZ', 'FA', 'FB', 'FC', 'FD', 'FE', 'FF', 'FG', 'FH', 'GC', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GJ', 'GK', 'GL', 'GM', 'GN', 'GO', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GV', 'GW', 'GX', 'GY', 'GZ', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL', 'HM', 'HN', 'HO', 'HP', 'HQ', 'HR', 'HS', 'HT', 'HU', 'HV', 'HW', 'HX', 'HY', 'HZ', 'IA', 'IB', 'IC', 'ID', 'IE', 'IF', 'IG', 'IH', 'II', 'IJ', 'IK', 'IL', 'IM', 'IN', 'IO', 'IP', 'IQ', 'IR', 'IS', 'IT', 'IU', 'IV', 'IW', 'IX', 'IY', 'IZ', 'JA', 'JB', 'JC', 'JD', 'JE', 'JF', 'JG', 'JH', 'JI', 'JJ', 'JK', 'JL', 'JM', 'JN', 'JO', 'JP', 'JQ', 'JR', 'JS', 'JT', 'JU', 'JV', 'JW', 'JX', 'JY', 'JZ', 'KA', 'KB', 'KC', 'KD', 'KE', 'KF', 'KG', 'KH', 'KI', 'KJ', 'KK', 'KL', 'KM', 'KN', 'KO', 'KP', 'KQ', 'KR', 'KS', 'KT', 'KU', 'KV', 'KW', 'KX', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LD', 'LE', 'LF', 'LG', 'LH', 'LI', 'LJ', 'LK', 'LL', 'LM', 'LN', 'LO', 'LP', 'LQ', 'LR', 'LS', 'LT', 'LU', 'LV', 'LW', 'LX', 'LY', 'LZ', 'MA', 'MB', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MI', 'MJ', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NB', 'NC', 'ND', 'NE', 'NF', 'NG', 'NH', 'NI', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO', 'NP', 'NQ', 'NR', 'NS', 'NT', 'NU', 'NV', 'NW', 'NX', 'NY', 'NZ', 'OA', 'OB', 'OC', 'OD', 'OE', 'OF', 'OG', 'OH', 'OI', 'OJ', 'OK', 'OL', 'OM', 'ON', 'OO', 'OP', 'OQ', 'OR', 'OS', 'OT', 'OU', 'OV', 'OW', 'OX', 'OY', 'OZ', 'PA', 'PB', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI', 'PJ', 'PK', 'PL', 'PM', 'PN', 'PO', 'PP', 'PQ', 'PR', 'PS', 'PT', 'PU', 'PV', 'PW', 'PX', 'PY', 'PZ', 'QA', 'QB', 'QC', 'QD', 'QE', 'QF', 'QG', 'QH', 'QI', 'QJ', 'QK', 'QL', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'QS', 'QT', 'QU', 'QV', 'QW', 'QX', 'QY', 'QZ', 'RA', 'RB', 'RC', 'RD', 'RE', 'RF', 'RG', 'RH', 'RI', 'RJ', 'RK', 'RL', 'RM', 'RN', 'RO', 'RP', 'RQ', 'RR', 'RS', 'RT', 'RU', 'RV', 'RW', 'RX', 'RY', 'RZ', 'SA', 'SB', 'SC', 'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SP', 'SQ', 'SR', 'SS', 'ST', 'SU', 'SV', 'SW', 'SX', 'SY', 'SZ', 'TA', 'TB', 'TC', 'TD', 'TE', 'TF', 'TG', 'TH', 'TI', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TP', 'TQ', 'TR', 'TS', 'TT', 'TU', 'TV', 'TW', 'TX', 'TY', 'TZ', 'UA', 'UB', 'UC', 'UD', 'UE', 'UF', 'UG', 'UH', 'UI', 'UJ', 'UK', 'UL', 'UM', 'UN', 'UO', 'UP', 'UQ', 'UR', 'US', 'UT', 'UU', 'UV', 'UW', 'UX', 'UY', 'UZ', 'VA', 'VB', 'VC', 'VD', 'VE', 'VF', 'VG', 'VH', 'VI', 'VJ', 'VK', 'VL', 'VM', 'VN', 'VO', 'VP', 'VQ', 'VR', 'VS', 'VT', 'VU', 'VV', 'VW', 'VX', 'VY', 'VZ', 'WA', 'WB', 'WC', 'WD', 'WE', 'WF', 'WG', 'WH', 'WI', 'WJ', 'WK', 'WL', 'WM', 'WN', 'WO', 'WP', 'WQ', 'WR', 'WS', 'WT', 'WU', 'WV', 'WW', 'WX', 'WY', 'WZ', 'XA', 'XB', 'XC', 'XD', 'XE', 'XF', 'XG', 'XH', 'XI', 'XJ', 'XK', 'XL', 'XM', 'XN', 'XO', 'XP', 'XQ', 'XR', 'XS', 'XT', 'XU', 'XV', 'XW', 'XX', 'XY', 'XZ', 'YA', 'YB', 'YC', 'YD', 'YE', 'YF', 'YG', 'YH', 'YI', 'YJ', 'YK', 'YL', 'YM', 'YN', 'YO', 'YP', 'YQ', 'YR', 'YS', 'YT', 'YU', 'YV', 'YW', 'YX', 'YY', 'YZ', 'ZA', 'ZB', 'ZC', 'ZD', 'ZE', 'ZF', 'ZG', 'ZH', 'ZI', 'ZJ', 'ZK', 'ZL', 'ZM', 'ZN', 'ZO', 'ZP', 'ZQ', 'ZR', 'ZS', 'ZT', 'ZU', 'ZV', 'ZW', 'ZX', 'ZY', 'ZZ']

def null_codon(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    if cmd == '00': pass
    return (array, apointer, inputdata, output, source, spointer)

def undefined_codon(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    return (array, apointer, inputdata, output, source, spointer)

def interpret_codon(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
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
        # R36: 0 + 13 => 14 + 21
        min_M = min(array[0], array[13])
        array[0], array[13] = array[0] - min_M, array[13] - min_M
        array[14], array[21] = array[14] + min_M, array[21] + min_M
    if cmd == '37': 
        # R37: 3 + 4 => 8 + 16
        min_M = min(array[3], array[4])
        array[3], array[4] = array[3] - min_M, array[4] - min_M
        array[8], array[16] = array[8] + min_M, array[16] + min_M
    if cmd == '38': 
        # R38: 13 + 19 => 2 + 7
        min_M = min(array[13], array[19])
        array[13], array[19] = array[13] - min_M, array[19] - min_M
        array[2], array[7] = array[2] + min_M, array[7] + min_M
    if cmd == '39': 
        # R39: 4 + 13 => 2 + 19
        min_M = min(array[4], array[13])
        array[4], array[13] = array[4] - min_M, array[13] - min_M
        array[2], array[19] = array[2] + min_M, array[19] + min_M
    if cmd == '40': 
        # R40: 0 + 22 => 3 + 16
        min_M = min(array[0], array[22])
        array[0], array[22] = array[0] - min_M, array[22] - min_M
        array[3], array[16] = array[3] + min_M, array[16] + min_M
    if cmd == '41': 
        # R41: 4 + 17 => 21 + 24
        min_M = min(array[4], array[17])
        array[4], array[17] = array[4] - min_M, array[17] - min_M
        array[21], array[24] = array[21] + min_M, array[24] + min_M
    if cmd == '42': 
        # R42: 1 + 4 => 2 + 20
        min_M = min(array[1], array[4])
        array[1], array[4] = array[1] - min_M, array[4] - min_M
        array[2], array[20] = array[2] + min_M, array[20] + min_M
    if cmd == '43': 
        # R43: 12 + 13 => 14 + 20
        min_M = min(array[12], array[13])
        array[12], array[13] = array[12] - min_M, array[13] - min_M
        array[14], array[20] = array[14] + min_M, array[20] + min_M
    if cmd == '44': 
        # R44: 9 + 22 => 2 + 8
        min_M = min(array[9], array[22])
        array[9], array[22] = array[9] - min_M, array[22] - min_M
        array[2], array[8] = array[2] + min_M, array[8] + min_M
    if cmd == '45': 
        # R45: 6 + 9 => 3 + 19
        min_M = min(array[6], array[9])
        array[6], array[9] = array[6] - min_M, array[9] - min_M
        array[3], array[19] = array[3] + min_M, array[19] + min_M
    return (array, apointer, inputdata, output, source, spointer)

def importers(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'AZ': 
        # RAZ: eA =>  0 + p * eA
        array[0] = array[0] + (p * inputdata[0])    
    if cmd == 'BZ': 
        # RBZ: eB => 1 + p * eB
        array[1] = array[1] + (p * inputdata[1]) 
    if cmd == 'CZ': 
        # RCZ: eC => 2 + p * eC
        array[2] = array[2] + (p * inputdata[2]) 
    if cmd == 'DZ': 
        # RDZ: eD => 3 + p * eD
        array[3] = array[3] + (p * inputdata[3]) 
    if cmd == 'EZ': 
        # REZ: eE => 4 + p * eE
        array[4] = array[4] + (p * inputdata[4]) 
    if cmd == 'FZ': 
        # RFZ: eF => 5 + p * eF
        array[5] = array[5] + (p * inputdata[5]) 
    if cmd == 'GZ': 
        # RGZ: eG => 6 + p * eH
        array[6] = array[6] + (p * inputdata[6]) 
    if cmd == 'HZ': 
        # RHZ: eH => 7 + p * eH
        array[7] = array[7] + (p * inputdata[7]) 
    if cmd == 'IZ': 
        # RIZ: eI => 8 + p * eI
        array[8] = array[8] + (p * inputdata[8]) 
    if cmd == 'JZ': 
        # RJZ: eJ => 9 + p * eJ
        array[9] = array[9] + (p * inputdata[9]) 
    if cmd == 'KZ': 
        # RKZ: eK => 10 + p * eK
        array[10] = array[10] + (p * inputdata[10]) 
    if cmd == 'LZ': 
        # RLZ: eL => 11 + p * eL
        array[11] = array[11] + (p * inputdata[11]) 
    if cmd == 'MZ': 
        # RMZ: eM => 12 + p * eM
        array[12] = array[12] + (p * inputdata[12]) 
    if cmd == 'NZ': 
        # RNZ: eN => 13 + p * eN
        array[13] = array[13] + (p * inputdata[13])    
    if cmd == 'OZ': 
        # ROZ: eO => 14 + p * eO
        array[14] = array[14] + (p * inputdata[14]) 
    if cmd == 'PZ': 
        # RPZ: eP => 15 + p * eP
        array[15] = array[15] + (p * inputdata[15]) 
    if cmd == 'QZ': 
        # RQZ: eQ => 16 + p * eQ
        array[16] = array[16] + (p * inputdata[16]) 
    if cmd == 'RZ': 
        # RRZ: eR => 17 + p * eR
        array[17] = array[17] + (p * inputdata[17]) 
    if cmd == 'SZ': 
        # RSZ: eS => 18 + p * eS
        array[18] = array[18] + (p * inputdata[18]) 
    if cmd == 'TZ': 
        # RTZ: eT => 19 + p * eT
        array[19] = array[19] + (p * inputdata[19]) 
    if cmd == 'UZ': 
        # RUZ: eU => 20 + p * eU
        array[20] = array[20] + (p * inputdata[20]) 
    if cmd == 'VZ': 
        # RVZ: eV => 21 + p * eV
        array[21] = array[21] + (p * inputdata[21]) 
    if cmd == 'WZ': 
        # RWZ: eW => 22 + p * eW
        array[22] = array[22] + (p * inputdata[2]) 
    if cmd == 'XZ': 
        # RXZ: eX => 23 + p * eX
        array[23] = array[23] + (p * inputdata[23]) 
    if cmd == 'YZ': 
        # RYZ: eY => 24 + p * eY
        array[24] = array[24] + (p * inputdata[24])
    return (array, apointer, inputdata, output, source, spointer)

def exporters(array, apointer, inputdata, output, source, spointer):
    cmd = source[spointer:spointer+codonLength]
    if cmd == 'ZA': 
        # RZA: 0 ==> 50% of 0
        r = 0.5 * array[0]
        array[0], inputdata[0] = r, inputdata[0] + r
    if cmd == 'ZB': 
        # RZB: 1 ==> 50% of 1
        r = 0.5 * array[1]
        array[1], inputdata[1] = r, inputdata[1] + r
    if cmd == 'ZC': 
        # RZC: 2 ==> 50% of 2
        r = 0.5 * array[2]
        array[2], inputdata[2] = r, inputdata[2] + r
    if cmd == 'ZD': 
        # RZD: 3 ==> 50% of 3
        r = 0.5 * array[3]
        array[3], inputdata[3] = r, inputdata[3] + r
    if cmd == 'ZE': 
        # RZE: 4 ==> 50% of 4
        r = 0.5 * array[4]
        array[4], inputdata[4] = r, inputdata[4] + r
    if cmd == 'ZF': 
        # RZF: 5 ==> 50% of 5
        r = 0.5 * array[5]
        array[5], inputdata[5] = r, inputdata[5] + r 
    if cmd == 'ZG': 
        # RZG: 6 ==> 50% of 6
        r = 0.5 * array[6]
        array[6], inputdata[6] = r, inputdata[6] + r
    if cmd == 'ZH': 
        # RZH: 7 ==> 50% of 7
        r = 0.5 * array[7]
        array[7], inputdata[7] = r, inputdata[7] + r
    if cmd == 'ZI': 
        # RZI: 8 ==> 50% of 8
        r = 0.5 * array[8]
        array[8], inputdata[8] = r, inputdata[8] + r
    if cmd == 'ZJ': 
        # RZJ: 9 ==> 50% of 9
        r = 0.5 * array[9]
        array[9], inputdata[9] = r, inputdata[9] + r 
    if cmd == 'ZK': 
        # RZK: 10 ==> 50% of 10
        r = 0.5 * array[10]
        array[10], inputdata[10] = r, inputdata[10] + r
    if cmd == 'ZL': 
        # RZL: 11 ==> 50% of 11
        r = 0.5 * array[11]
        array[11], inputdata[11] = r, inputdata[11] + r
    if cmd == 'ZM': 
        # RZM: 12 ==> 50% of 12
        r = 0.5 * array[12]
        array[12], inputdata[12] = r, inputdata[12] + r
    if cmd == 'ZN': 
        # RZN: 13 ==> 50% of 13
        r = 0.5 * array[13]
        array[13], inputdata[13] = r, inputdata[13] + r
    if cmd == 'ZO': 
        # RZO: 14 ==> 50% of 14
        r = 0.5 * array[14]
        array[14], inputdata[14] = r, inputdata[14] + r
    if cmd == 'ZP': 
        # RZP: 15 ==> 50% of 15
        r = 0.5 * array[15]
        array[15], inputdata[15] = r, inputdata[15] + r
    if cmd == 'ZQ': 
        # RZQ: 16 ==> 50% of 16
        r = 0.5 * array[16]
        array[16], inputdata[16] = r, inputdata[16] + r
    if cmd == 'ZR': 
        # RZR: 17 ==> 50% of 17
        r = 0.5 * array[17]
        array[17], inputdata[17] = r, inputdata[17] + r
    if cmd == 'ZS': 
        # RZS: 18 ==> 50% of 18
        r = 0.5 * array[18]
        array[18], inputdata[18] = r, inputdata[18] + r
    if cmd == 'ZT': 
        # RZT: 19 ==> 50% of 19
        r = 0.5 * array[19]
        array[19], inputdata[19] = r, inputdata[19] + r
    if cmd == 'ZU': 
        # RZU: 20 ==> 50% of 20
        r = 0.5 * array[20]
        array[20], inputdata[20] = r, inputdata[20] + r
    if cmd == 'ZV': 
        # RZV: 21 ==> 50% of 21
        r = 0.5 * array[21]
        array[21], inputdata[21] = r, inputdata[21] + r
    if cmd == 'ZW': 
        # RZW: 22 ==> 50% of 22
        r = 0.5 * array[10]
        array[22], inputdata[22] = r, inputdata[22] + r
    if cmd == 'ZX': 
        # RZX: 23 ==> 50% of 23
        r = 0.5 * array[23]
        array[23], inputdata[23] = r, inputdata[23] + r
    if cmd == 'ZY': 
        # RZY: 24 ==> 50% of 24
        r = 0.5 * array[24]
        array[24], inputdata[24] = r, inputdata[24] + r
    return (array, apointer, inputdata, output, source, spointer)

numericCodons = {'00': null_codon, '01': interpret_codon, '02': interpret_codon, '03': interpret_codon, '04': interpret_codon, '05': interpret_codon, '06': interpret_codon, '07': interpret_codon, '08': interpret_codon, '09': interpret_codon, '10': interpret_codon, '11': interpret_codon, '12': interpret_codon, '13': interpret_codon, '14': interpret_codon, '15': interpret_codon, '16': interpret_codon, '17': interpret_codon, '18': interpret_codon, '19': interpret_codon, '20': interpret_codon, '21': interpret_codon, '22': interpret_codon, '23': interpret_codon, '24': interpret_codon, '25': interpret_codon, '26': interpret_codon, '27': interpret_codon, '28': interpret_codon, '29': interpret_codon, '30': interpret_codon, '31': interpret_codon, '32': interpret_codon, '33': interpret_codon, '34': interpret_codon, '35': interpret_codon, '36': interpret_codon, '37': interpret_codon, '38': interpret_codon, '39': interpret_codon, '40': interpret_codon, '41': interpret_codon, '42': interpret_codon, '43': interpret_codon, '44': interpret_codon, '45': interpret_codon, '46': undefined_codon, '47': undefined_codon, '48': undefined_codon, '49': undefined_codon, '50': undefined_codon, '51': undefined_codon, '52': undefined_codon, '53': undefined_codon, '54': undefined_codon, '55': undefined_codon, '56': undefined_codon, '57': undefined_codon, '58': undefined_codon, '59': undefined_codon, '60': undefined_codon, '61': undefined_codon, '62': undefined_codon, '63': undefined_codon, '64': undefined_codon, '65': undefined_codon, '66': undefined_codon, '67': undefined_codon, '68': undefined_codon, '69': undefined_codon, '70': undefined_codon, '71': undefined_codon, '72': undefined_codon, '73': undefined_codon, '74': undefined_codon, '75': undefined_codon, '76': undefined_codon, '77': undefined_codon, '78': undefined_codon, '79': undefined_codon, '80': undefined_codon, '81': undefined_codon, '82': undefined_codon, '83': undefined_codon, '84': undefined_codon, '85': undefined_codon, '86': undefined_codon, '87': undefined_codon, '88': undefined_codon, '89': undefined_codon, '90': undefined_codon, '91': undefined_codon, '92': undefined_codon, '93': undefined_codon, '94': undefined_codon, '95': undefined_codon, '96': undefined_codon, '97': undefined_codon, '98': undefined_codon, '99': undefined_codon}

alphabeticalCodons = {'AA': undefined_codon, 'AB': undefined_codon, 'AC': undefined_codon, 'AD': undefined_codon, 'AE': undefined_codon, 'AF': undefined_codon, 'AG': undefined_codon, 'AH': undefined_codon, 'AI': undefined_codon, 'AJ': undefined_codon, 'AK': undefined_codon, 'AL': undefined_codon, 'AM': undefined_codon, 'AN': undefined_codon, 'AO': undefined_codon, 'AP': undefined_codon, 'AQ': undefined_codon, 'AR': undefined_codon, 'AS': undefined_codon, 'AT': undefined_codon, 'AU': undefined_codon, 'AV': undefined_codon, 'AW': undefined_codon, 'AX': undefined_codon, 'AY': undefined_codon, 'AZ': importers, 'BA': undefined_codon, 'BB': undefined_codon, 'BC': undefined_codon, 'BD': undefined_codon, 'BE': undefined_codon, 'BF': undefined_codon, 'BG': undefined_codon, 'BH': undefined_codon, 'BI': undefined_codon, 'BJ': undefined_codon, 'BK': undefined_codon, 'BL': undefined_codon, 'BM': undefined_codon, 'BN': undefined_codon, 'BO': undefined_codon, 'BP': undefined_codon, 'BQ': undefined_codon, 'BR': undefined_codon, 'BS': undefined_codon, 'BT': undefined_codon, 'BU': undefined_codon, 'BV': undefined_codon, 'BW': undefined_codon, 'BX': undefined_codon, 'BY': undefined_codon, 'BZ': importers, 'CA': undefined_codon, 'CB': undefined_codon, 'CC': undefined_codon, 'CD': undefined_codon, 'CE': undefined_codon, 'CF': undefined_codon, 'CG': undefined_codon, 'CH': undefined_codon, 'CI': undefined_codon, 'CJ': undefined_codon, 'CK': undefined_codon, 'CL': undefined_codon, 'CM': undefined_codon, 'CN': undefined_codon, 'CO': undefined_codon, 'CP': undefined_codon, 'CQ': undefined_codon, 'CR': undefined_codon, 'CS': undefined_codon, 'CT': undefined_codon, 'CU': undefined_codon, 'CV': undefined_codon, 'CW': undefined_codon, 'CX': undefined_codon, 'CY': undefined_codon, 'CZ': importers, 'DA': undefined_codon, 'DB': undefined_codon, 'DC': undefined_codon, 'DD': undefined_codon, 'DE': undefined_codon, 'DF': undefined_codon, 'DG': undefined_codon, 'DH': undefined_codon, 'DI': undefined_codon, 'DJ': undefined_codon, 'DK': undefined_codon, 'DL': undefined_codon, 'DM': undefined_codon, 'DN': undefined_codon, 'DO': undefined_codon, 'DP': undefined_codon, 'DQ': undefined_codon, 'DR': undefined_codon, 'DS': undefined_codon, 'DT': undefined_codon, 'DU': undefined_codon, 'DV': undefined_codon, 'DW': undefined_codon, 'DX': undefined_codon, 'DY': undefined_codon, 'DZ': importers, 'EA': undefined_codon, 'EB': undefined_codon, 'EC': undefined_codon, 'ED': undefined_codon, 'EE': undefined_codon, 'EF': undefined_codon, 'EG': undefined_codon, 'EH': undefined_codon, 'EI': undefined_codon, 'EJ': undefined_codon, 'EK': undefined_codon, 'EL': undefined_codon, 'EM': undefined_codon, 'EN': undefined_codon, 'EO': undefined_codon, 'EP': undefined_codon, 'EQ': undefined_codon, 'ER': undefined_codon, 'ES': undefined_codon, 'ET': undefined_codon, 'EU': undefined_codon, 'EV': undefined_codon, 'EW': undefined_codon, 'EX': undefined_codon, 'EY': undefined_codon, 'EZ': importers, 'FA': undefined_codon, 'FB': undefined_codon, 'FC': undefined_codon, 'FD': undefined_codon, 'FE': undefined_codon, 'FF': undefined_codon, 'FG': undefined_codon, 'FH': undefined_codon, 'FI': undefined_codon, 'FJ': undefined_codon, 'FK': undefined_codon, 'FL': undefined_codon, 'FM': undefined_codon, 'FN': undefined_codon, 'FO': undefined_codon, 'FP': undefined_codon, 'FQ': undefined_codon, 'FR': undefined_codon, 'FS': undefined_codon, 'FT': undefined_codon, 'FU': undefined_codon, 'FV': undefined_codon, 'FW': undefined_codon, 'FX': undefined_codon, 'FY': undefined_codon, 'FZ': importers, 'GA': undefined_codon, 'GB': undefined_codon, 'GC': undefined_codon, 'GD': undefined_codon, 'GE': undefined_codon, 'GF': undefined_codon, 'GG': undefined_codon, 'GH': undefined_codon, 'GI': undefined_codon, 'GJ': undefined_codon, 'GK': undefined_codon, 'GL': undefined_codon, 'GM': undefined_codon, 'GN': undefined_codon, 'GO': undefined_codon, 'GP': undefined_codon, 'GQ': undefined_codon, 'GR': undefined_codon, 'GS': undefined_codon, 'GT': undefined_codon, 'GU': undefined_codon, 'GV': undefined_codon, 'GW': undefined_codon, 'GX': undefined_codon, 'GY': undefined_codon, 'GZ': importers, 'HA': undefined_codon, 'HB': undefined_codon, 'HC': undefined_codon, 'HD': undefined_codon, 'HE': undefined_codon, 'HF': undefined_codon, 'HG': undefined_codon, 'HH': undefined_codon, 'HI': undefined_codon, 'HJ': undefined_codon, 'HK': undefined_codon, 'HL': undefined_codon, 'HM': undefined_codon, 'HN': undefined_codon, 'HO': undefined_codon, 'HP': undefined_codon, 'HQ': undefined_codon, 'HR': undefined_codon, 'HS': undefined_codon, 'HT': undefined_codon, 'HU': undefined_codon, 'HV': undefined_codon, 'HW': undefined_codon, 'HX': undefined_codon, 'HY': undefined_codon, 'HZ': importers, 'IA': undefined_codon, 'IB': undefined_codon, 'IC': undefined_codon, 'ID': undefined_codon, 'IE': undefined_codon, 'IF': undefined_codon, 'IG': undefined_codon, 'IH': undefined_codon, 'II': undefined_codon, 'IJ': undefined_codon, 'IK': undefined_codon, 'IL': undefined_codon, 'IM': undefined_codon, 'IN': undefined_codon, 'IO': undefined_codon, 'IP': undefined_codon, 'IQ': undefined_codon, 'IR': undefined_codon, 'IS': undefined_codon, 'IT': undefined_codon, 'IU': undefined_codon, 'IV': undefined_codon, 'IW': undefined_codon, 'IX': undefined_codon, 'IY': undefined_codon, 'IZ': importers, 'JA': undefined_codon, 'JB': undefined_codon, 'JC': undefined_codon, 'JD': undefined_codon, 'JE': undefined_codon, 'JF': undefined_codon, 'JG': undefined_codon, 'JH': undefined_codon, 'JI': undefined_codon, 'JJ': undefined_codon, 'JK': undefined_codon, 'JL': undefined_codon, 'JM': undefined_codon, 'JN': undefined_codon, 'JO': undefined_codon, 'JP': undefined_codon, 'JQ': undefined_codon, 'JR': undefined_codon, 'JS': undefined_codon, 'JT': undefined_codon, 'JU': undefined_codon, 'JV': undefined_codon, 'JW': undefined_codon, 'JX': undefined_codon, 'JY': undefined_codon, 'JZ': importers, 'KA': undefined_codon, 'KB': undefined_codon, 'KC': undefined_codon, 'KD': undefined_codon, 'KE': undefined_codon, 'KF': undefined_codon, 'KG': undefined_codon, 'KH': undefined_codon, 'KI': undefined_codon, 'KJ': undefined_codon, 'KK': undefined_codon, 'KL': undefined_codon, 'KM': undefined_codon, 'KN': undefined_codon, 'KO': undefined_codon, 'KP': undefined_codon, 'KQ': undefined_codon, 'KR': undefined_codon, 'KS': undefined_codon, 'KT': undefined_codon, 'KU': undefined_codon, 'KV': undefined_codon, 'KW': undefined_codon, 'KX': undefined_codon, 'KY': undefined_codon, 'KZ': importers, 'LA': undefined_codon, 'LB': undefined_codon, 'LC': undefined_codon, 'LD': undefined_codon, 'LE': undefined_codon, 'LF': undefined_codon, 'LG': undefined_codon, 'LH': undefined_codon, 'LI': undefined_codon, 'LJ': undefined_codon, 'LK': undefined_codon, 'LL': undefined_codon, 'LM': undefined_codon, 'LN': undefined_codon, 'LO': undefined_codon, 'LP': undefined_codon, 'LQ': undefined_codon, 'LR': undefined_codon, 'LS': undefined_codon, 'LT': undefined_codon, 'LU': undefined_codon, 'LV': undefined_codon, 'LW': undefined_codon, 'LX': undefined_codon, 'LY': undefined_codon, 'LZ': importers, 'MA': undefined_codon, 'MB': undefined_codon, 'MC': undefined_codon, 'MD': undefined_codon, 'ME': undefined_codon, 'MF': undefined_codon, 'MG': undefined_codon, 'MH': undefined_codon, 'MI': undefined_codon, 'MJ': undefined_codon, 'MK': undefined_codon, 'ML': undefined_codon, 'MM': undefined_codon, 'MN': undefined_codon, 'MO': undefined_codon, 'MP': undefined_codon, 'MQ': undefined_codon, 'MR': undefined_codon, 'MS': undefined_codon, 'MT': undefined_codon, 'MU': undefined_codon, 'MV': undefined_codon, 'MW': undefined_codon, 'MX': undefined_codon, 'MY': undefined_codon, 'MZ': importers, 'NA': undefined_codon, 'NB': undefined_codon, 'NC': undefined_codon, 'ND': undefined_codon, 'NE': undefined_codon, 'NF': undefined_codon, 'NG': undefined_codon, 'NH': undefined_codon, 'NI': undefined_codon, 'NJ': undefined_codon, 'NK': undefined_codon, 'NL': undefined_codon, 'NM': undefined_codon, 'NN': undefined_codon, 'NO': undefined_codon, 'NP': undefined_codon, 'NQ': undefined_codon, 'NR': undefined_codon, 'NS': undefined_codon, 'NT': undefined_codon, 'NU': undefined_codon, 'NV': undefined_codon, 'NW': undefined_codon, 'NX': undefined_codon, 'NY': undefined_codon, 'NZ': importers, 'OA': undefined_codon, 'OB': undefined_codon, 'OC': undefined_codon, 'OD': undefined_codon, 'OE': undefined_codon, 'OF': undefined_codon, 'OG': undefined_codon, 'OH': undefined_codon, 'OI': undefined_codon, 'OJ': undefined_codon, 'OK': undefined_codon, 'OL': undefined_codon, 'OM': undefined_codon, 'ON': undefined_codon, 'OO': undefined_codon, 'OP': undefined_codon, 'OQ': undefined_codon, 'OR': undefined_codon, 'OS': undefined_codon, 'OT': undefined_codon, 'OU': undefined_codon, 'OV': undefined_codon, 'OW': undefined_codon, 'OX': undefined_codon, 'OY': undefined_codon, 'OZ': importers, 'PA': undefined_codon, 'PB': undefined_codon, 'PC': undefined_codon, 'PD': undefined_codon, 'PE': undefined_codon, 'PF': undefined_codon, 'PG': undefined_codon, 'PH': undefined_codon, 'PI': undefined_codon, 'PJ': undefined_codon, 'PK': undefined_codon, 'PL': undefined_codon, 'PM': undefined_codon, 'PN': undefined_codon, 'PO': undefined_codon, 'PP': undefined_codon, 'PQ': undefined_codon, 'PR': undefined_codon, 'PS': undefined_codon, 'PT': undefined_codon, 'PU': undefined_codon, 'PV': undefined_codon, 'PW': undefined_codon, 'PX': undefined_codon, 'PY': undefined_codon, 'PZ': importers, 'QA': undefined_codon, 'QB': undefined_codon, 'QC': undefined_codon, 'QD': undefined_codon, 'QE': undefined_codon, 'QF': undefined_codon, 'QG': undefined_codon, 'QH': undefined_codon, 'QI': undefined_codon, 'QJ': undefined_codon, 'QK': undefined_codon, 'QL': undefined_codon, 'QM': undefined_codon, 'QN': undefined_codon, 'QO': undefined_codon, 'QP': undefined_codon, 'QQ': undefined_codon, 'QR': undefined_codon, 'QS': undefined_codon, 'QT': undefined_codon, 'QU': undefined_codon, 'QV': undefined_codon, 'QW': undefined_codon, 'QX': undefined_codon, 'QY': undefined_codon, 'QZ': importers, 'RA': undefined_codon, 'RB': undefined_codon, 'RC': undefined_codon, 'RD': undefined_codon, 'RE': undefined_codon, 'RF': undefined_codon, 'RG': undefined_codon, 'RH': undefined_codon, 'RI': undefined_codon, 'RJ': undefined_codon, 'RK': undefined_codon, 'RL': undefined_codon, 'RM': undefined_codon, 'RN': undefined_codon, 'RO': undefined_codon, 'RP': undefined_codon, 'RQ': undefined_codon, 'RR': undefined_codon, 'RS': undefined_codon, 'RT': undefined_codon, 'RU': undefined_codon, 'RV': undefined_codon, 'RW': undefined_codon, 'RX': undefined_codon, 'RY': undefined_codon, 'RZ': importers, 'SA': undefined_codon, 'SB': undefined_codon, 'SC': undefined_codon, 'SD': undefined_codon, 'SE': undefined_codon, 'SF': undefined_codon, 'SG': undefined_codon, 'SH': undefined_codon, 'SI': undefined_codon, 'SJ': undefined_codon, 'SK': undefined_codon, 'SL': undefined_codon, 'SM': undefined_codon, 'SN': undefined_codon, 'SO': undefined_codon, 'SP': undefined_codon, 'SQ': undefined_codon, 'SR': undefined_codon, 'SS': undefined_codon, 'ST': undefined_codon, 'SU': undefined_codon, 'SV': undefined_codon, 'SW': undefined_codon, 'SX': undefined_codon, 'SY': undefined_codon, 'SZ': importers, 'TA': undefined_codon, 'TB': undefined_codon, 'TC': undefined_codon, 'TD': undefined_codon, 'TE': undefined_codon, 'TF': undefined_codon, 'TG': undefined_codon, 'TH': undefined_codon, 'TI': undefined_codon, 'TJ': undefined_codon, 'TK': undefined_codon, 'TL': undefined_codon, 'TM': undefined_codon, 'TN': undefined_codon, 'TO': undefined_codon, 'TP': undefined_codon, 'TQ': undefined_codon, 'TR': undefined_codon, 'TS': undefined_codon, 'TT': undefined_codon, 'TU': undefined_codon, 'TV': undefined_codon, 'TW': undefined_codon, 'TX': undefined_codon, 'TY': undefined_codon, 'TZ': importers, 'UA': undefined_codon, 'UB': undefined_codon, 'UC': undefined_codon, 'UD': undefined_codon, 'UE': undefined_codon, 'UF': undefined_codon, 'UG': undefined_codon, 'UH': undefined_codon, 'UI': undefined_codon, 'UJ': undefined_codon, 'UK': undefined_codon, 'UL': undefined_codon, 'UM': undefined_codon, 'UN': undefined_codon, 'UO': undefined_codon, 'UP': undefined_codon, 'UQ': undefined_codon, 'UR': undefined_codon, 'US': undefined_codon, 'UT': undefined_codon, 'UU': undefined_codon, 'UV': undefined_codon, 'UW': undefined_codon, 'UX': undefined_codon, 'UY': undefined_codon, 'UZ': importers, 'VA': undefined_codon, 'VB': undefined_codon, 'VC': undefined_codon, 'VD': undefined_codon, 'VE': undefined_codon, 'VF': undefined_codon, 'VG': undefined_codon, 'VH': undefined_codon, 'VI': undefined_codon, 'VJ': undefined_codon, 'VK': undefined_codon, 'VL': undefined_codon, 'VM': undefined_codon, 'VN': undefined_codon, 'VO': undefined_codon, 'VP': undefined_codon, 'VQ': undefined_codon, 'VR': undefined_codon, 'VS': undefined_codon, 'VT': undefined_codon, 'VU': undefined_codon, 'VV': undefined_codon, 'VW': undefined_codon, 'VX': undefined_codon, 'VY': undefined_codon, 'VZ': importers, 'WA': undefined_codon, 'WB': undefined_codon, 'WC': undefined_codon, 'WD': undefined_codon, 'WE': undefined_codon, 'WF': undefined_codon, 'WG': undefined_codon, 'WH': undefined_codon, 'WI': undefined_codon, 'WJ': undefined_codon, 'WK': undefined_codon, 'WL': undefined_codon, 'WM': undefined_codon, 'WN': undefined_codon, 'WO': undefined_codon, 'WP': undefined_codon, 'WQ': undefined_codon, 'WR': undefined_codon, 'WS': undefined_codon, 'WT': undefined_codon, 'WU': undefined_codon, 'WV': undefined_codon, 'WW': undefined_codon, 'WX': undefined_codon, 'WY': undefined_codon, 'WZ': importers, 'XA': undefined_codon, 'XB': undefined_codon, 'XC': undefined_codon, 'XD': undefined_codon, 'XE': undefined_codon, 'XF': undefined_codon, 'XG': undefined_codon, 'XH': undefined_codon, 'XI': undefined_codon, 'XJ': undefined_codon, 'XK': undefined_codon, 'XL': undefined_codon, 'XM': undefined_codon, 'XN': undefined_codon, 'XO': undefined_codon, 'XP': undefined_codon, 'XQ': undefined_codon, 'XR': undefined_codon, 'XS': undefined_codon, 'XT': undefined_codon, 'XU': undefined_codon, 'XV': undefined_codon, 'XW': undefined_codon, 'XX': undefined_codon, 'XY': undefined_codon, 'XZ': importers, 'YA': undefined_codon, 'YB': undefined_codon, 'YC': undefined_codon, 'YD': undefined_codon, 'YE': undefined_codon, 'YF': undefined_codon, 'YG': undefined_codon, 'YH': undefined_codon, 'YI': undefined_codon, 'YJ': undefined_codon, 'YK': undefined_codon, 'YL': undefined_codon, 'YM': undefined_codon, 'YN': undefined_codon, 'YO': undefined_codon, 'YP': undefined_codon, 'YQ': undefined_codon, 'YR': undefined_codon, 'YS': undefined_codon, 'YT': undefined_codon, 'YU': undefined_codon, 'YV': undefined_codon, 'YW': undefined_codon, 'YX': undefined_codon, 'YY': undefined_codon, 'YZ': importers, 'ZA': exporters, 'ZB': exporters, 'ZC': exporters, 'ZD': exporters, 'ZE': exporters, 'ZF': exporters, 'ZG': exporters, 'ZH': exporters, 'ZI': exporters, 'ZJ': exporters, 'ZK': exporters, 'ZL': exporters, 'ZM': exporters, 'ZN': exporters, 'ZO': exporters, 'ZP': exporters, 'ZQ': exporters, 'ZR': exporters, 'ZS': exporters, 'ZT': exporters, 'ZU': exporters, 'ZV': exporters, 'ZW': exporters, 'ZX': exporters, 'ZY': exporters, 'ZZ': undefined_codon}

interpreter = {}
interpreter.update(numericCodons)
interpreter.update(alphabeticalCodons)
