"""
ENZYMATIC REACTIONS, ENZYMATIC GENES & PERCEPTION GENES

"""

enzymatic_reactions = {
    "AB": ('M274', 'M77'), "AC": ('M162', 'M83'), "AD": ('M286', 'M108'),
    "AE": ('M183', 'M184'), "AF": ('M250', 'M105'), "AG": ('M103', 'M239'),
    "AH": ('M16', 'M247'), "AI": ('M277', 'M199'), "AJ": ('M94', 'M308'),
    "AK": ('M59', 'M305'), "AM": ('M125', 'M72'), "AO": ('M158', 'M283'),
    "AY": ('M300', 'M291'), "AZ": ('M257', 'M259'), "BC": ('M298', 'M274'),
    "BE": ('M71', 'M204'), "BF": ('M174', 'M129'), "BH": ('M212', 'M44'),
    "BI": ('M175', 'M295'), "BK": ('M237', 'M31'), "BL": ('M111', 'M270'),
    "BM": ('M232', 'M59'), "BN": ('M102', 'M65'), "BO": ('M55', 'M314'),
    "BP": ('M159', 'M35'), "BQ": ('M187', 'M55'), "BR": ('M210', 'M303'),
    "BS": ('M316', 'M273'), "BT": ('M41', 'M165'), "BV": ('M233', 'M114'),
    "BW": ('M287', 'M45'), "BY": ('M88', 'M130'), "CA": ('M304', 'M198'),
    "CB": ('M56', 'M261'), "CD": ('M263', 'M84'), "CE": ('M85', 'M187'),
    "CF": ('M146', 'M219'), "CH": ('M191', 'M69'), "CJ": ('M219', 'M36'),
    "CK": ('M253', 'M13'), "CL": ('M127', 'M30'), "CM": ('M65', 'M53'),
    "CN": ('M24', 'M12'), "CO": ('M150', 'M103'), "CP": ('M221', 'M73'),
    "CQ": ('M213', 'M26'), "CS": ('M178', 'M23'), "CT": ('M153', 'M146'),
    "CU": ('M116', 'M9'), "CV": ('M81', 'M34'), "CW": ('M51', 'M224'),
    "CY": ('M7', 'M208'), "CZ": ('M266', 'M181'), "DA": ('M144', 'M218'),
    "DB": ('M152', 'M145'), "DC": ('M182', 'M226'), "DE": ('M64', 'M27'),
    "DG": ('M62', 'M96'), "DH": ('M31', 'M311'), "DI": ('M249', 'M192'),
    "DL": ('M57', 'M172'), "DM": ('M278', 'M275'), "DN": ('M135', 'M171'),
    "DS": ('M32', 'M201'), "DV": ('M177', 'M266'), "DY": ('M307', 'M194'),
    "EA": ('M282', 'M140'), "EB": ('M200', 'M235'), "ED": ('M256', 'M200'),
    "EF": ('M79', 'M125'), "EG": ('M284', 'M111'), "EH": ('M296', 'M306'),
    "EI": ('M119', 'M117'), "EK": ('M30', 'M6'), "EM": ('M38', 'M209'),
    "EP": ('M224', 'M288'), "EQ": ('M45', 'M85'), "ER": ('M260', 'M217'),
    "ES": ('M170', 'M166'), "ET": ('M96', 'M168'), "EU": ('M283', 'M52'),
    "EV": ('M259', 'M78'), "EW": ('M83', 'M248'), "EX": ('M246', 'M160'),
    "EY": ('M205', 'M151'), "FB": ('M39', 'M121'), "FC": ('M84', 'M50'),
    "FG": ('M141', 'M156'), "FH": ('M255', 'M70'), "FK": ('M104', 'M268'),
    "FQ": ('M161', 'M183'), "FR": ('M77', 'M221'), "FU": ('M195', 'M216'),
    "FX": ('M261', 'M107'), "FZ": ('M145', 'M42'), "GB": ('M167', 'M82'),
    "GC": ('M244', 'M136'), "GD": ('M220', 'M178'), "GE": ('M306', 'M307'),
    "GF": ('M15', 'M133'), "GH": ('M173', 'M37'), "GJ": ('M72', 'M131'),
    "GL": ('M28', 'M40'), "GM": ('M288', 'M47'), "GN": ('M91', 'M244'),
    "GO": ('M123', 'M234'), "GQ": ('M236', 'M100'), "GR": ('M312', 'M32'),
    "GS": ('M241', 'M279'), "GU": ('M34', 'M233'), "GY": ('M302', 'M197'),
    "HA": ('M37', 'M207'), "HC": ('M242', 'M102'), "HD": ('M264', 'M202'),
    "HE": ('M226', 'M267'), "HF": ('M204', 'M116'), "HG": ('M19', 'M258'),
    "HK": ('M82', 'M260'), "HP": ('M18', 'M33'), "HQ": ('M128', 'M175'),
    "HS": ('M78', 'M25'), "HT": ('M188', 'M159'), "HW": ('M42', 'M174'),
    "HX": ('M180', 'M231'), "IC": ('M136', 'M128'), "IE": ('M132', 'M152'),
    "IH": ('M25', 'M250'), "IJ": ('M166', 'M164'), "IM": ('M23', 'M214'),
    "IN": ('M299', 'M113'), "IO": ('M50', 'M294'), "IQ": ('M190', 'M134'),
    "IR": ('M47', 'M246'), "IT": ('M297', 'M280'), "IU": ('M211', 'M123'),
    "IV": ('M134', 'M49'), "IW": ('M2', 'M144'), "IX": ('M225', 'M120'),
    "IZ": ('M245', 'M173'), "JA": ('M154', 'M67'), "JC": ('M199', 'M81'),
    "JD": ('M22', 'M24'), "JE": ('M48', 'M191'), "JF": ('M184', 'M56'),
    "JG": ('M1', 'M188'), "JI": ('M234', 'M142'), "JL": ('M279', 'M292'),
    "JN": ('M115', 'M251'), "JO": ('M131', 'M223'), "JP": ('M130', 'M163'),
    "JQ": ('M44', 'M240'), "JR": ('M107', 'M90'), "JS": ('M181', 'M203'),
    "JU": ('M73', 'M293'), "JW": ('M156', 'M54'), "JX": ('M280', 'M254'),
    "JY": ('M90', 'M39'), "JZ": ('M86', 'M10'), "KB": ('M202', 'M249'),
    "KD": ('M314', 'M14'), "KF": ('M176', 'M75'), "KH": ('M54', 'M177'),
    "KJ": ('M198', 'M76'), "KL": ('M97', 'M278'), "KM": ('M11', 'M213'),
    "KP": ('M139', 'M269'), "KQ": ('M140', 'M98'), "KR": ('M248', 'M106'),
    "KU": ('M171', 'M301'), "KV": ('M309', 'M300'), "KY": ('M203', 'M236'),
    "LA": ('M267', 'M285'), "LB": ('M75', 'M229'), "LC": ('M289', 'M245'),
    "LD": ('M209', 'M122'), "LE": ('M281', 'M153'), "LF": ('M13', 'M38'),
    "LH": ('M239', 'M220'), "LJ": ('M186', 'M189'), "LK": ('M137', 'M297'),
    "LM": ('M98', 'M15'), "LN": ('M179', 'M310'), "LO": ('M305', 'M60'),
    "LP": ('M223', 'M124'), "LQ": ('M66', 'M18'), "LR": ('M87', 'M148'),
    "LS": ('M49', 'M2'), "LT": ('M315', 'M284'), "LU": ('M17', 'M141'),
    "LV": ('M68', 'M139'), "LZ": ('M310', 'M57'), "MA": ('M149', 'M309'),
    "MB": ('M193', 'M212'), "MC": ('M12', 'M313'), "MF": ('M243', 'M3'),
    "MG": ('M192', 'M196'), "MI": ('M168', 'M19'), "MJ": ('M80', 'M179'),
    "ML": ('M164', 'M296'), "MN": ('M160', 'M58'), "MO": ('M27', 'M186'),
    "MQ": ('M229', 'M290'), "MR": ('M67', 'M195'), "MT": ('M271', 'M256'),
    "MU": ('M129', 'M104'), "MW": ('M206', 'M304'), "MX": ('M201', 'M277'),
    "MY": ('M105', 'M255'), "NA": ('M21', 'M281'), "NE": ('M222', 'M154'),
    "NH": ('M313', 'M132'), "NI": ('M60', 'M63'), "NJ": ('M117', 'M242'),
    "NQ": ('M126', 'M167'), "NR": ('M106', 'M232'), "NT": ('M120', 'M315'),
    "NW": ('M52', 'M228'), "NY": ('M265', 'M170'), "OA": ('M5', 'M215'),
    "OB": ('M110', 'M20'), "OC": ('M217', 'M271'), "OE": ('M311', 'M227'),
    "OF": ('M112', 'M46'), "OH": ('M235', 'M86'), "OI": ('M207', 'M180'),
    "OJ": ('M247', 'M48'), "OK": ('M61', 'M243'), "OL": ('M189', 'M264'),
    "OM": ('M285', 'M253'), "OP": ('M58', 'M241'), "OQ": ('M26', 'M316'),
    "OT": ('M29', 'M16'), "OW": ('M252', 'M93'), "OX": ('M303', 'M88'),
    "OY": ('M6', 'M257'), "OZ": ('M63', 'M158'), "PA": ('M74', 'M252'),
    "PB": ('M272', 'M91'), "PC": ('M228', 'M138'), "PD": ('M155', 'M185'),
    "PG": ('M99', 'M302'), "PK": ('M143', 'M61'), "PM": ('M254', 'M276'),
    "PN": ('M291', 'M41'), "PO": ('M92', 'M205'), "PQ": ('M238', 'M169'),
    "PT": ('M36', 'M101'), "PW": ('M8', 'M112'), "PZ": ('M14', 'M299'),
    "QA": ('M89', 'M149'), "QB": ('M214', 'M79'), "QC": ('M43', 'M238'),
    "QD": ('M273', 'M206'), "QE": ('M69', 'M110'), "QF": ('M262', 'M17'),
    "QI": ('M4', 'M89'), "QJ": ('M251', 'M115'), "QK": ('M138', 'M11'),
    "QM": ('M142', 'M119'), "QN": ('M109', 'M99'), "QT": ('M269', 'M1'),
    "QX": ('M275', 'M4'), "QZ": ('M3', 'M237'), "RA": ('M301', 'M182'),
    "RC": ('M35', 'M137'), "RD": ('M165', 'M126'), "RF": ('M308', 'M5'),
    "RH": ('M9', 'M8'), "RJ": ('M114', 'M162'), "RL": ('M240', 'M176'),
    "RM": ('M295', 'M29'), "RO": ('M268', 'M265'), "RP": ('M151', 'M28'),
    "RQ": ('M95', 'M155'), "RS": ('M20', 'M210'), "RT": ('M70', 'M118'),
    "RU": ('M148', 'M157'), "RW": ('M270', 'M150'), "RX": ('M93', 'M282'),
    "RY": ('M53', 'M43'), "RZ": ('M169', 'M7'), "SA": ('M185', 'M95'),
    "SB": ('M157', 'M161'), "SC": ('M108', 'M92'), "SE": ('M172', 'M211'),
    "SF": ('M292', 'M143'), "SH": ('M113', 'M135'), "SI": ('M163', 'M21'),
    "SJ": ('M208', 'M289'), "SK": ('M101', 'M87'), "SL": ('M100', 'M272'),
    "SM": ('M122', 'M74'), "SN": ('M293', 'M71'), "SP": ('M124', 'M22'),
    "SQ": ('M76', 'M127'), "ST": ('M227', 'M51'), "SU": ('M118', 'M66'),
    "SW": ('M196', 'M109'), "SY": ('M294', 'M225'), "SZ": ('M40', 'M263'),
    "TA": ('M46', 'M68'), "TC": ('M276', 'M80'), "TK": ('M290', 'M94'),
    "TV": ('M258', 'M193'), "TX": ('M230', 'M64'), "TY": ('M215', 'M62'),
    "UA": ('M147', 'M97'), "UC": ('M216', 'M262'), "UE": ('M231', 'M147'),
    "UH": ('M33', 'M190'), "UK": ('M194', 'M298'), "UM": ('M218', 'M230'),
    "UQ": ('M197', 'M222'), "UR": ('M10', 'M287'), "UT": ('M121', 'M286'),
    "UY": ('M133', 'M312'), "UZ": ('M300', 'M242'), "VA": ('M257', 'M167'),
    "VB": ('M298', 'M232'), "VC": ('M71', 'M315'), "VD": ('M174', 'M228'),
    "VE": ('M212', 'M170'), "VF": ('M175', 'M215'), "VG": ('M237', 'M20'),
    "VH": ('M111', 'M271'), "VK": ('M232', 'M227'), "VM": ('M102', 'M46'),
    "VO": ('M270', 'M86'), "VP": ('M93', 'M180'), "VR": ('M53', 'M48'),
    "VS": ('M169', 'M243'), "VT": ('M185', 'M264'), "VU": ('M157', 'M253'),
    "VW": ('M108', 'M241'), "VY": ('M172', 'M316'), "WA": ('M292', 'M16'),
    "WB": ('M113', 'M93'), "WC": ('M163', 'M88'), "WE": ('M208', 'M257'),
    "WH": ('M101', 'M158'), "WI": ('M100', 'M252'), "WJ": ('M122', 'M91'),
    "WK": ('M293', 'M138'), "WL": ('M124', 'M185'), "WM": ('M76', 'M302'),
    "WN": ('M227', 'M61'), "WP": ('M118', 'M276'), "WQ": ('M196', 'M41'),
    "WT": ('M294', 'M205'), "WV": ('M40', 'M169'), "WY": ('M46', 'M101'),
    "WZ": ('M184', 'M112'), "XA": ('M1', 'M299'), "XB": ('M234', 'M149'),
    "XC": ('M279', 'M79'), "XD": ('M115', 'M238'), "XE": ('M131', 'M206'),
    "XH": ('M130', 'M108'), "XI": ('M44', 'M184'), "XJ": ('M107', 'M105'),
    "XK": ('M181', 'M239'), "XM": ('M73', 'M247'), "XS": ('M156', 'M199'),
    "XV": ('M280', 'M308'), "XW": ('M90', 'M305'), "XZ": ('M86', 'M72'),
    "YA": ('M202', 'M283'), "YB": ('M314', 'M291'),"YC": ('M176', 'M259'),
    "YD": ('M54', 'M274'), "YE": ('M198', 'M204'), "YH": ('M97', 'M129'),
    "YI": ('M11', 'M44'), "YJ": ('M139', 'M295'), "YK": ('M140', 'M31'),
    "YL": ('M248', 'M270'), "YM": ('M171', 'M59'), "YN": ('M309', 'M65'),
    "YO": ('M203', 'M314'), "YP": ('M267', 'M35'), "YQ": ('M75', 'M55'),
    "YR": ('M289', 'M303'), "YS": ('M209', 'M273'), "YT": ('M281', 'M165'),
    "YV": ('M13', 'M114'), "YW": ('M239', 'M45'), "YZ": ('M241', 'M130'),
    "ZA": ('M34', 'M198'), "ZB": ('M302', 'M261'), "ZD": ('M37', 'M84'),
    "ZE": ('M242', 'M313'), "ZF": ('M264', 'M3'), "ZG": ('M226', 'M196'),
    "ZH": ('M204', 'M19'), "ZI": ('M19', 'M179'), "ZJ": ('M82', 'M296'),
    "ZM": ('M18', 'M58'), "ZN": ('M128', 'M186'), "ZP": ('M78', 'M290'),
    "ZQ": ('M188', 'M195'), "ZR": ('M42', 'M256'), "ZS": ('M180', 'M104'),
    "ZV": ('M136', 'M117'), "ZW": ('M132', 'M6'), "ZX": ('M25', 'M209'),
    "ZY": ('M11', 'M288')
}

enzymatic_genes = list(enzymatic_reactions.keys())

perception_genes = [
    "AL", "AN", "BA", "BZ", "CG", "CI", "CR", "CX", "DF", "DZ", "EC", "EJ",
    "FA", "GA", "GI", "GK", "HB", "HI", "HJ", "IP", "JB", "JH", "JV", "KA",
    "KC", "KN", "KO", "LG", "LI", "LW", "LX", "MD", "ME", "NM", "NO", "OR",
    "PE", "QG", "QH", "RB", "RE", "RN", "SD", "SG", "SO", "SR", "SV", "TB",
    "TM", "TQ", "UB", "UD", "UF", "UG", "UJ", "UL", "UN", "VZ", "WD", "WF",
    "WG", "WO", "WR", "XY", "YF", "YU", "ZO", "ZT"
]
