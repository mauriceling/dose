"""
SUNANDA GENOMIC INTERPRETER
Date created: 9th April 2021

The interpreter environment consists of the following elements:

    1. Array/Tape   ==> A circular tape initialized with 316 cells proxy for 316 metabolites.

    2. Source       ==> The program

    3. Input List   ==> A list of data given to the execution environment at initialization.

    4. Output List  ==> A list of output from the execution. This may also be used as a
                        secondary tape.

When the program terminates, 4 elements (Array, Source, Input List and Output List)
are returned, and the interpreter terminates itself.

"""

codon_length = 2


def reserved_gene(array, pointer, inputdata, output, source, spointer):
    """
    Default handler for the initiated instructions symbolizing reserved/initialised
    genes (26 identical di-nucleotides ==> AA,BB,CC...,YY, ZZ).
    """
    cmd = source[spointer: spointer + codon_length]
    if cmd in ["AA", "BB", "CC", "DD", "EE", "FF", "GG", "HH", "II",
               "JJ", "KK", "LL", "MM", "NN", "OO", "PP", "QQ", "RR",
               "SS", "TT", "UU", "VV", "WW", "XX", "YY", "ZZ"]:
        pass
    return (array, pointer, inputdata, output, source, spointer)


def enzymatic_gene(array, pointer, inputdata, output, source, spointer):
    """
    Default handler for the set of 406 enzymatic genes that define metabolic activity.
    """
    cmd = source[spointer: spointer + codon_length]
    if cmd =="AB" and array[273] > 0: array[273], array[76] = array[273] - 1, array[76] + 1
    if cmd =="AC" and array[161] > 0: array[161], array[82] = array[161] - 1, array[82] + 1
    if cmd =="AD" and array[285] > 0: array[285], array[107] = array[285] - 1, array[107] + 1
    if cmd =="AE" and array[182] > 0: array[182], array[183] = array[182] - 1, array[183] + 1
    if cmd =="AF" and array[249] > 0: array[249], array[104] = array[249] - 1, array[104] + 1
    if cmd =="AG" and array[102] > 0: array[102], array[238] = array[102] - 1, array[238] + 1
    if cmd =="AH" and array[15] > 0: array[15], array[246] = array[15] - 1, array[246] + 1
    if cmd =="AI" and array[276] > 0: array[276], array[198] = array[276] - 1, array[198] + 1
    if cmd =="AJ" and array[93] > 0: array[93], array[307] = array[93] - 1, array[307] + 1
    if cmd =="AK" and array[58] > 0: array[58], array[304] = array[58] - 1, array[304] + 1
    if cmd =="AM" and array[124] > 0: array[124], array[71] = array[124] - 1, array[71] + 1
    if cmd =="AO" and array[157] > 0: array[157], array[282] = array[157] - 1, array[282] + 1
    if cmd =="AY" and array[299] > 0: array[299], array[290] = array[299] - 1, array[290] + 1
    if cmd =="AZ" and array[256] > 0: array[256], array[258] = array[256] - 1, array[258] + 1
    if cmd =="BC" and array[297] > 0: array[297], array[273] = array[297] - 1, array[273] + 1
    if cmd =="BE" and array[70] > 0: array[70], array[203] = array[70] - 1, array[203] + 1
    if cmd =="BF" and array[173] > 0: array[173], array[128] = array[173] - 1, array[128] + 1
    if cmd =="BH" and array[211] > 0: array[211], array[43] = array[211] - 1, array[43] + 1
    if cmd =="BI" and array[174] > 0: array[174], array[294] = array[174] - 1, array[294] + 1
    if cmd =="BK" and array[236] > 0: array[236], array[30] = array[236] - 1, array[30] + 1
    if cmd =="BL" and array[110] > 0: array[110], array[269] = array[110] - 1, array[269] + 1
    if cmd =="BM" and array[231] > 0: array[231], array[58] = array[231] - 1, array[58] + 1
    if cmd =="BN" and array[101] > 0: array[101], array[64] = array[101] - 1, array[64] + 1
    if cmd =="BO" and array[54] > 0: array[54], array[313] = array[54] - 1, array[313] + 1
    if cmd =="BP" and array[158] > 0: array[158], array[34] = array[158] - 1, array[34] + 1
    if cmd =="BQ" and array[186] > 0: array[186], array[54] = array[186] - 1, array[54] + 1
    if cmd =="BR" and array[209] > 0: array[209], array[302] = array[209] - 1, array[302] + 1
    if cmd =="BS" and array[315] > 0: array[315], array[272] = array[315] - 1, array[272] + 1
    if cmd =="BT" and array[40] > 0: array[40], array[164] = array[40] - 1, array[164] + 1
    if cmd =="BV" and array[232] > 0: array[232], array[113] = array[232] - 1, array[113] + 1
    if cmd =="BW" and array[286] > 0: array[286], array[44] = array[286] - 1, array[44] + 1
    if cmd =="BY" and array[87] > 0: array[87], array[129] = array[87] - 1, array[129] + 1
    if cmd =="CA" and array[303] > 0: array[303], array[197] = array[303] - 1, array[197] + 1
    if cmd =="CB" and array[55] > 0: array[55], array[260] = array[55] - 1, array[260] + 1
    if cmd =="CD" and array[262] > 0: array[262], array[83] = array[262] - 1, array[83] + 1
    if cmd =="CE" and array[84] > 0: array[84], array[186] = array[84] - 1, array[186] + 1
    if cmd =="CF" and array[145] > 0: array[145], array[218] = array[145] - 1, array[218] + 1
    if cmd =="CH" and array[190] > 0: array[190], array[68] = array[190] - 1, array[68] + 1
    if cmd =="CJ" and array[218] > 0: array[218], array[35] = array[218] - 1, array[35] + 1
    if cmd =="CK" and array[252] > 0: array[252], array[12] = array[252] - 1, array[12] + 1
    if cmd =="CL" and array[126] > 0: array[126], array[29] = array[126] - 1, array[29] + 1
    if cmd =="CM" and array[64] > 0: array[64], array[52] = array[64] - 1, array[52] + 1
    if cmd =="CN" and array[23] > 0: array[23], array[11] = array[23] - 1, array[11] + 1
    if cmd =="CO" and array[149] > 0: array[149], array[102] = array[149] - 1, array[102] + 1
    if cmd =="CP" and array[220] > 0: array[220], array[72] = array[220] - 1, array[72] + 1
    if cmd =="CQ" and array[212] > 0: array[212], array[25] = array[212] - 1, array[25] + 1
    if cmd =="CS" and array[177] > 0: array[177], array[22] = array[177] - 1, array[22] + 1
    if cmd =="CT" and array[152] > 0: array[152], array[145] = array[152] - 1, array[145] + 1
    if cmd =="CU" and array[115] > 0: array[115], array[8] = array[115] - 1, array[8] + 1
    if cmd =="CV" and array[80] > 0: array[80], array[33] = array[80] - 1, array[33] + 1
    if cmd =="CW" and array[50] > 0: array[50], array[223] = array[50] - 1, array[223] + 1
    if cmd =="CY" and array[6] > 0: array[6], array[207] = array[6] - 1, array[207] + 1
    if cmd =="CZ" and array[265] > 0: array[265], array[180] = array[265] - 1, array[180] + 1
    if cmd =="DA" and array[143] > 0: array[143], array[217] = array[143] - 1, array[217] + 1
    if cmd =="DB" and array[151] > 0: array[151], array[144] = array[151] - 1, array[144] + 1
    if cmd =="DC" and array[181] > 0: array[181], array[225] = array[181] - 1, array[225] + 1
    if cmd =="DE" and array[63] > 0: array[63], array[26] = array[63] - 1, array[26] + 1
    if cmd =="DG" and array[61] > 0: array[61], array[95] = array[61] - 1, array[95] + 1
    if cmd =="DH" and array[30] > 0: array[30], array[310] = array[30] - 1, array[310] + 1
    if cmd =="DI" and array[248] > 0: array[248], array[191] = array[248] - 1, array[191] + 1
    if cmd =="DL" and array[56] > 0: array[56], array[171] = array[56] - 1, array[171] + 1
    if cmd =="DM" and array[277] > 0: array[277], array[274] = array[277] - 1, array[274] + 1
    if cmd =="DN" and array[134] > 0: array[134], array[170] = array[134] - 1, array[170] + 1
    if cmd =="DS" and array[31] > 0: array[31], array[200] = array[31] - 1, array[200] + 1
    if cmd =="DV" and array[176] > 0: array[176], array[265] = array[176] - 1, array[265] + 1
    if cmd =="DY" and array[306] > 0: array[306], array[193] = array[306] - 1, array[193] + 1
    if cmd =="EA" and array[281] > 0: array[281], array[139] = array[281] - 1, array[139] + 1
    if cmd =="EB" and array[199] > 0: array[199], array[234] = array[199] - 1, array[234] + 1
    if cmd =="ED" and array[255] > 0: array[255], array[199] = array[255] - 1, array[199] + 1
    if cmd =="EF" and array[78] > 0: array[78], array[124] = array[78] - 1, array[124] + 1
    if cmd =="EG" and array[283] > 0: array[283], array[110] = array[283] - 1, array[110] + 1
    if cmd =="EH" and array[295] > 0: array[295], array[305] = array[295] - 1, array[305] + 1
    if cmd =="EI" and array[118] > 0: array[118], array[116] = array[118] - 1, array[116] + 1
    if cmd =="EK" and array[29] > 0: array[29], array[5] = array[29] - 1, array[5] + 1
    if cmd =="EM" and array[37] > 0: array[37], array[208] = array[37] - 1, array[208] + 1
    if cmd =="EP" and array[223] > 0: array[223], array[287] = array[223] - 1, array[287] + 1
    if cmd =="EQ" and array[44] > 0: array[44], array[84] = array[44] - 1, array[84] + 1
    if cmd =="ER" and array[259] > 0: array[259], array[216] = array[259] - 1, array[216] + 1
    if cmd =="ES" and array[169] > 0: array[169], array[165] = array[169] - 1, array[165] + 1
    if cmd =="ET" and array[95] > 0: array[95], array[167] = array[95] - 1, array[167] + 1
    if cmd =="EU" and array[282] > 0: array[282], array[51] = array[282] - 1, array[51] + 1
    if cmd =="EV" and array[258] > 0: array[258], array[77] = array[258] - 1, array[77] + 1
    if cmd =="EW" and array[82] > 0: array[82], array[247] = array[82] - 1, array[247] + 1
    if cmd =="EX" and array[245] > 0: array[245], array[159] = array[245] - 1, array[159] + 1
    if cmd =="EY" and array[204] > 0: array[204], array[150] = array[204] - 1, array[150] + 1
    if cmd =="FB" and array[38] > 0: array[38], array[120] = array[38] - 1, array[120] + 1
    if cmd =="FC" and array[83] > 0: array[83], array[49] = array[83] - 1, array[49] + 1
    if cmd =="FG" and array[140] > 0: array[140], array[155] = array[140] - 1, array[155] + 1
    if cmd =="FH" and array[254] > 0: array[254], array[69] = array[254] - 1, array[69] + 1
    if cmd =="FK" and array[103] > 0: array[103], array[267] = array[103] - 1, array[267] + 1
    if cmd =="FQ" and array[160] > 0: array[160], array[182] = array[160] - 1, array[182] + 1
    if cmd =="FR" and array[76] > 0: array[76], array[220] = array[76] - 1, array[220] + 1
    if cmd =="FU" and array[194] > 0: array[194], array[215] = array[194] - 1, array[215] + 1
    if cmd =="FX" and array[260] > 0: array[260], array[106] = array[260] - 1, array[106] + 1
    if cmd =="FZ" and array[144] > 0: array[144], array[41] = array[144] - 1, array[41] + 1
    if cmd =="GB" and array[166] > 0: array[166], array[81] = array[166] - 1, array[81] + 1
    if cmd =="GC" and array[243] > 0: array[243], array[135] = array[243] - 1, array[135] + 1
    if cmd =="GD" and array[219] > 0: array[219], array[177] = array[219] - 1, array[177] + 1
    if cmd =="GE" and array[305] > 0: array[305], array[306] = array[305] - 1, array[306] + 1
    if cmd =="GF" and array[14] > 0: array[14], array[132] = array[14] - 1, array[132] + 1
    if cmd =="GH" and array[172] > 0: array[172], array[36] = array[172] - 1, array[36] + 1
    if cmd =="GJ" and array[71] > 0: array[71], array[130] = array[71] - 1, array[130] + 1
    if cmd =="GL" and array[27] > 0: array[27], array[39] = array[27] - 1, array[39] + 1
    if cmd =="GM" and array[287] > 0: array[287], array[46] = array[287] - 1, array[46] + 1
    if cmd =="GN" and array[90] > 0: array[90], array[243] = array[90] - 1, array[243] + 1
    if cmd =="GO" and array[122] > 0: array[122], array[233] = array[122] - 1, array[233] + 1
    if cmd =="GQ" and array[235] > 0: array[235], array[99] = array[235] - 1, array[99] + 1
    if cmd =="GR" and array[311] > 0: array[311], array[31] = array[311] - 1, array[31] + 1
    if cmd =="GS" and array[240] > 0: array[240], array[278] = array[240] - 1, array[278] + 1
    if cmd =="GU" and array[33] > 0: array[33], array[232] = array[33] - 1, array[232] + 1
    if cmd =="GY" and array[301] > 0: array[301], array[196] = array[301] - 1, array[196] + 1
    if cmd =="HA" and array[36] > 0: array[36], array[206] = array[36] - 1, array[206] + 1
    if cmd =="HC" and array[241] > 0: array[241], array[101] = array[241] - 1, array[101] + 1
    if cmd =="HD" and array[263] > 0: array[263], array[201] = array[263] - 1, array[201] + 1
    if cmd =="HE" and array[225] > 0: array[225], array[266] = array[225] - 1, array[266] + 1
    if cmd =="HF" and array[203] > 0: array[203], array[115] = array[203] - 1, array[115] + 1
    if cmd =="HG" and array[18] > 0: array[18], array[257] = array[18] - 1, array[257] + 1
    if cmd =="HK" and array[81] > 0: array[81], array[259] = array[81] - 1, array[259] + 1
    if cmd =="HP" and array[17] > 0: array[17], array[32] = array[17] - 1, array[32] + 1
    if cmd =="HQ" and array[127] > 0: array[127], array[174] = array[127] - 1, array[174] + 1
    if cmd =="HS" and array[77] > 0: array[77], array[24] = array[77] - 1, array[24] + 1
    if cmd =="HT" and array[187] > 0: array[187], array[158] = array[187] - 1, array[158] + 1
    if cmd =="HW" and array[41] > 0: array[41], array[173] = array[41] - 1, array[173] + 1
    if cmd =="HX" and array[179] > 0: array[179], array[230] = array[179] - 1, array[230] + 1
    if cmd =="IC" and array[135] > 0: array[135], array[127] = array[135] - 1, array[127] + 1
    if cmd =="IE" and array[131] > 0: array[131], array[151] = array[131] - 1, array[151] + 1
    if cmd =="IH" and array[24] > 0: array[24], array[249] = array[24] - 1, array[249] + 1
    if cmd =="IJ" and array[165] > 0: array[165], array[163] = array[165] - 1, array[163] + 1
    if cmd =="IM" and array[22] > 0: array[22], array[213] = array[22] - 1, array[213] + 1
    if cmd =="IN" and array[298] > 0: array[298], array[112] = array[298] - 1, array[112] + 1
    if cmd =="IO" and array[49] > 0: array[49], array[293] = array[49] - 1, array[293] + 1
    if cmd =="IQ" and array[189] > 0: array[189], array[133] = array[189] - 1, array[133] + 1
    if cmd =="IR" and array[46] > 0: array[46], array[245] = array[46] - 1, array[245] + 1
    if cmd =="IT" and array[296] > 0: array[296], array[279] = array[296] - 1, array[279] + 1
    if cmd =="IU" and array[210] > 0: array[210], array[122] = array[210] - 1, array[122] + 1
    if cmd =="IV" and array[133] > 0: array[133], array[48] = array[133] - 1, array[48] + 1
    if cmd =="IW" and array[1] > 0: array[1], array[143] = array[1] - 1, array[143] + 1
    if cmd =="IX" and array[224] > 0: array[224], array[119] = array[224] - 1, array[119] + 1
    if cmd =="IZ" and array[244] > 0: array[244], array[172] = array[244] - 1, array[172] + 1
    if cmd =="JA" and array[153] > 0: array[153], array[66] = array[153] - 1, array[66] + 1
    if cmd =="JC" and array[198] > 0: array[198], array[80] = array[198] - 1, array[80] + 1
    if cmd =="JD" and array[21] > 0: array[21], array[23] = array[21] - 1, array[23] + 1
    if cmd =="JE" and array[47] > 0: array[47], array[190] = array[47] - 1, array[190] + 1
    if cmd =="JF" and array[183] > 0: array[183], array[55] = array[183] - 1, array[55] + 1
    if cmd =="JG" and array[0] > 0: array[0], array[187] = array[0] - 1, array[187] + 1
    if cmd =="JI" and array[233] > 0: array[233], array[141] = array[233] - 1, array[141] + 1
    if cmd =="JL" and array[278] > 0: array[278], array[291] = array[278] - 1, array[291] + 1
    if cmd =="JN" and array[114] > 0: array[114], array[250] = array[114] - 1, array[250] + 1
    if cmd =="JO" and array[130] > 0: array[130], array[222] = array[130] - 1, array[222] + 1
    if cmd =="JP" and array[129] > 0: array[129], array[162] = array[129] - 1, array[162] + 1
    if cmd =="JQ" and array[43] > 0: array[43], array[239] = array[43] - 1, array[239] + 1
    if cmd =="JR" and array[106] > 0: array[106], array[89] = array[106] - 1, array[89] + 1
    if cmd =="JS" and array[180] > 0: array[180], array[202] = array[180] - 1, array[202] + 1
    if cmd =="JU" and array[72] > 0: array[72], array[292] = array[72] - 1, array[292] + 1
    if cmd =="JW" and array[155] > 0: array[155], array[53] = array[155] - 1, array[53] + 1
    if cmd =="JX" and array[279] > 0: array[279], array[253] = array[279] - 1, array[253] + 1
    if cmd =="JY" and array[89] > 0: array[89], array[38] = array[89] - 1, array[38] + 1
    if cmd =="JZ" and array[85] > 0: array[85], array[9] = array[85] - 1, array[9] + 1
    if cmd =="KB" and array[201] > 0: array[201], array[248] = array[201] - 1, array[248] + 1
    if cmd =="KD" and array[313] > 0: array[313], array[13] = array[313] - 1, array[13] + 1
    if cmd =="KF" and array[175] > 0: array[175], array[74] = array[175] - 1, array[74] + 1
    if cmd =="KH" and array[53] > 0: array[53], array[176] = array[53] - 1, array[176] + 1
    if cmd =="KJ" and array[197] > 0: array[197], array[75] = array[197] - 1, array[75] + 1
    if cmd =="KL" and array[96] > 0: array[96], array[277] = array[96] - 1, array[277] + 1
    if cmd =="KM" and array[10] > 0: array[10], array[212] = array[10] - 1, array[212] + 1
    if cmd =="KP" and array[138] > 0: array[138], array[268] = array[138] - 1, array[268] + 1
    if cmd =="KQ" and array[139] > 0: array[139], array[97] = array[139] - 1, array[97] + 1
    if cmd =="KR" and array[247] > 0: array[247], array[105] = array[247] - 1, array[105] + 1
    if cmd =="KU" and array[170] > 0: array[170], array[300] = array[170] - 1, array[300] + 1
    if cmd =="KV" and array[308] > 0: array[308], array[299] = array[308] - 1, array[299] + 1
    if cmd =="KY" and array[202] > 0: array[202], array[235] = array[202] - 1, array[235] + 1
    if cmd =="LA" and array[266] > 0: array[266], array[284] = array[266] - 1, array[284] + 1
    if cmd =="LB" and array[74] > 0: array[74], array[228] = array[74] - 1, array[228] + 1
    if cmd =="LC" and array[288] > 0: array[288], array[244] = array[288] - 1, array[244] + 1
    if cmd =="LD" and array[208] > 0: array[208], array[121] = array[208] - 1, array[121] + 1
    if cmd =="LE" and array[280] > 0: array[280], array[152] = array[280] - 1, array[152] + 1
    if cmd =="LF" and array[12] > 0: array[12], array[37] = array[12] - 1, array[37] + 1
    if cmd =="LH" and array[238] > 0: array[238], array[219] = array[238] - 1, array[219] + 1
    if cmd =="LJ" and array[185] > 0: array[185], array[188] = array[185] - 1, array[188] + 1
    if cmd =="LK" and array[136] > 0: array[136], array[296] = array[136] - 1, array[296] + 1
    if cmd =="LM" and array[97] > 0: array[97], array[14] = array[97] - 1, array[14] + 1
    if cmd =="LN" and array[178] > 0: array[178], array[309] = array[178] - 1, array[309] + 1
    if cmd =="LO" and array[304] > 0: array[304], array[59] = array[304] - 1, array[59] + 1
    if cmd =="LP" and array[222] > 0: array[222], array[123] = array[222] - 1, array[123] + 1
    if cmd =="LQ" and array[65] > 0: array[65], array[17] = array[65] - 1, array[17] + 1
    if cmd =="LR" and array[86] > 0: array[86], array[147] = array[86] - 1, array[147] + 1
    if cmd =="LS" and array[48] > 0: array[48], array[1] = array[48] - 1, array[1] + 1
    if cmd =="LT" and array[314] > 0: array[314], array[283] = array[314] - 1, array[283] + 1
    if cmd =="LU" and array[16] > 0: array[16], array[140] = array[16] - 1, array[140] + 1
    if cmd =="LV" and array[67] > 0: array[67], array[138] = array[67] - 1, array[138] + 1
    if cmd =="LZ" and array[309] > 0: array[309], array[56] = array[309] - 1, array[56] + 1
    if cmd =="MA" and array[148] > 0: array[148], array[308] = array[148] - 1, array[308] + 1
    if cmd =="MB" and array[192] > 0: array[192], array[211] = array[192] - 1, array[211] + 1
    if cmd =="MC" and array[11] > 0: array[11], array[312] = array[11] - 1, array[312] + 1
    if cmd =="MF" and array[242] > 0: array[242], array[2] = array[242] - 1, array[2] + 1
    if cmd =="MG" and array[191] > 0: array[191], array[195] = array[191] - 1, array[195] + 1
    if cmd =="MI" and array[167] > 0: array[167], array[18] = array[167] - 1, array[18] + 1
    if cmd =="MJ" and array[79] > 0: array[79], array[178] = array[79] - 1, array[178] + 1
    if cmd =="ML" and array[163] > 0: array[163], array[295] = array[163] - 1, array[295] + 1
    if cmd =="MN" and array[159] > 0: array[159], array[57] = array[159] - 1, array[57] + 1
    if cmd =="MO" and array[26] > 0: array[26], array[185] = array[26] - 1, array[185] + 1
    if cmd =="MQ" and array[228] > 0: array[228], array[289] = array[228] - 1, array[289] + 1
    if cmd =="MR" and array[66] > 0: array[66], array[194] = array[66] - 1, array[194] + 1
    if cmd =="MT" and array[270] > 0: array[270], array[255] = array[270] - 1, array[255] + 1
    if cmd =="MU" and array[128] > 0: array[128], array[103] = array[128] - 1, array[103] + 1
    if cmd =="MW" and array[205] > 0: array[205], array[303] = array[205] - 1, array[303] + 1
    if cmd =="MX" and array[200] > 0: array[200], array[276] = array[200] - 1, array[276] + 1
    if cmd =="MY" and array[104] > 0: array[104], array[254] = array[104] - 1, array[254] + 1
    if cmd =="NA" and array[20] > 0: array[20], array[280] = array[20] - 1, array[280] + 1
    if cmd =="NE" and array[221] > 0: array[221], array[153] = array[221] - 1, array[153] + 1
    if cmd =="NH" and array[312] > 0: array[312], array[131] = array[312] - 1, array[131] + 1
    if cmd =="NI" and array[59] > 0: array[59], array[62] = array[59] - 1, array[62] + 1
    if cmd =="NJ" and array[116] > 0: array[116], array[241] = array[116] - 1, array[241] + 1
    if cmd =="NQ" and array[125] > 0: array[125], array[166] = array[125] - 1, array[166] + 1
    if cmd =="NR" and array[105] > 0: array[105], array[231] = array[105] - 1, array[231] + 1
    if cmd =="NT" and array[119] > 0: array[119], array[314] = array[119] - 1, array[314] + 1
    if cmd =="NW" and array[51] > 0: array[51], array[227] = array[51] - 1, array[227] + 1
    if cmd =="NY" and array[264] > 0: array[264], array[169] = array[264] - 1, array[169] + 1
    if cmd =="OA" and array[4] > 0: array[4], array[214] = array[4] - 1, array[214] + 1
    if cmd =="OB" and array[109] > 0: array[109], array[19] = array[109] - 1, array[19] + 1
    if cmd =="OC" and array[216] > 0: array[216], array[270] = array[216] - 1, array[270] + 1
    if cmd =="OE" and array[310] > 0: array[310], array[226] = array[310] - 1, array[226] + 1
    if cmd =="OF" and array[111] > 0: array[111], array[45] = array[111] - 1, array[45] + 1
    if cmd =="OH" and array[234] > 0: array[234], array[85] = array[234] - 1, array[85] + 1
    if cmd =="OI" and array[206] > 0: array[206], array[179] = array[206] - 1, array[179] + 1
    if cmd =="OJ" and array[246] > 0: array[246], array[47] = array[246] - 1, array[47] + 1
    if cmd =="OK" and array[60] > 0: array[60], array[242] = array[60] - 1, array[242] + 1
    if cmd =="OL" and array[188] > 0: array[188], array[263] = array[188] - 1, array[263] + 1
    if cmd =="OM" and array[284] > 0: array[284], array[252] = array[284] - 1, array[252] + 1
    if cmd =="OP" and array[57] > 0: array[57], array[240] = array[57] - 1, array[240] + 1
    if cmd =="OQ" and array[25] > 0: array[25], array[315] = array[25] - 1, array[315] + 1
    if cmd =="OT" and array[28] > 0: array[28], array[15] = array[28] - 1, array[15] + 1
    if cmd =="OW" and array[251] > 0: array[251], array[92] = array[251] - 1, array[92] + 1
    if cmd =="OX" and array[302] > 0: array[302], array[87] = array[302] - 1, array[87] + 1
    if cmd =="OY" and array[5] > 0: array[5], array[256] = array[5] - 1, array[256] + 1
    if cmd =="OZ" and array[62] > 0: array[62], array[157] = array[62] - 1, array[157] + 1
    if cmd =="PA" and array[73] > 0: array[73], array[251] = array[73] - 1, array[251] + 1
    if cmd =="PB" and array[271] > 0: array[271], array[90] = array[271] - 1, array[90] + 1
    if cmd =="PC" and array[227] > 0: array[227], array[137] = array[227] - 1, array[137] + 1
    if cmd =="PD" and array[154] > 0: array[154], array[184] = array[154] - 1, array[184] + 1
    if cmd =="PG" and array[98] > 0: array[98], array[301] = array[98] - 1, array[301] + 1
    if cmd =="PK" and array[142] > 0: array[142], array[60] = array[142] - 1, array[60] + 1
    if cmd =="PM" and array[253] > 0: array[253], array[275] = array[253] - 1, array[275] + 1
    if cmd =="PN" and array[290] > 0: array[290], array[40] = array[290] - 1, array[40] + 1
    if cmd =="PO" and array[91] > 0: array[91], array[204] = array[91] - 1, array[204] + 1
    if cmd =="PQ" and array[237] > 0: array[237], array[168] = array[237] - 1, array[168] + 1
    if cmd =="PT" and array[35] > 0: array[35], array[100] = array[35] - 1, array[100] + 1
    if cmd =="PW" and array[7] > 0: array[7], array[111] = array[7] - 1, array[111] + 1
    if cmd =="PZ" and array[13] > 0: array[13], array[298] = array[13] - 1, array[298] + 1
    if cmd =="QA" and array[88] > 0: array[88], array[148] = array[88] - 1, array[148] + 1
    if cmd =="QB" and array[213] > 0: array[213], array[78] = array[213] - 1, array[78] + 1
    if cmd =="QC" and array[42] > 0: array[42], array[237] = array[42] - 1, array[237] + 1
    if cmd =="QD" and array[272] > 0: array[272], array[205] = array[272] - 1, array[205] + 1
    if cmd =="QE" and array[68] > 0: array[68], array[109] = array[68] - 1, array[109] + 1
    if cmd =="QF" and array[261] > 0: array[261], array[16] = array[261] - 1, array[16] + 1
    if cmd =="QI" and array[3] > 0: array[3], array[88] = array[3] - 1, array[88] + 1
    if cmd =="QJ" and array[250] > 0: array[250], array[114] = array[250] - 1, array[114] + 1
    if cmd =="QK" and array[137] > 0: array[137], array[10] = array[137] - 1, array[10] + 1
    if cmd =="QM" and array[141] > 0: array[141], array[118] = array[141] - 1, array[118] + 1
    if cmd =="QN" and array[108] > 0: array[108], array[98] = array[108] - 1, array[98] + 1
    if cmd =="QT" and array[268] > 0: array[268], array[0] = array[268] - 1, array[0] + 1
    if cmd =="QX" and array[274] > 0: array[274], array[3] = array[274] - 1, array[3] + 1
    if cmd =="QZ" and array[2] > 0: array[2], array[236] = array[2] - 1, array[236] + 1
    if cmd =="RA" and array[300] > 0: array[300], array[181] = array[300] - 1, array[181] + 1
    if cmd =="RC" and array[34] > 0: array[34], array[136] = array[34] - 1, array[136] + 1
    if cmd =="RD" and array[164] > 0: array[164], array[125] = array[164] - 1, array[125] + 1
    if cmd =="RF" and array[307] > 0: array[307], array[4] = array[307] - 1, array[4] + 1
    if cmd =="RH" and array[8] > 0: array[8], array[7] = array[8] - 1, array[7] + 1
    if cmd =="RJ" and array[113] > 0: array[113], array[161] = array[113] - 1, array[161] + 1
    if cmd =="RL" and array[239] > 0: array[239], array[175] = array[239] - 1, array[175] + 1
    if cmd =="RM" and array[294] > 0: array[294], array[28] = array[294] - 1, array[28] + 1
    if cmd =="RO" and array[267] > 0: array[267], array[264] = array[267] - 1, array[264] + 1
    if cmd =="RP" and array[150] > 0: array[150], array[27] = array[150] - 1, array[27] + 1
    if cmd =="RQ" and array[94] > 0: array[94], array[154] = array[94] - 1, array[154] + 1
    if cmd =="RS" and array[19] > 0: array[19], array[209] = array[19] - 1, array[209] + 1
    if cmd =="RT" and array[69] > 0: array[69], array[117] = array[69] - 1, array[117] + 1
    if cmd =="RU" and array[147] > 0: array[147], array[156] = array[147] - 1, array[156] + 1
    if cmd =="RW" and array[269] > 0: array[269], array[149] = array[269] - 1, array[149] + 1
    if cmd =="RX" and array[92] > 0: array[92], array[281] = array[92] - 1, array[281] + 1
    if cmd =="RY" and array[52] > 0: array[52], array[42] = array[52] - 1, array[42] + 1
    if cmd =="RZ" and array[168] > 0: array[168], array[6] = array[168] - 1, array[6] + 1
    if cmd =="SA" and array[184] > 0: array[184], array[94] = array[184] - 1, array[94] + 1
    if cmd =="SB" and array[156] > 0: array[156], array[160] = array[156] - 1, array[160] + 1
    if cmd =="SC" and array[107] > 0: array[107], array[91] = array[107] - 1, array[91] + 1
    if cmd =="SE" and array[171] > 0: array[171], array[210] = array[171] - 1, array[210] + 1
    if cmd =="SF" and array[291] > 0: array[291], array[142] = array[291] - 1, array[142] + 1
    if cmd =="SH" and array[112] > 0: array[112], array[134] = array[112] - 1, array[134] + 1
    if cmd =="SI" and array[162] > 0: array[162], array[20] = array[162] - 1, array[20] + 1
    if cmd =="SJ" and array[207] > 0: array[207], array[288] = array[207] - 1, array[288] + 1
    if cmd =="SK" and array[100] > 0: array[100], array[86] = array[100] - 1, array[86] + 1
    if cmd =="SL" and array[99] > 0: array[99], array[271] = array[99] - 1, array[271] + 1
    if cmd =="SM" and array[121] > 0: array[121], array[73] = array[121] - 1, array[73] + 1
    if cmd =="SN" and array[292] > 0: array[292], array[70] = array[292] - 1, array[70] + 1
    if cmd =="SP" and array[123] > 0: array[123], array[21] = array[123] - 1, array[21] + 1
    if cmd =="SQ" and array[75] > 0: array[75], array[126] = array[75] - 1, array[126] + 1
    if cmd =="ST" and array[226] > 0: array[226], array[50] = array[226] - 1, array[50] + 1
    if cmd =="SU" and array[117] > 0: array[117], array[65] = array[117] - 1, array[65] + 1
    if cmd =="SW" and array[195] > 0: array[195], array[108] = array[195] - 1, array[108] + 1
    if cmd =="SY" and array[293] > 0: array[293], array[224] = array[293] - 1, array[224] + 1
    if cmd =="SZ" and array[39] > 0: array[39], array[262] = array[39] - 1, array[262] + 1
    if cmd =="TA" and array[45] > 0: array[45], array[67] = array[45] - 1, array[67] + 1
    if cmd =="TC" and array[275] > 0: array[275], array[79] = array[275] - 1, array[79] + 1
    if cmd =="TK" and array[289] > 0: array[289], array[93] = array[289] - 1, array[93] + 1
    if cmd =="TV" and array[257] > 0: array[257], array[192] = array[257] - 1, array[192] + 1
    if cmd =="TX" and array[229] > 0: array[229], array[63] = array[229] - 1, array[63] + 1
    if cmd =="TY" and array[214] > 0: array[214], array[61] = array[214] - 1, array[61] + 1
    if cmd =="UA" and array[146] > 0: array[146], array[96] = array[146] - 1, array[96] + 1
    if cmd =="UC" and array[215] > 0: array[215], array[261] = array[215] - 1, array[261] + 1
    if cmd =="UE" and array[230] > 0: array[230], array[146] = array[230] - 1, array[146] + 1
    if cmd =="UH" and array[32] > 0: array[32], array[189] = array[32] - 1, array[189] + 1
    if cmd =="UK" and array[193] > 0: array[193], array[297] = array[193] - 1, array[297] + 1
    if cmd =="UM" and array[217] > 0: array[217], array[229] = array[217] - 1, array[229] + 1
    if cmd =="UQ" and array[196] > 0: array[196], array[221] = array[196] - 1, array[221] + 1
    if cmd =="UR" and array[9] > 0: array[9], array[286] = array[9] - 1, array[286] + 1
    if cmd =="UT" and array[120] > 0: array[120], array[285] = array[120] - 1, array[285] + 1
    if cmd =="UY" and array[132] > 0: array[132], array[311] = array[132] - 1, array[311] + 1
    if cmd =="UZ" and array[299] > 0: array[299], array[241] = array[299] - 1, array[241] + 1
    if cmd =="VA" and array[256] > 0: array[256], array[166] = array[256] - 1, array[166] + 1
    if cmd =="VB" and array[297] > 0: array[297], array[231] = array[297] - 1, array[231] + 1
    if cmd =="VC" and array[70] > 0: array[70], array[314] = array[70] - 1, array[314] + 1
    if cmd =="VD" and array[173] > 0: array[173], array[227] = array[173] - 1, array[227] + 1
    if cmd =="VE" and array[211] > 0: array[211], array[169] = array[211] - 1, array[169] + 1
    if cmd =="VF" and array[174] > 0: array[174], array[214] = array[174] - 1, array[214] + 1
    if cmd =="VG" and array[236] > 0: array[236], array[19] = array[236] - 1, array[19] + 1
    if cmd =="VH" and array[110] > 0: array[110], array[270] = array[110] - 1, array[270] + 1
    if cmd =="VK" and array[231] > 0: array[231], array[226] = array[231] - 1, array[226] + 1
    if cmd =="VM" and array[101] > 0: array[101], array[45] = array[101] - 1, array[45] + 1
    if cmd =="VO" and array[269] > 0: array[269], array[85] = array[269] - 1, array[85] + 1
    if cmd =="VP" and array[92] > 0: array[92], array[179] = array[92] - 1, array[179] + 1
    if cmd =="VR" and array[52] > 0: array[52], array[47] = array[52] - 1, array[47] + 1
    if cmd =="VS" and array[168] > 0: array[168], array[242] = array[168] - 1, array[242] + 1
    if cmd =="VT" and array[184] > 0: array[184], array[263] = array[184] - 1, array[263] + 1
    if cmd =="VU" and array[156] > 0: array[156], array[252] = array[156] - 1, array[252] + 1
    if cmd =="VW" and array[107] > 0: array[107], array[240] = array[107] - 1, array[240] + 1
    if cmd =="VY" and array[171] > 0: array[171], array[315] = array[171] - 1, array[315] + 1
    if cmd =="WA" and array[291] > 0: array[291], array[15] = array[291] - 1, array[15] + 1
    if cmd =="WB" and array[112] > 0: array[112], array[92] = array[112] - 1, array[92] + 1
    if cmd =="WC" and array[162] > 0: array[162], array[87] = array[162] - 1, array[87] + 1
    if cmd =="WE" and array[207] > 0: array[207], array[256] = array[207] - 1, array[256] + 1
    if cmd =="WH" and array[100] > 0: array[100], array[157] = array[100] - 1, array[157] + 1
    if cmd =="WI" and array[99] > 0: array[99], array[251] = array[99] - 1, array[251] + 1
    if cmd =="WJ" and array[121] > 0: array[121], array[90] = array[121] - 1, array[90] + 1
    if cmd =="WK" and array[292] > 0: array[292], array[137] = array[292] - 1, array[137] + 1
    if cmd =="WL" and array[123] > 0: array[123], array[184] = array[123] - 1, array[184] + 1
    if cmd =="WM" and array[75] > 0: array[75], array[301] = array[75] - 1, array[301] + 1
    if cmd =="WN" and array[226] > 0: array[226], array[60] = array[226] - 1, array[60] + 1
    if cmd =="WP" and array[117] > 0: array[117], array[275] = array[117] - 1, array[275] + 1
    if cmd =="WQ" and array[195] > 0: array[195], array[40] = array[195] - 1, array[40] + 1
    if cmd =="WT" and array[293] > 0: array[293], array[204] = array[293] - 1, array[204] + 1
    if cmd =="WV" and array[39] > 0: array[39], array[168] = array[39] - 1, array[168] + 1
    if cmd =="WY" and array[45] > 0: array[45], array[100] = array[45] - 1, array[100] + 1
    if cmd =="WZ" and array[183] > 0: array[183], array[111] = array[183] - 1, array[111] + 1
    if cmd =="XA" and array[0] > 0: array[0], array[298] = array[0] - 1, array[298] + 1
    if cmd =="XB" and array[233] > 0: array[233], array[148] = array[233] - 1, array[148] + 1
    if cmd =="XC" and array[278] > 0: array[278], array[78] = array[278] - 1, array[78] + 1
    if cmd =="XD" and array[114] > 0: array[114], array[237] = array[114] - 1, array[237] + 1
    if cmd =="XE" and array[130] > 0: array[130], array[205] = array[130] - 1, array[205] + 1
    if cmd =="XH" and array[129] > 0: array[129], array[107] = array[129] - 1, array[107] + 1
    if cmd =="XI" and array[43] > 0: array[43], array[183] = array[43] - 1, array[183] + 1
    if cmd =="XJ" and array[106] > 0: array[106], array[104] = array[106] - 1, array[104] + 1
    if cmd =="XK" and array[180] > 0: array[180], array[238] = array[180] - 1, array[238] + 1
    if cmd =="XM" and array[72] > 0: array[72], array[246] = array[72] - 1, array[246] + 1
    if cmd =="XS" and array[155] > 0: array[155], array[198] = array[155] - 1, array[198] + 1
    if cmd =="XV" and array[279] > 0: array[279], array[307] = array[279] - 1, array[307] + 1
    if cmd =="XW" and array[89] > 0: array[89], array[304] = array[89] - 1, array[304] + 1
    if cmd =="XZ" and array[85] > 0: array[85], array[71] = array[85] - 1, array[71] + 1
    if cmd =="YA" and array[201] > 0: array[201], array[282] = array[201] - 1, array[282] + 1
    if cmd =="YB" and array[313] > 0: array[313], array[290] = array[313] - 1, array[290] + 1
    if cmd =="YC" and array[175] > 0: array[175], array[258] = array[175] - 1, array[258] + 1
    if cmd =="YD" and array[53] > 0: array[53], array[273] = array[53] - 1, array[273] + 1
    if cmd =="YE" and array[197] > 0: array[197], array[203] = array[197] - 1, array[203] + 1
    if cmd =="YH" and array[96] > 0: array[96], array[128] = array[96] - 1, array[128] + 1
    if cmd =="YI" and array[10] > 0: array[10], array[43] = array[10] - 1, array[43] + 1
    if cmd =="YJ" and array[138] > 0: array[138], array[294] = array[138] - 1, array[294] + 1
    if cmd =="YK" and array[139] > 0: array[139], array[30] = array[139] - 1, array[30] + 1
    if cmd =="YL" and array[247] > 0: array[247], array[269] = array[247] - 1, array[269] + 1
    if cmd =="YM" and array[170] > 0: array[170], array[58] = array[170] - 1, array[58] + 1
    if cmd =="YN" and array[308] > 0: array[308], array[64] = array[308] - 1, array[64] + 1
    if cmd =="YO" and array[202] > 0: array[202], array[313] = array[202] - 1, array[313] + 1
    if cmd =="YP" and array[266] > 0: array[266], array[34] = array[266] - 1, array[34] + 1
    if cmd =="YQ" and array[74] > 0: array[74], array[54] = array[74] - 1, array[54] + 1
    if cmd =="YR" and array[288] > 0: array[288], array[302] = array[288] - 1, array[302] + 1
    if cmd =="YS" and array[208] > 0: array[208], array[272] = array[208] - 1, array[272] + 1
    if cmd =="YT" and array[280] > 0: array[280], array[164] = array[280] - 1, array[164] + 1
    if cmd =="YV" and array[12] > 0: array[12], array[113] = array[12] - 1, array[113] + 1
    if cmd =="YW" and array[238] > 0: array[238], array[44] = array[238] - 1, array[44] + 1
    if cmd =="YZ" and array[240] > 0: array[240], array[129] = array[240] - 1, array[129] + 1
    if cmd =="ZA" and array[33] > 0: array[33], array[197] = array[33] - 1, array[197] + 1
    if cmd =="ZB" and array[301] > 0: array[301], array[260] = array[301] - 1, array[260] + 1
    if cmd =="ZD" and array[36] > 0: array[36], array[83] = array[36] - 1, array[83] + 1
    if cmd =="ZE" and array[241] > 0: array[241], array[312] = array[241] - 1, array[312] + 1
    if cmd =="ZF" and array[263] > 0: array[263], array[2] = array[263] - 1, array[2] + 1
    if cmd =="ZG" and array[225] > 0: array[225], array[195] = array[225] - 1, array[195] + 1
    if cmd =="ZH" and array[203] > 0: array[203], array[18] = array[203] - 1, array[18] + 1
    if cmd =="ZI" and array[18] > 0: array[18], array[178] = array[18] - 1, array[178] + 1
    if cmd =="ZJ" and array[81] > 0: array[81], array[295] = array[81] - 1, array[295] + 1
    if cmd =="ZM" and array[17] > 0: array[17], array[57] = array[17] - 1, array[57] + 1
    if cmd =="ZN" and array[127] > 0: array[127], array[185] = array[127] - 1, array[185] + 1
    if cmd =="ZP" and array[77] > 0: array[77], array[289] = array[77] - 1, array[289] + 1
    if cmd =="ZQ" and array[187] > 0: array[187], array[194] = array[187] - 1, array[194] + 1
    if cmd =="ZR" and array[41] > 0: array[41], array[255] = array[41] - 1, array[255] + 1
    if cmd =="ZS" and array[179] > 0: array[179], array[103] = array[179] - 1, array[103] + 1
    if cmd =="ZV" and array[135] > 0: array[135], array[116] = array[135] - 1, array[116] + 1
    if cmd =="ZW" and array[131] > 0: array[131], array[5] = array[131] - 1, array[5] + 1
    if cmd =="ZX" and array[24] > 0: array[24], array[208] = array[24] - 1, array[208] + 1
    if cmd =="ZY" and array[10] > 0: array[10], array[287] = array[10] - 1, array[287] + 1
    return (array, apointer, inputdata, output, source, spointer)


def perception_gene(array, apointer, inputdata, output, source, spointer):
    """
    Default handler for the set of 68 perception genes that perceive the environment.
    """
    cmd = source[spointer: spointer + codon_length]
    if cmd == "AL": array[282] = array[282] + (inputdata[62] * 0.01)
    if cmd == "AN": array[120] = array[120] + (inputdata[66] * 0.01)
    if cmd == "BA": array[98] = array[98] + (inputdata[1] * 0.01)
    if cmd == "BZ": array[119] = array[119] + (inputdata[29] * 0.01)
    if cmd == "CG": array[191] = array[191] + (inputdata[4] * 0.01)
    if cmd == "CI": array[300] = array[300] + (inputdata[42] * 0.01)
    if cmd == "CR": array[279] = array[279] + (inputdata[17] * 0.01)
    if cmd == "CX": array[0] = array[0] + (inputdata[32] * 0.01)
    if cmd == "DF": array[144] = array[144] + (inputdata[18] * 0.01)
    if cmd == "DZ": array[215] = array[215] + (inputdata[63] * 0.01)
    if cmd == "EC": array[312] = array[312] + (inputdata[59] * 0.01)
    if cmd == "EJ": array[210] = array[210] + (inputdata[43] * 0.01)
    if cmd == "FA": array[267] = array[267] + (inputdata[46] * 0.01)
    if cmd == "GA": array[225] = array[225] + (inputdata[34] * 0.01)
    if cmd == "GI": array[171] = array[171] + (inputdata[35] * 0.01)
    if cmd == "GK": array[175] = array[175] + (inputdata[51] * 0.01)
    if cmd == "HB": array[220] = array[220] + (inputdata[48] * 0.01)
    if cmd == "HI": array[284] = array[284] + (inputdata[36] * 0.01)
    if cmd == "HJ": array[237] = array[237] + (inputdata[57] * 0.01)
    if cmd == "IP": array[144] = array[144] + (inputdata[58] * 0.01)
    if cmd == "JB": array[268] = array[268] + (inputdata[2] * 0.01)
    if cmd == "JH": array[110] = array[110] + (inputdata[50] * 0.01)
    if cmd == "JV": array[303] = array[303] + (inputdata[27] * 0.01)
    if cmd == "KA": array[102] = array[102] + (inputdata[6] * 0.01)
    if cmd == "KC": array[223] = array[223] + (inputdata[5] * 0.01)
    if cmd == "KN": array[1] = array[1] + (inputdata[45] * 0.01)
    if cmd == "KO": array[264] = array[264] + (inputdata[52] * 0.01)
    if cmd == "LG": array[262] = array[262] + (inputdata[0] * 0.01)
    if cmd == "LI": array[5] = array[5] + (inputdata[9] * 0.01)
    if cmd == "LW": array[261] = array[261] + (inputdata[39] * 0.01)
    if cmd == "LX": array[66] = array[66] + (inputdata[30] * 0.01)
    if cmd == "MD": array[6] = array[6] + (inputdata[16] * 0.01)
    if cmd == "ME": array[279] = array[279] + (inputdata[41] * 0.01)
    if cmd == "NM": array[171] = array[171] + (inputdata[19] * 0.01)
    if cmd == "NO": array[174] = array[174] + (inputdata[60] * 0.01)
    if cmd == "OR": array[182] = array[182] + (inputdata[7] * 0.01)
    if cmd == "PE": array[255] = array[255] + (inputdata[8] * 0.01)
    if cmd == "QG": array[129] = array[129] + (inputdata[53] * 0.01)
    if cmd == "QH": array[26] = array[26] + (inputdata[3] * 0.01)
    if cmd == "RB": array[61] = array[61] + (inputdata[26] * 0.01)
    if cmd == "RE": array[245] = array[245] + (inputdata[37] * 0.01)
    if cmd == "RN": array[223] = array[223] + (inputdata[31] * 0.01)
    if cmd == "SD": array[32] = array[32] + (inputdata[54] * 0.01)
    if cmd == "SG": array[68] = array[68] + (inputdata[10] * 0.01)
    if cmd == "SO": array[136] = array[136] + (inputdata[15] * 0.01)
    if cmd == "SR": array[198] = array[198] + (inputdata[47] * 0.01)
    if cmd == "SV": array[240] = array[240] + (inputdata[55] * 0.01)
    if cmd == "TB": array[144] = array[144] + (inputdata[61] * 0.01)
    if cmd == "TM": array[272] = array[272] + (inputdata[38] * 0.01)
    if cmd == "TQ": array[31] = array[31] + (inputdata[67] * 0.01)
    if cmd == "UB": array[157] = array[157] + (inputdata[23] * 0.01)
    if cmd == "UD": array[86] = array[86] + (inputdata[24] * 0.01)
    if cmd == "UF": array[249] = array[249] + (inputdata[21] * 0.01)
    if cmd == "UG": array[74] = array[74] + (inputdata[33] * 0.01)
    if cmd == "UJ": array[148] = array[148] + (inputdata[22] * 0.01)
    if cmd == "UL": array[244] = array[244] + (inputdata[56] * 0.01)
    if cmd == "UN": array[80] = array[80] + (inputdata[11] * 0.01)
    if cmd == "VZ": array[248] = array[248] + (inputdata[12] * 0.01)
    if cmd == "WD": array[181] = array[181] + (inputdata[28] * 0.01)
    if cmd == "WF": array[33] = array[33] + (inputdata[40] * 0.01)
    if cmd == "WG": array[300] = array[300] + (inputdata[14] * 0.01)
    if cmd == "WO": array[120] = array[120] + (inputdata[65] * 0.01)
    if cmd == "WR": array[229] = array[229] + (inputdata[49] * 0.01)
    if cmd == "XY": array[163] = array[163] + (inputdata[13] * 0.01)
    if cmd == "YF": array[292] = array[292] + (inputdata[25] * 0.01)
    if cmd == "YU": array[304] = array[304] + (inputdata[44] * 0.01)
    if cmd == "ZO": array[209] = array[209] + (inputdata[64] * 0.01)
    if cmd == "ZT": array[182] = array[182] + (inputdata[20] * 0.01)
    return (array, apointer, inputdata, output, source, spointer)


def undefined_gene(array, apointer, inputdata, output, source, spointer):
    """
    Default handler for the 176 unimplemented instructions symbolizing undefined
    (do-nothing) genes.
    """
    cmd = source[spointer: spointer + codon_length]
    if cmd in ["AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX",
               "BD", "BG", "BJ", "BU", "BX", "DJ", "DK", "DO", "DP",
               "DQ", "DR", "DT", "DU", "DW", "DX", "EL", "EN", "EO",
               "EZ", "FD", "FE", "FI", "FJ", "FL", "FM", "FN", "FO",
               "FP", "FS", "FT", "FV", "FW", "FY", "GP", "GT", "GV",
               "GW", "GX", "GZ", "HL", "HM", "HN", "HO", "HR", "HU",
               "HV", "HY", "HZ", "IA", "IB", "ID", "IF", "IG", "IK",
               "IL", "IS", "IY", "JK", "JM", "JT", "KE", "KG", "KI",
               "KS", "KT", "KW", "KX", "KZ", "LY", "MH", "MK", "MP",
               "MS", "MV", "MZ", "NB", "NC", "ND", "NF", "NG", "NK",
               "NL", "NP", "NS", "NU", "NV", "NX", "NZ", "OD", "OG",
               "ON", "OS", "OU", "OV", "PF", "PH", "PI", "PJ", "PL",
               "PR", "PS", "PU", "PV", "PX", "PY", "QL", "QO", "QP",
               "QR", "QS", "QU", "QV", "QW", "QY", "RG", "RI", "RK",
               "RV", "SX", "TD", "TE", "TF", "TG", "TH", "TI", "TJ",
               "TL", "TN", "TO", "TP", "TR", "TS", "TU", "TW", "TZ",
               "UI", "UO", "UP", "US", "UV", "UW", "UX", "VI", "VJ",
               "VL", "VN", "VQ", "VX", "WS", "WU", "WX", "XF", "XG",
               "XL", "XN", "XO", "XP", "XQ", "XR", "XT", "XU", "YG",
               "YX", "ZC", "ZK", "ZL", "ZU"]:
        pass
    return (array, apointer, inputdata, output, source, spointer)


interpreter = {"AA": reserved_gene,   "AB": enzymatic_gene,  "AC": enzymatic_gene,  "AD": enzymatic_gene,
               "AE": enzymatic_gene,  "AF": enzymatic_gene,  "AG": enzymatic_gene,  "AH": enzymatic_gene,
               "AI": enzymatic_gene,  "AJ": enzymatic_gene,  "AK": enzymatic_gene,  "AL": perception_gene,
               "AM": enzymatic_gene,  "AN": perception_gene, "AO": enzymatic_gene,  "AP": undefined_gene,
               "AQ": undefined_gene,  "AR": undefined_gene,  "AS": undefined_gene,  "AT": undefined_gene,
               "AU": undefined_gene,  "AV": undefined_gene,  "AW": undefined_gene,  "AX": undefined_gene,
               "AY": enzymatic_gene,  "AZ": enzymatic_gene,  "BA": perception_gene, "BB": reserved_gene,
               "BC": enzymatic_gene,  "BD": undefined_gene,  "BE": enzymatic_gene,  "BF": enzymatic_gene,
               "BG": undefined_gene,  "BH": enzymatic_gene,  "BI": enzymatic_gene,  "BJ": undefined_gene,
               "BK": enzymatic_gene,  "BL": enzymatic_gene,  "BM": enzymatic_gene,  "BN": enzymatic_gene,
               "BO": enzymatic_gene,  "BP": enzymatic_gene,  "BQ": enzymatic_gene,  "BR": enzymatic_gene,
               "BS": enzymatic_gene,  "BT": enzymatic_gene,  "BU": undefined_gene,  "BV": enzymatic_gene,
               "BW": enzymatic_gene,  "BX": undefined_gene,  "BY": enzymatic_gene,  "BZ": perception_gene,
               "CA": enzymatic_gene,  "CB": enzymatic_gene,  "CC": reserved_gene,   "CD": enzymatic_gene,
               "CE": enzymatic_gene,  "CF": enzymatic_gene,  "CG": perception_gene, "CH": enzymatic_gene,
               "CI": perception_gene, "CJ": enzymatic_gene,  "CK": enzymatic_gene,  "CL": enzymatic_gene,
               "CM": enzymatic_gene,  "CN": enzymatic_gene,  "CO": enzymatic_gene,  "CP": enzymatic_gene,
               "CQ": enzymatic_gene,  "CR": perception_gene, "CS": enzymatic_gene,  "CT": enzymatic_gene,
               "CU": enzymatic_gene,  "CV": enzymatic_gene,  "CW": enzymatic_gene,  "CX": perception_gene,
               "CY": enzymatic_gene,  "CZ": enzymatic_gene,  "DA": enzymatic_gene,  "DB": enzymatic_gene,
               "DC": enzymatic_gene,  "DD": reserved_gene,   "DE": enzymatic_gene,  "DF": perception_gene,
               "DG": enzymatic_gene,  "DH": enzymatic_gene,  "DI": enzymatic_gene,  "DJ": undefined_gene,
               "DK": undefined_gene,  "DL": enzymatic_gene,  "DM": enzymatic_gene,  "DN": enzymatic_gene,
               "DO": undefined_gene,  "DP": undefined_gene,  "DQ": undefined_gene,  "DR": undefined_gene,
               "DS": enzymatic_gene,  "DT": undefined_gene,  "DU": undefined_gene,  "DV": enzymatic_gene,
               "DW": undefined_gene,  "DX": undefined_gene,  "DY": enzymatic_gene,  "DZ": perception_gene,
               "EA": enzymatic_gene,  "EB": enzymatic_gene,  "EC": perception_gene, "ED": enzymatic_gene,
               "EE": reserved_gene,   "EF": enzymatic_gene,  "EG": enzymatic_gene,  "EH": enzymatic_gene,
               "EI": enzymatic_gene,  "EJ": perception_gene, "EK": enzymatic_gene,  "EL": undefined_gene,
               "EM": enzymatic_gene,  "EN": undefined_gene,  "EO": undefined_gene,  "EP": enzymatic_gene,
               "EQ": enzymatic_gene,  "ER": enzymatic_gene,  "ES": enzymatic_gene,  "ET": enzymatic_gene,
               "EU": enzymatic_gene,  "EV": enzymatic_gene,  "EW": enzymatic_gene,  "EX": enzymatic_gene,
               "EY": enzymatic_gene,  "EZ": undefined_gene,  "FA": perception_gene, "FB": enzymatic_gene,
               "FC": enzymatic_gene,  "FD": undefined_gene,  "FE": undefined_gene,  "FF": reserved_gene,
               "FG": enzymatic_gene,  "FH": enzymatic_gene,  "FI": undefined_gene,  "FJ": undefined_gene,
               "FK": enzymatic_gene,  "FL": undefined_gene,  "FM": undefined_gene,  "FN": undefined_gene,
               "FO": undefined_gene,  "FP": undefined_gene,  "FQ": enzymatic_gene,  "FR": enzymatic_gene,
               "FS": undefined_gene,  "FT": undefined_gene,  "FU": enzymatic_gene,  "FV": undefined_gene,
               "FW": undefined_gene,  "FX": enzymatic_gene,  "FY": undefined_gene,  "FZ": enzymatic_gene,
               "GA": perception_gene, "GB": enzymatic_gene,  "GC": enzymatic_gene,  "GD": enzymatic_gene,
               "GE": enzymatic_gene,  "GF": enzymatic_gene,  "GG": reserved_gene,   "GH": enzymatic_gene,
               "GI": perception_gene, "GJ": enzymatic_gene,  "GK": perception_gene, "GL": enzymatic_gene,
               "GM": enzymatic_gene,  "GN": enzymatic_gene,  "GO": enzymatic_gene,  "GP": undefined_gene,
               "GQ": enzymatic_gene,  "GR": enzymatic_gene,  "GS": enzymatic_gene,  "GT": undefined_gene,
               "GU": enzymatic_gene,  "GV": undefined_gene,  "GW": undefined_gene,  "GX": undefined_gene,
               "GY": enzymatic_gene,  "GZ": undefined_gene,  "HA": enzymatic_gene,  "HB": perception_gene,
               "HC": enzymatic_gene,  "HD": enzymatic_gene,  "HE": enzymatic_gene,  "HF": enzymatic_gene,
               "HG": enzymatic_gene,  "HH": reserved_gene,   "HI": perception_gene, "HJ": perception_gene,
               "HK": enzymatic_gene,  "HL": undefined_gene,  "HM": undefined_gene,  "HN": undefined_gene,
               "HO": undefined_gene,  "HP": enzymatic_gene,  "HQ": enzymatic_gene,  "HR": undefined_gene,
               "HS": enzymatic_gene,  "HT": enzymatic_gene,  "HU": undefined_gene,  "HV": undefined_gene,
               "HW": enzymatic_gene,  "HX": enzymatic_gene,  "HY": undefined_gene,  "HZ": undefined_gene,
               "IA": undefined_gene,  "IB": undefined_gene,  "IC": enzymatic_gene,  "ID": undefined_gene,
               "IE": enzymatic_gene,  "IF": undefined_gene,  "IG": undefined_gene,  "IH": enzymatic_gene,
               "II": reserved_gene,   "IJ": enzymatic_gene,  "IK": undefined_gene,  "IL": undefined_gene,
               "IM": enzymatic_gene,  "IN": enzymatic_gene,  "IO": enzymatic_gene,  "IP": perception_gene,
               "IQ": enzymatic_gene,  "IR": enzymatic_gene,  "IS": undefined_gene,  "IT": enzymatic_gene,
               "IU": enzymatic_gene,  "IV": enzymatic_gene,  "IW": enzymatic_gene,  "IX": enzymatic_gene,
               "IY": undefined_gene,  "IZ": enzymatic_gene,  "JA": enzymatic_gene,  "JB": perception_gene,
               "JC": enzymatic_gene,  "JD": enzymatic_gene,  "JE": enzymatic_gene,  "JF": enzymatic_gene,
               "JG": enzymatic_gene,  "JH": perception_gene, "JI": enzymatic_gene,  "JJ": reserved_gene,
               "JK": undefined_gene,  "JL": enzymatic_gene,  "JM": undefined_gene,  "JN": enzymatic_gene,
               "JO": enzymatic_gene,  "JP": enzymatic_gene,  "JQ": enzymatic_gene,  "JR": enzymatic_gene,
               "JS": enzymatic_gene,  "JT": undefined_gene,  "JU": enzymatic_gene,  "JV": perception_gene,
               "JW": enzymatic_gene,  "JX": enzymatic_gene,  "JY": enzymatic_gene,  "JZ": enzymatic_gene,
               "KA": perception_gene, "KB": enzymatic_gene,  "KC": perception_gene, "KD": enzymatic_gene,
               "KE": undefined_gene,  "KF": enzymatic_gene,  "KG": undefined_gene,  "KH": enzymatic_gene,
               "KI": undefined_gene,  "KJ": enzymatic_gene,  "KK": reserved_gene,   "KL": enzymatic_gene,
               "KM": enzymatic_gene,  "KN": perception_gene, "KO": perception_gene, "KP": enzymatic_gene,
               "KQ": enzymatic_gene,  "KR": enzymatic_gene,  "KS": undefined_gene,  "KT": undefined_gene,
               "KU": enzymatic_gene,  "KV": enzymatic_gene,  "KW": undefined_gene,  "KX": undefined_gene,
               "KY": enzymatic_gene,  "KZ": undefined_gene,  "LA": enzymatic_gene,  "LB": enzymatic_gene,
               "LC": enzymatic_gene,  "LD": enzymatic_gene,  "LE": enzymatic_gene,  "LF": enzymatic_gene,
               "LG": perception_gene, "LH": enzymatic_gene,  "LI": perception_gene, "LJ": enzymatic_gene,
               "LK": enzymatic_gene,  "LL": reserved_gene,   "LM": enzymatic_gene,  "LN": enzymatic_gene,
               "LO": enzymatic_gene,  "LP": enzymatic_gene,  "LQ": enzymatic_gene,  "LR": enzymatic_gene,
               "LS": enzymatic_gene,  "LT": enzymatic_gene,  "LU": enzymatic_gene,  "LV": enzymatic_gene,
               "LW": perception_gene, "LX": perception_gene, "LY": undefined_gene,  "LZ": enzymatic_gene,
               "MA": enzymatic_gene,  "MB": enzymatic_gene,  "MC": enzymatic_gene,  "MD": perception_gene,
               "ME": perception_gene, "MF": enzymatic_gene,  "MG": enzymatic_gene,  "MH": undefined_gene,
               "MI": enzymatic_gene,  "MJ": enzymatic_gene,  "MK": undefined_gene,  "ML": enzymatic_gene,
               "MM": reserved_gene,   "MN": enzymatic_gene,  "MO": enzymatic_gene,  "MP": undefined_gene,
               "MQ": enzymatic_gene,  "MR": enzymatic_gene,  "MS": undefined_gene,  "MT": enzymatic_gene,
               "MU": enzymatic_gene,  "MV": undefined_gene,  "MW": enzymatic_gene,  "MX": enzymatic_gene,
               "MY": enzymatic_gene,  "MZ": undefined_gene,  "NA": enzymatic_gene,  "NB": undefined_gene,
               "NC": undefined_gene,  "ND": undefined_gene,  "NE": enzymatic_gene,  "NF": undefined_gene,
               "NG": undefined_gene,  "NH": enzymatic_gene,  "NI": enzymatic_gene,  "NJ": enzymatic_gene,
               "NK": undefined_gene,  "NL": undefined_gene,  "NM": perception_gene, "NN": reserved_gene,
               "NO": perception_gene, "NP": undefined_gene,  "NQ": enzymatic_gene,  "NR": enzymatic_gene,
               "NS": undefined_gene,  "NT": enzymatic_gene,  "NU": undefined_gene,  "NV": undefined_gene,
               "NW": enzymatic_gene,  "NX": undefined_gene,  "NY": enzymatic_gene,  "NZ": undefined_gene,
               "OA": enzymatic_gene,  "OB": enzymatic_gene,  "OC": enzymatic_gene,  "OD": undefined_gene,
               "OE": enzymatic_gene,  "OF": enzymatic_gene,  "OG": undefined_gene,  "OH": enzymatic_gene,
               "OI": enzymatic_gene,  "OJ": enzymatic_gene,  "OK": enzymatic_gene,  "OL": enzymatic_gene,
               "OM": enzymatic_gene,  "ON": undefined_gene,  "OO": reserved_gene,   "OP": enzymatic_gene,
               "OQ": enzymatic_gene,  "OR": perception_gene, "OS": undefined_gene,  "OT": enzymatic_gene,
               "OU": undefined_gene,  "OV": undefined_gene,  "OW": enzymatic_gene,  "OX": enzymatic_gene,
               "OY": enzymatic_gene,  "OZ": enzymatic_gene,  "PA": enzymatic_gene,  "PB": enzymatic_gene,
               "PC": enzymatic_gene,  "PD": enzymatic_gene,  "PE": perception_gene, "PF": undefined_gene,
               "PG": enzymatic_gene,  "PH": undefined_gene,  "PI": undefined_gene,  "PJ": undefined_gene,
               "PK": enzymatic_gene,  "PL": undefined_gene,  "PM": enzymatic_gene,  "PN": enzymatic_gene,
               "PO": enzymatic_gene,  "PP": reserved_gene,   "PQ": enzymatic_gene,  "PR": undefined_gene,
               "PS": undefined_gene,  "PT": enzymatic_gene,  "PU": undefined_gene,  "PV": undefined_gene,
               "PW": enzymatic_gene,  "PX": undefined_gene,  "PY": undefined_gene,  "PZ": enzymatic_gene,
               "QA": enzymatic_gene,  "QB": enzymatic_gene,  "QC": enzymatic_gene,  "QD": enzymatic_gene,
               "QE": enzymatic_gene,  "QF": enzymatic_gene,  "QG": perception_gene, "QH": perception_gene,
               "QI": enzymatic_gene,  "QJ": enzymatic_gene,  "QK": enzymatic_gene,  "QL": undefined_gene,
               "QM": enzymatic_gene,  "QN": enzymatic_gene,  "QO": undefined_gene,  "QP": undefined_gene,
               "QQ": reserved_gene,   "QR": undefined_gene,  "QS": undefined_gene,  "QT": enzymatic_gene,
               "QU": undefined_gene,  "QV": undefined_gene,  "QW": undefined_gene,  "QX": enzymatic_gene,
               "QY": undefined_gene,  "QZ": enzymatic_gene,  "RA": enzymatic_gene,  "RB": perception_gene,
               "RC": enzymatic_gene,  "RD": enzymatic_gene,  "RE": perception_gene, "RF": enzymatic_gene,
               "RG": undefined_gene,  "RH": enzymatic_gene,  "RI": undefined_gene,  "RJ": enzymatic_gene,
               "RK": undefined_gene,  "RL": enzymatic_gene,  "RM": enzymatic_gene,  "RN": perception_gene,
               "RO": enzymatic_gene,  "RP": enzymatic_gene,  "RQ": enzymatic_gene,  "RR": reserved_gene,
               "RS": enzymatic_gene,  "RT": enzymatic_gene,  "RU": enzymatic_gene,  "RV": undefined_gene,
               "RW": enzymatic_gene,  "RX": enzymatic_gene,  "RY": enzymatic_gene,  "RZ": enzymatic_gene,
               "SA": enzymatic_gene,  "SB": enzymatic_gene,  "SC": enzymatic_gene,  "SD": perception_gene,
               "SE": enzymatic_gene,  "SF": enzymatic_gene,  "SG": perception_gene, "SH": enzymatic_gene,
               "SI": enzymatic_gene,  "SJ": enzymatic_gene,  "SK": enzymatic_gene,  "SL": enzymatic_gene,
               "SM": enzymatic_gene,  "SN": enzymatic_gene,  "SO": perception_gene, "SP": enzymatic_gene,
               "SQ": enzymatic_gene,  "SR": perception_gene, "SS": reserved_gene,   "ST": enzymatic_gene,
               "SU": enzymatic_gene,  "SV": perception_gene, "SW": enzymatic_gene,  "SX": undefined_gene,
               "SY": enzymatic_gene,  "SZ": enzymatic_gene,  "TA": enzymatic_gene,  "TB": perception_gene,
               "TC": enzymatic_gene,  "TD": undefined_gene,  "TE": undefined_gene,  "TF": undefined_gene,
               "TG": undefined_gene,  "TH": undefined_gene,  "TI": undefined_gene,  "TJ": undefined_gene,
               "TK": enzymatic_gene,  "TL": undefined_gene,  "TM": perception_gene, "TN": undefined_gene,
               "TO": undefined_gene,  "TP": undefined_gene,  "TQ": perception_gene, "TR": undefined_gene,
               "TS": undefined_gene,  "TT": reserved_gene,   "TU": undefined_gene,  "TV": enzymatic_gene,
               "TW": undefined_gene,  "TX": enzymatic_gene,  "TY": enzymatic_gene,  "TZ": undefined_gene,
               "UA": enzymatic_gene,  "UB": perception_gene, "UC": enzymatic_gene,  "UD": perception_gene,
               "UE": enzymatic_gene,  "UF": perception_gene, "UG": perception_gene, "UH": enzymatic_gene,
               "UI": undefined_gene,  "UJ": perception_gene, "UK": enzymatic_gene,  "UL": perception_gene,
               "UM": enzymatic_gene,  "UN": perception_gene, "UO": undefined_gene,  "UP": undefined_gene,
               "UQ": enzymatic_gene,  "UR": enzymatic_gene,  "US": undefined_gene,  "UT": enzymatic_gene,
               "UU": reserved_gene,   "UV": undefined_gene,  "UW": undefined_gene,  "UX": undefined_gene,
               "UY": enzymatic_gene,  "UZ": enzymatic_gene,  "VA": enzymatic_gene,  "VB": enzymatic_gene,
               "VC": enzymatic_gene,  "VD": enzymatic_gene,  "VE": enzymatic_gene,  "VF": enzymatic_gene,
               "VG": enzymatic_gene,  "VH": enzymatic_gene,  "VI": undefined_gene,  "VJ": undefined_gene,
               "VK": enzymatic_gene,  "VL": undefined_gene,  "VM": enzymatic_gene,  "VN": undefined_gene,
               "VO": enzymatic_gene,  "VP": enzymatic_gene,  "VQ": undefined_gene,  "VR": enzymatic_gene,
               "VS": enzymatic_gene,  "VT": enzymatic_gene,  "VU": enzymatic_gene,  "VV": reserved_gene,
               "VW": enzymatic_gene,  "VX": undefined_gene,  "VY": enzymatic_gene,  "VZ": perception_gene,
               "WA": enzymatic_gene,  "WB": enzymatic_gene,  "WC": enzymatic_gene,  "WD": perception_gene,
               "WE": enzymatic_gene,  "WF": perception_gene, "WG": perception_gene, "WH": enzymatic_gene,
               "WI": enzymatic_gene,  "WJ": enzymatic_gene,  "WK": enzymatic_gene,  "WL": enzymatic_gene,
               "WM": enzymatic_gene,  "WN": enzymatic_gene,  "WO": perception_gene, "WP": enzymatic_gene,
               "WQ": enzymatic_gene,  "WR": perception_gene, "WS": undefined_gene,  "WT": enzymatic_gene,
               "WU": undefined_gene,  "WV": enzymatic_gene,  "WW": reserved_gene,   "WX": undefined_gene,
               "WY": enzymatic_gene,  "WZ": enzymatic_gene,  "XA": enzymatic_gene,  "XB": enzymatic_gene,
               "XC": enzymatic_gene,  "XD": enzymatic_gene,  "XE": enzymatic_gene,  "XF": undefined_gene,
               "XG": undefined_gene,  "XH": enzymatic_gene,  "XI": enzymatic_gene,  "XJ": enzymatic_gene,
               "XK": enzymatic_gene,  "XL": undefined_gene,  "XM": enzymatic_gene,  "XN": undefined_gene,
               "XO": undefined_gene,  "XP": undefined_gene,  "XQ": undefined_gene,  "XR": undefined_gene,
               "XS": enzymatic_gene,  "XT": undefined_gene,  "XU": undefined_gene,  "XV": enzymatic_gene,
               "XW": enzymatic_gene,  "XX": reserved_gene,   "XY": perception_gene, "XZ": enzymatic_gene,
               "YA": enzymatic_gene,  "YB": enzymatic_gene,  "YC": enzymatic_gene,  "YD": enzymatic_gene,
               "YE": enzymatic_gene,  "YF": perception_gene, "YG": undefined_gene,  "YH": enzymatic_gene,
               "YI": enzymatic_gene,  "YJ": enzymatic_gene,  "YK": enzymatic_gene,  "YL": enzymatic_gene,
               "YM": enzymatic_gene,  "YN": enzymatic_gene,  "YO": enzymatic_gene,  "YP": enzymatic_gene,
               "YQ": enzymatic_gene,  "YR": enzymatic_gene,  "YS": enzymatic_gene,  "YT": enzymatic_gene,
               "YU": perception_gene, "YV": enzymatic_gene,  "YW": enzymatic_gene,  "YX": undefined_gene,
               "YY": reserved_gene,   "YZ": enzymatic_gene,  "ZA": enzymatic_gene,  "ZB": enzymatic_gene,
               "ZC": undefined_gene,  "ZD": enzymatic_gene,  "ZE": enzymatic_gene,  "ZF": enzymatic_gene,
               "ZG": enzymatic_gene,  "ZH": enzymatic_gene,  "ZI": enzymatic_gene,  "ZJ": enzymatic_gene,
               "ZK": undefined_gene,  "ZL": undefined_gene,  "ZM": enzymatic_gene,  "ZN": enzymatic_gene,
               "ZO": perception_gene, "ZP": enzymatic_gene,  "ZQ": enzymatic_gene,  "ZR": enzymatic_gene,
               "ZS": enzymatic_gene,  "ZT": perception_gene, "ZU": undefined_gene,  "ZV": enzymatic_gene,
               "ZW": enzymatic_gene,  "ZX": enzymatic_gene,  "ZY": enzymatic_gene,  "ZZ": reserved_gene}
