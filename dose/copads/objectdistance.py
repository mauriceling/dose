"""
Functions for Calculating Similarity Coefficients between 2 Objects.

Generally, the lower boundary of similar coefficient
signifies complete difference (no similarity) while the upper boundary
(if any) signifies complete similarity (no difference).

In the following formulae, the following notations will be used
    - A = found in both 'original' and 'test'
    - B = found in 'original' only
    - C = found in 'test' only
    - D = not found in either 'original' or 'test'
    - P = total (that is, P = A + B + C + D)

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 17th August 2005
"""

import math
from .copadsexceptions import DistanceInputSizeError


def binarize(data, absent=0, type='Full'):
    """
    Converts input data in a list of presence or absence of values.
    For example,
    binarize([1, 2, 0, 3, 4, 0], 0, 'Full') --> [1, 1, 0, 1, 1, 0]
    binarize([1, 2, 0, 3, 4, 0], 0, 'Partial') --> [1, 2, 0, 3, 4, 0]
    binarize([1, 2, 0, 3, 4, 0], 2, 'Full') --> [1, 0, 1, 1, 1, 1]
    binarize([1, 2, 0, 3, 4, 0], 2, 'Partial') --> [1, 0, 0, 3, 4, 0]

    As 1 and 0 are commonly used to denote presence and absence, please 
    take care when data contains 1s and 0s.

    @param data: data to binarize
    @type data: list
    @param absent: value/symbol to denote absent value. Default = 0.
    @param type: Denotes type of binarization, which can be 'Full' or 
    'Partial'. If full binarize, the returned data will only be 1 
    (denote presence) or 0 (denote absence). If partial binarize, the 
    returned data will be 0 (denote absence) or the original values 
    in data (denoting not absent). Default = Full. 
    """
    if type == 'Full':
        return [{absent: 0}.get(x, 1) for x in data]
    elif type == 'Partial':
        return [{absent: 0}.get(x, x) for x in data]

def compare(original, test, absent, type='Set'):
    """
    Used for processing list-based (positional) or set-based
    (non-positional) distance of categorical data.

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: indicator to define absent data
    @param type: {List | Set}
    """
    if type == 'Set':
        original_only = float(len([x for x in original if x not in test]))
        test_only = float(len([x for x in test if x not in original]))
        both = float(len([x for x in original if x in test]))
        return (original_only, test_only, both, 0.0)
    if type == 'List':
        original, test = list(original), list(test)
        original_only, test_only, both, none = 0.0, 0.0, 0.0, 0.0
        for i in range(len(original)):
            if original[i] == absent and test[i] == absent:
                none = none + 1
            elif original[i] == test[i]:
                both = both + 1
            elif original[i] != absent and test[i] == absent:
                original_only = original_only + 1
            elif original[i] == absent and test[i] != absent:
                test_only = test_only + 1
            else: pass
        return (original_only, test_only, both, none)

def Jaccard(original, test, absent=0, type='Set'):
    """
    Jaccard coefficient for nominal or ordinal data.

    Coefficient: M{A / (A + B + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.1
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return both / (both + original + test)

def Sokal_Michener(original, test, absent=0, type='Set'):
    """
    Sokal and Michener coefficient for nominal or ordinal data.

    Coefficient: M{(A + D) / P}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.1
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
                equal for Sokal & Michener's distance")
    (original, test, both, none) = compare(original, test, absent, type)
    return (both + none) / (original + test + both + none)

def Matching(original, test, absent=0, type='Set'):
    """
    Matching coefficient for nominal or ordinal data

    Coefficient: M{(A + D) / (2A + B + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return (both + none) / (original + both + test + both)

def Dice(original, test, absent=0, type='Set'):
    """
    Dice coefficient for nominal or ordinal data.

    Coefficient: M{2A / (2A + B + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.1
    """
    all_region = float(len(original)) + float(len(test))
    (original, test, both, none) = compare(original, test, absent, type)
    return (2 * both) / all_region

def Ochiai(original, test, absent=0, type='Set'):
    """
    Ochiai coefficient for nominal or ordinal data.

    Coefficient: M{2A / sqrt((A + B)(A + C)))}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.1
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return both / ((both + original) * (both + test)) ** 0.5

def Ochiai2(original, test, absent=0, type='Set'):
    """
    Ochiai 2 coefficient for nominal or ordinal data, and requires
    the presence of regions whereby both original and test are not
    present.

    Coefficient: M{(A * D) / sqrt((A + B)(A + C)(D + B)(D + C))}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    denominator = ((both + original) * (both + test) * \
                  (none + original) * (none + test)) ** 0.5
    return (both * none) / denominator

def Anderberg(original, test, absent=0, type='Set'):
    """
    Anderberg coefficient for nominal or ordinal data.

    Coefficient: M{A / (A + 2(B + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return both / (both + 2 * (original + test))

def Kulczynski2(original, test, absent=0, type='Set'):
    """
    Second Kulczynski coefficient for nominal or ordinal data.

    Coefficient: M{((A / (A + B)) + (A / (A + C))) / 2}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    x1 = both / (original + both)
    x2 = both / (test + both)
    return (x1 + x2) / 2

def Kulczynski(original, test, absent=0, type='Set'):
    """
    First Kulczyski coefficient for nominal or ordinal data.

    Coefficient: M{A / (B + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.1
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return both / (original + test)

def Forbes(original, test, absent=0, type='Set'):
    """
    Forbes coefficient for nominal or ordinal data.

    Coefficient: M{A(P) / ((A + B)(A + C))}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = both * (both + original + test + none)
    denominator = (original + both) * (test + both)
    return numerator / denominator

def Hamann(original, test, absent=0, type='Set'):
    """
    Hamann coefficient for nominal or ordinal data.

    Coefficient: M{((A + D) - (B + C)) / P}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = (both + none) - (test + original)
    return numerator / (original + test + both + none)

def Simpson(original, test, absent=0, type='Set'):
    """
    Simpson coefficient for nominal or ordinal data.

    Coefficient: M{A / min(A + B, A + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return both / min(both + test, both + original)

def Russel_Rao(original, test, absent=0, type='Set'):
    """
    Russel and Rao coefficient for nominal or ordinal data.

    Coefficient: M{A / P}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return both / (original + test + both + none)

def Roger_Tanimoto(original, test, absent=0, type='Set'):
    """
    Roger and Tanimoto coefficient for nominal or ordinal data.

    Coefficient: M{(A + D) / (A + 2B + 2C + D)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    denominator = (2 * original) + (2 * test) + both + none
    return (both + none) / denominator

def Sokal_Sneath(original, test, absent=0, type='Set'):
    """
    Sokal and Sneath coefficient for nominal or ordinal data.

    Coefficient: M{A / (A + 2B + 2C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    denominator = (2 * original) + (2 * test) + both
    return both / denominator

def Sokal_Sneath2(original, test, absent=0, type='Set'):
    """
    Sokal and Sneath 2 coefficient for nominal or ordinal data.

    Coefficient: M{(2A + 2D) / (2A + B + C + 2D)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = (2 * both) + (2 * none)
    denominator = (2 * both) + original + test + (2 * none)
    return numerator / denominator

def Sokal_Sneath3(original, test, absent=0, type='Set'):
    """
    Sokal and Sneath 3 coefficient for nominal or ordinal data.

    Coefficient: M{(A + D) / (B + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    return (both + none) / (test + original)

def Buser(original, test, absent=0, type='Set'):
    """
    Buser coefficient (also known as Baroni-Urbani coefficient)
    for nominal or ordinal data.

    Coefficient: M{(sqrt(A * D) + A) / (sqrt(A * D) + A + B + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    t = (both + none) ** 0.5
    return (t + both) / (t + both + test + original)

def Fossum(original, test, absent=0, type='Set'):
    """
    Fossum coefficient for nominal or ordinal data.

    Coefficient:
    M{((A + B + C + D)(A - 0.5)^2) / ((A + B)(A + C))}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = original + test + both + none
    numerator = numerator * (both - 0.5) ** 2
    return numerator / ((both + test) * (both + original))

def YuleQ(original, test, absent=0, type='Set'):
    """
    Yule Q coefficient (also known as First Yule coefficient) for
    nominal or ordinal data.

    Coefficient: M{((A * D) - (B * C)) / ((A * D) + (B * C))}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = (both * none) - (test * original)
    denominator = (both * none) + (test * original)
    return numerator / denominator

def YuleY(original, test, absent=0, type='Set'):
    """
    Yule Y coefficient (also known as Second Yule coefficient) for
    nominal or ordinal data.

    Coefficient:
    M{(sqrt(A * D) - sqrt(B * C)) / (sqrt(A * D) + sqrt(B * C))}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = ((both * none) ** 0.5) - ((test * original) ** 0.5)
    denominator = ((both * none) ** 0.5) + ((test * original) ** 0.5)
    return numerator / denominator

def Mcconnaughey(original, test, absent=0, type='Set'):
    """
    McConnaughey coefficient for nominal or ordinal data.

    Coefficient: M{(A^2 - (B * C)) / (A + B)(A + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = (both * both) - (original * test)
    denominator = (both + original) * (both + test)
    return numerator / denominator

def Stiles(original, test, absent=0, type='Set'):
    """
    Stiles coefficient for nominal or ordinal data.

    Coefficient:
    M{log10((P(|(A * D) - (B * C)| - (P / 2)) ^ 2) /
    (A + B)(A + C)(B + D)(C + D))}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    n = original + test + both + none
    t = abs((both * none) - (test * original))
    numerator = n * ((t - (0.5 * n)) ** 2)
    denominator = (both + original) * (both + test) * \
                  (none + original) * (none + test)
    return math.log10(numerator / denominator)

def Pearson(original, test, absent=0, type='Set'):
    """
    Pearson coefficient for nominal or ordinal data.

    Coefficient:
    M{((A * D) - (B * C)) / (A + B)(A + C)(B + D)(C + D)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    numerator = (both * none) - (test * original)
    denominator = ((both + original) * (both + test) * \
                   (none + original) * (none + test)) ** 0.5
    return numerator / denominator

def Dennis(original, test, absent=0, type='Set'):
    """
    Dennis coefficient for nominal or ordinal data.

    Coefficient:
    M{((A * D) - (B * C)) / P(A + B)(A + C)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    n = original + test + both + none
    numerator = (both * none) - (test * original)
    denominator = (n * (both + original) * (both + test)) ** 0.5
    return numerator / denominator

def Gower_Legendre(original, test, absent=0, type='Set'):
    """
    Gower and Legendre coefficient for nominal or ordinal data.

    Coefficient: M{(A + D) / ((0.5 * (B + C)) + A + D)}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    n = original + test + both + none
    numerator = both + none
    denominator = (0.5 * (test + original)) + numerator
    return numerator / denominator

def Tulloss(original, test, absent=0, type='Set'):
    """
    Tulloss coefficient for nominal or ordinal data.

    Coefficient:
    M{sqrt(U * S * R)}
        - M{U = log(1 + ((min(B, C) + A) / (max(B, C) + A))) / log2}
        - M{S = 1 / sqrt(log(2 + (min(B, C) / (A + 1))) / log2)}
        - M{R = log(1 + A / (A + B))log(1 + A / (A + C)) / log2log2}

    @param original: list of original data
    @param test: list of data to test against original
    @param absent: user-defined identifier for absent of region,
        default = 0
    @param type: {Set | List}, define whether use Set comparison
        (non-positional) or list comparison (positional), default = Set

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.3
    """
    (original, test, both, none) = compare(original, test, absent, type)
    U = (min(test, original) + both) / (max(test, original) + both)
    U = math.log10(1 + U) / math.log10(2)
    S = math.log10(2 + (min(test, original) / (both + 1)))
    S = 1 / ((S / math.log10(2)) ** 0.5)
    R = math.log10(1 + (both / (both + original)))
    R = R * math.log10(1 + (both / (both + test)))
    R = R / (math.log10(2) * math.log10(2))
    return (U * S * R) ** 0.5

def Hamming(original, test):
    """
    Hamming coefficient for ordinal data - only for positional data.

    Coefficient: number of mismatches with respect to position

    @param original: list of original data
    @param test: list of data to test against original

    @see: Ling, MHT. 2010. COPADS, I: Distances Measures between Two
    Lists or Sets. The Python Papers Source Codes 2:2.

    @status: Tested function
    @since: version 0.1
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Hamming's distance")
    mismatch = 0
    for index in range(len(original)):
        if original[index] != test[index]: mismatch = mismatch + 1
    return mismatch

def Euclidean(original, test):
    """
    Euclidean coefficient for interval or ratio data.

    Coefficient: M{sqrt(S{sum}(((A + B)(i) - (A + C)(i)) ^ 2))}

    euclidean(original, test) -> euclidean distance between original
    and test. Adapted from BioPython

    @param original: list of original data
    @param test: list of data to test against original

    @status: Tested function
    @since: version 0.1
    """
    # lightly modified from implementation by Thomas Sicheritz-Ponten.
    # This works faster than the Numeric implementation on shorter
    # vectors.
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Euclidean distance")
    sum = 0
    for i in range(len(original)):
        sum = sum + (original[i] - test[i]) ** 2
    return math.sqrt(sum)

def Minkowski(original, test, power=3):
    """
    Minkowski coefficient for interval or ratio data.

    Coefficient: M{power-th root(S{sum}(((A + B)(i) - (A + C)(i)) ^ power))}

    Minkowski Distance is a generalized absolute form of Euclidean
    Distance. Minkowski Distance = Euclidean Distance when power = 2

    @param original: list of original data
    @param test: list of data to test against original
    @param power: expontential variable
    @type power: integer

    @status: Tested function
    @since: version 0.4
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Minkowski distance")
    sum = 0
    for i in range(len(original)):
        sum = sum + abs(original[i] - test[i]) ** power
    return sum ** (1 / float(power))

def Manhattan(original, test):
    """
    Manhattan coefficient for interval or ratio data.

    Coefficient: M{S{sum}(abs((A + B)(i) - (A + C)(i)))}

    Manhattan Distance is also known as City Block Distance. It is
    essentially summation of the absolute difference between each
    element.

    @see: Krause, Eugene F. 1987. Taxicab Geometry. Dover. ISBN 0-486-
    25202-7.

    @param original: list of original data
    @param test: list of data to test against original

    @status: Tested function
    @since: version 0.4
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Manhattan distance")
    sum = 0
    for i in range(len(original)):
        sum = sum + abs(original[i] - test[i])
    return float(sum)

def Canberra(original, test):
    """
    Canberra coefficient for interval or ratio data.

    Coefficient:
    M{S{sum}(abs((A + B)(i) - (A + C)(i)) / abs((A + B)(i) + (A + C)(i)))}

    @see: Lance GN and Williams WT. 1966. Computer programs for
    hierarchical polythetic classification. Computer Journal 9: 60-64.

    @param original: list of original data
    @param test: list of data to test against original

    @status: Tested function
    @since: version 0.4
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Canberra distance")
    sum = 0
    for i in range(len(original)):
        sum = sum + (abs(original[i] - test[i]) / abs(original[i] + \
            test[i]))
    return sum

def Bray_Curtis(original, test):
    """
    Complement Bray and Curtis coefficient for interval or ratio data.
    Lower boundary of Bray and Curtis coefficient represents complete
    similarity (no difference).

    Coefficient:
    M{1 - S{sum}(abs((A + B)(i) - (A + C)(i))) /
    (S{sum}((A + B)(i)) + S{sum}((A + C)(i)))}

    @see: Bray JR and Curtis JT. 1957. An ordination of the upland
    forest communities of S. Winconsin. Ecological Monographs 27:
    325-349.

    @param original: list of original data
    @param test: list of data to test against original

    @status: Tested function
    @since: version 0.4
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Bray-Curtis distance")
    return 1 - (Manhattan(original, test) / \
            float(sum(original) + sum(test)))

def Cosine(original, test):
    """
    Cosine coefficient for interval or ratio data.

    Coefficient:
    M{S{sum}(abs((A + B)(i) * (A + C)(i))) /
    (S{sum}((A + B) ^ 2) * S{sum}((A + C) ^ 2))}

    @param original: list of original data
    @param test: list of data to test against original

    @status: Tested function
    @since: version 0.4
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Cosine distance")
    original = [float(x) for x in original]
    test = [float(x) for x in test]
    numerator = sum([original[x] * test[x] for x in range(len(original))])
    denominator = sum([x * x for x in original]) ** 0.5
    denominator = denominator * (sum([x * x for x in test]) ** 0.5)
    return numerator / denominator

def Tanimoto(original, test):
    """
    Tanimoto coefficient for interval or ratio data.

    Coefficient:
    M{S{sum}(abs((A + B)(i) * (A + C)(i))) /
    (S{sum}((A + B) ^ 2) + S{sum}((A + C) ^ 2) -
    S{sum}(abs((A + B)(i) * (A + C)(i))))}

    @param original: list of original data
    @param test: list of data to test against original

    @status: Tested function
    @since: version 0.4
    """
    if len(original) != len(test):
        raise DistanceInputSizeError("Size (length) of inputs must be \
            equal for Cosine distance")
    original = [float(x) for x in original]
    test = [float(x) for x in test]
    numerator = sum([original[x] * test[x] for x in range(len(original))])
    denominator = sum([x * x for x in original])
    denominator = denominator + (sum([x * x for x in test])) - numerator
    return numerator / denominator
