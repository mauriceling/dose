"""
Statistical Hypothesis Testing Routines.

Each routine will Returns a 5-element list
    - [left result, left critical, statistic, right critical, right result]
where
    - left result = True (statistic in lower critical region) or
    False (statistic not in lower critical region)
    - left critical = lower critical value generated from 1 - confidence
    - statistic = calculated statistic value
    - right critical = upper critical value generated from confidence
    - right result = True (statistic in upper critical region) or
    False (statistic not in upper critical region)

References
    - Test 1-100: Gopal K. Kanji. 2006. 100 Statistical Tests, 3rd edition.
    Sage Publications.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 1st September 2008
"""

from math import sqrt, log, e
from statisticsdistribution import *

def test(statistic, distribution, confidence):
    """Generates the critical value from distribution and confidence value
    using the distribution's inverseCDF method and performs 1-tailed and
    2-tailed test by comparing the calculated statistic with the critical
    value.


    Returns a 5-element list
    [left result, left critical, statistic, right critical, right result]
    where
        - left result = True (statistic in lower critical region) or
        False (statistic not in lower critical region)
        - left critical = lower critical value generated from 1 - confidence
        - statistic = calculated statistic value
        - right critical = upper critical value generated from confidence
        - right result = True (statistic in upper critical region) or
        False (statistic not in upper critical region)

    Therefore, null hypothesis is accepted if left result and right result are
    both False in a 2-tailed test.

    @param statistic: calculated statistic (float)
    @param distribution: distribution to calculate critical value
    @type distribution: instance of a statistics distribution
    @param confidence: confidence level of a one-tail
        test (usually 0.95 or 0.99), use 0.975 or 0.995 for 2-tail test
    @type confidence: float of less than 1.0"""
    data = [None, None, statistic, None, None]
    data[1] = distribution.inverseCDF(1.0 - confidence)[0]
    if data[1] < statistic: data[0] = False
    else: data[0] = True
    data[3] = distribution.inverseCDF(confidence)[0]
    if statistic < data[3]: data[4] = False
    else: data[4] = True
    return data

def Z1Mean1Variance(smean, pmean, pvar, ssize, confidence):
    """
    Test 1: Z-test for a population mean (variance known)

    To investigate the significance of the difference between an assumed
    population mean and sample mean when the population variance is
    known.

    Limitations
        1. Requires population variance (use Test 7 if population variance
        unknown)

    @param smean: sample mean
    @param pmean: population mean
    @param pvar: population variance
    @param ssize: sample size
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    statistic = float(abs(smean - pmean)/ \
                (pvar / sqrt(ssize)))
    return test(statistic, NormalDistribution(), confidence)

def Z2Mean1Variance(smean1, smean2, pvar, ssize1, ssize2, confidence,
                    pmean1=0.0, pmean2=0.0):
    """
    Test 2: Z-test for two population means (variances known and equal)

    To investigate the significance of the difference between the means of two
    samples when the variances are known and equal.

    Limitations
        1. Population variances must be known and equal (use Test 8 if
        population variances unknown

    @param smean1: sample mean of sample #1
    @param smean2: sample mean of sample #2
    @param pvar: variances of both populations (variances are equal)
    @param ssize1: sample size of sample #1
    @param ssize2: sample size of sample #2
    @param confidence: confidence level
    @param pmean1: population mean of population #1 (optional)
    @param pmean2: population mean of population #2 (optional)

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    statistic = float(((smean1 - smean2) - (pmean1 - pmean2))/ \
                (pvar * sqrt((1.0 / ssize1) + (1.0 / ssize2))))
    return test(statistic, NormalDistribution(), confidence)

def Z2Mean2Variance(smean1, smean2, pvar1, pvar2, ssize1, ssize2, confidence,
                    pmean1=0.0, pmean2=0.0):
    """
    Test 3: Z-test for two population means (variances known and unequal)

    To investigate the significance of the difference between the means of two
    samples when the variances are known and unequal.

    Limitations
        1. Population variances must be known(use Test 9 if population variances
        unknown

    @param smean1: sample mean of sample #1
    @param smean2: sample mean of sample #2
    @param pvar1: variance of population #1
    @param pvar2: variance of population #2
    @param ssize1: sample size of sample #1
    @param ssize2: sample size of sample #2
    @param confidence: confidence level
    @param pmean1: population mean of population #1 (optional)
    @param pmean2: population mean of population #2 (optional)

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.4
    """
    statistic = float(((smean1 - smean2) - (pmean1 - pmean2))/ \
                sqrt((pvar1 / ssize1) + (pvar2 / ssize2)))
    return test(statistic, NormalDistribution(), confidence)

def Z1Proportion(spro, ppro, ssize, confidence):
    """
    Test 4: Z-test for a proportion (binomial distribution)

    To investigate the significance of the difference between an assumed
    proportion and an observed proportion.

    Limitations
        1. Requires sufficiently large sample size to use Normal approximation
        to binomial

    @param spro: sample proportion
    @param ppro: population proportion
    @param ssize: sample size
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    statistic = float((abs(ppro - spro) - (1 / (2 * ssize)))/ \
                sqrt((ppro * (1 - spro)) / ssize))
    return test(statistic, NormalDistribution(), confidence)

def Z2Proportion(spro1, spro2, ssize1, ssize2, confidence):
    """
    Test 5: Z-test for the equality of two proportions (binomial distribution)
    To investigate the assumption that the proportions of elements from two
    populations are equal, based on two samples, one from each population.

    Limitations
        1. Requires sufficiently large sample size to use Normal approximation
        to binomial

    @param spro1: sample proportion #1
    @param spro2: sample proportion #2
    @param ssize1: sample size #1
    @param ssize2: sample size #2
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    P = float(((spro1 * ssize1) + (spro2 * ssize2)) / (ssize1 + ssize2))
    statistic = float((spro1 - spro2) / \
                (P * (1.0 - P) * ((1.0 / ssize1) + (1.0 / ssize2))) ** 0.5)
    return test(statistic, NormalDistribution(), confidence)

def Z2Count(time1, time2, count1, count2, confidence):
    """
    Test 6: Z-test for comparing two counts (Poisson distribution)

    To investigate the significance of the differences between two counts.

    Limitations
        1. Requires sufficiently large sample size to use Normal approximation
        to binomial

    @param time1: first measurement time
    @param time2: second measurement time
    @param count1: counts at first measurement time
    @param count2: counts at second measurement time
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    R1 = count1 / float(time1)
    R2 = count2 / float(time2)
    statistic = float((R1 - R2) / sqrt((R1 / time1) + (R2 / time2)))
    return test(statistic, NormalDistribution(), confidence)

def t1Mean(smean, pmean, svar, ssize, confidence):
    """
    Test 7: t-test for a population mean (population variance unknown)

    To investigate the significance of the difference between an assumed
    population mean and a sample mean when the population variance is
    unknown and cannot be assumed equal or not equal.

    Limitations
        1. Weaker form of Test 1

    @param smean: sample mean
    @param pmean: population mean
    @param svar: sample variance
    @param ssize: sample size
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float((smean - pmean) / (svar / sqrt(ssize)))
    return test(statistic, TDistribution(shape = ssize-1), confidence)

def t2Mean2EqualVariance(smean1, smean2, svar1, svar2, ssize1, ssize2,
                         confidence, pmean1=0.0, pmean2=0.0):
    """
    Test 8: t-test for two population means (population variance unknown but
    equal)

    To investigate the significance of the difference between the means of
    two populations when the population variances are unknown but assumed
    equal.

    Limitations
        1. Weaker form of Test 2

    @param smean1: sample mean of sample #1
    @param smean2: sample mean of sample #2
    @param svar1: variances of sample #1
    @param svar2: variances of sample #2
    @param ssize1: sample size of sample #1
    @param ssize2: sample size of sample #2
    @param confidence: confidence level
    @param pmean1: population mean of population #1 (optional)
    @param pmean2: population mean of population #2 (optional)

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    df = ssize1 + ssize2 - 2
    pvar = float((((ssize1 - 1) * svar1) + ((ssize2 - 1) * svar2)) / df)
    statistic = float(((smean1 - smean2) - (pmean1 - pmean2)) / \
                ((sqrt(pvar)) * sqrt((1.0 / ssize1) + (1.0 / ssize2))))
    return test(statistic, TDistribution(shape = df), confidence)

def t2Mean2UnequalVariance(smean1, smean2, svar1, svar2, ssize1, ssize2,
                           confidence, pmean1=0.0, pmean2=0.0):
    """
    Test 9: t-test for two population means (population variance unknown and
    unequal)

    To investigate the significance of the difference between the means of
    two populations when the population variances are unknown and unequal.

    Limitations
        1. Weaker form of Test 3

    @param smean1: sample mean of sample #1
    @param smean2: sample mean of sample #2
    @param svar1: variances of sample #1
    @param svar2: variances of sample #2
    @param ssize1: sample size of sample #1
    @param ssize2: sample size of sample #2
    @param confidence: confidence level
    @param pmean1: population mean of population #1 (optional)
    @param pmean2: population mean of population #2 (optional)

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float(((smean1 - smean2) - (pmean1 - pmean2)) / \
                sqrt((svar1 / ssize1) + (svar2 / ssize2)))
    df = float((((svar1 / ssize1) + (svar2 / ssize2)) ** 2) / \
        (((svar1 ** 2) / ((ssize1 ** 2) * (ssize1 - 1))) + \
            ((svar2 ** 2) / ((ssize2 ** 2) * (ssize2 - 1)))))
    return test(statistic, TDistribution(shape = df), confidence)

def tPaired(smean1, smean2, svar, ssize, confidence):
    """
    Test 10: t-test for two population means (method of paired comparisons)

    To investigate the significance of the difference between two population
    means when no assumption is made about the population variances.

    @param smean1: sample mean of sample #1
    @param smean2: sample mean of sample #2
    @param svar: variance of differences between pairs
    @param ssize: sample size
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float((smean1 - smean2) / (svar / sqrt(ssize)))
    return test(statistic, TDistribution(shape = ssize - 1), confidence)

def tRegressionCoefficient(variancex, varianceyx, b, ssize, confidence):
    """
    Test 11: t-test of a regression coefficient

    To investigate the significance of the regression coefficient.

    Limitations
        1. Homoedasticity of values

    @param variancex: variance of x
    @param varianceyx: variance of yx
    @param b: calculated Regression Coefficient
    @param ssize: sample size
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float(((b * sqrt(variancex)) / \
        sqrt(varianceyx)) * ((ssize-1) ** -0.5))
    return test(statistic, TDistribution(shape = ssize - 2), confidence)

def tPearsonCorrelation(r, ssize, confidence):
    """
    Test 12: t-test of a correlation coefficient

    To investigate whether the difference between the sample correlation
    coefficient and zero is statistically significant.

    Limitations
        1. Assumes population correlation coefficient to be zero (use Test 13
        for testing other population correlation coefficient
        2. Assumes a linear relationship (regression line as Y = MX + C)
        3. Independence of x-values and y-values

    Use Test 59 when these conditions cannot be met

    @param r: calculated Pearson's product-moment correlation coefficient
    @param ssize: sample size
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float((r * sqrt(ssize - 2)) / sqrt(1 - (r **2)))
    return test(statistic, TDistribution(shape = ssize - 2), confidence)

def ZPearsonCorrelation(sr, pr, ssize, confidence):
    """
    Test 13: Z-test of a correlation coefficient

    To investigate the significance of the difference between a correlation
    coefficient and a specified value.

    Limitations
        1. Assumes a linear relationship (regression line as Y = MX + C)
        2. Independence of x-values and y-values

    Use Test 59 when these conditions cannot be met

    @param sr: calculated sample Pearson's product-moment correlation
        coefficient
    @param pr: specified Pearson's product-moment correlation coefficient
        to test
    @param ssize: sample size
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    if sr == 1.0: sr = 0.9999999999
    if pr == 1.0: pr = 0.9999999999
    Z1 = float(0.5 * log((1 + sr) / (1 - sr)))
    meanZ1 = float(0.5 * log((1 + pr) / (1 - pr)))
    sigmaZ1 = float(1.0 / sqrt(ssize - 3))
    statistic = float((Z1 - meanZ1) / sigmaZ1)
    return test(statistic, NormalDistribution(), confidence)

def Z2PearsonCorrelation(r1, r2, ssize1, ssize2, confidence):
    """
    Test 14: Z-test for two correlation coefficients

    To investigate the significance of the difference between the correlation
    coefficients for a pair variables occurring from two difference
    populations.

    @param r1: Pearson correlation coefficient of sample #1
    @param r2: Pearson correlation coefficient of sample #2
    @param ssize1: Sample size #1
    @param ssize2: Sample size #2
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    z1 = float(0.5 * log((1.0 + r1) / (1.0 - r1)))
    z2 = float(0.5 * log((1.0 + r2) / (1.0 - r2)))
    sigma1 = float(1.0 / sqrt(ssize1 - 3))
    sigma2 = float(1.0 / sqrt(ssize2 - 3))
    sigma = float(sqrt((sigma1 ** 2) + (sigma2 ** 2)))
    statistic = float(abs(z1 - z2) / sigma)
    return test(statistic, NormalDistribution(), confidence)

def ChiSquarePopVar(values, ssize, pv, confidence = 0.95):
    """
    Test 15: Chi-square test for a population variance

    To investigate the difference between a sample variance and an assumed
    population variance.

    @param values: sample values
    @param ssize: sample size
    @param pv: population variance
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    mean = sum(values)/ssize
    freq = [float((values[i] - mean) ** 2)
            for i in range(len(values))]
    sv = float((sum(freq)/(ssize-1)))
    statistic = float((((ssize - 1) * sv) / pv))
    return test(statistic, ChiSquareDistribution(df = ssize-1), confidence)

def FVarianceRatio(var1, var2, ssize1, ssize2, confidence):
    """
    Test 16: F-test for two population variances (variance ratio test)

    To investigate the significance of the difference between two population
    variances.

    @param var1: variance #1
    @param var2: variance #2
    @param ssize1: sample size #1
    @param ssize2: sample size #2
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float(var1 / var2)
    return test(statistic, FDistribution(df1=ssize1-1, df2=ssize2-1),
    confidence)

def F2CorrelatedObs(r, var1, var2, ssize1, ssize2, confidence):
    """
    Test 17: F-test for two population variances (with correlated observations)

    To investigate the difference between two population variances when there
    is correlation between the pairs of observations.
    @param r: Sample correlation value
    @param var1: variance #1
    @param var2: variance #2
    @param ssize1: sample size #1
    @param ssize2: sample size #2
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float(((var1 / var2)- 1) / (((((var1 / var2) + 1) ** 2) - \
        (4 * (r ** 2) * (var1 / var2))) ** 0.5))
    return test(statistic, FDistribution(ssize1-1, ssize2-1), confidence)

#def t18(**kwargs):
#    """
#    Test 18: Hotelling's T-square test for two series of population means
#
#    To compare the results of two experiments, each of which yields a
#    multivariate result. In another words, we wish to know if the mean pattern
#    obtained from the first experiment agrees with the mean pattern obtained
#    for the second.
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t19(**kwargs):
#    """
#    Test 19: Discriminant test for the origin of a p-fold sample
#
#    To investigate the origin of one species of values for p random variates,
#    when one of two markedly different populations may have produced that
#    particular series."""
#    return test(statistic, Distribution(), confidence)

# def Fishercumulant(m1, m2, m3, m4, ssize, confidence):
    # """Test 20: Fisher's cumulant test for normality of a population

    # To investigate the significance of the difference between frequency
    # distribution based on a given sample and normal frequency distribution
    # with same mean and variance

    # Limitations:
        # 1. Sample size should be large, >50
        # 2. Distributions must have same mean and same variance

    # @param m1: sample moment #1
    # @param m2: sample moment #2
    # @param m3: sample moment #3
    # @param m4: sample moment #4
    # @param ssize: sample size
    # @param confidence: confidence level"""
    # k1 = float(m1 / ssize)
    # k2 = float((ssize * m2) - (m1 **2)) / (ssize * (ssize - 1))
    # k3 = float(((ssize **2) * m3) - (3 * ssize * m2 * m1) + (2 * (m1 **3))) / \
        # (ssize * (ssize-1) * (ssize-2))
    # A = float(((ssize **3) + ssize **2) * m4)
    # B = float(-4 * (((ssize **2) + ssize) * m3 * m1))
    # C = float(-3 * ((ssize **2) * (m2 **2)))
    # C2 = float(-3 * (-ssize * (m2 **2)))
    # D = float(12 * m2 * (m1 **2))
    # E = float(6 * (m1 **4))
    # F = ssize * (ssize-1) * (ssize - 2) * (ssize - 3)
    # k4 = float((A + B + C + C2 + D - E) / F)
    # skewness = (k3 / (k2 * (k2 ** 0.5))) * ((ssize / 6 ) **0.5)
    # kurtosis = (k4 / (k2 **2)) * ((ssize / 24 ) **0.5)
    # statistic = (skewness **2) + (kurtosis **2)
    # print A, B, C, C2, D, E, F, k4, kurtosis, statistic
    # return test(statistic, ChiSquareDistribution(df = ssize - 1), confidence)

# def DixonTest(values, n, confidence):
    # """
    # Test 21: Dixon's test for outliers

    # To investigate the significance of the difference between a suspicious
    # extreme value and other values in the sample.

    # Limitations:
    # 1. sample size should be greater than 3
    # 2. Population which is being sampled is assumed normal

    # @param values: list of values that are arranged in ascending order
    # @param n: sample size
    # @param confidence: confidence level"""
    # if n in range(4, 8):
        # statistic = float((values[1]) - (values[0])) / \
        # float((values[n-1]) - (values[0]))
    # elif n in range(8, 11):
        # statistic = float(values[1] - values[0]) / \
        # float(values[n-2] - values[0])
    # elif n in range(11, 14):
        # statistic = float(values[2] - values[0]) / \
        # float(values[n-2] - values[0])
    # elif n in range(14, 26):
        # statistic = float(values[2] - values[0]) / \
        # float(values[n-3] - values[0])
    # else: print 'Sample size is larger than 25 or smaller than 3'
    # return test(statistic, NormalDistribution(), confidence)

# def FTestAnalysisofVar(s, k, confidence):
    # """
    # Test 22: F-test for K population means (analysis of variance)

    # To test the null hypothesis that K samples are from K populations with
    # the same mean

    # Limitations:
        # 1. It is assumed that the populations are normally distributed
        # and have equal variances and samples are independent of each other

    # @param s: sample datas
    # @param k: number of populations
    # @param confidence: confidence level"""
    # Total = sum([sum(x) for x in s])
    # Mean = [float(sum(x)) / float(len(x)) for x in s]
    # N = sum([len(x) for x in s])
    # s0 = [Mean[i] * Mean[i] * len(s[i])
            # for i in range(len(Mean))]
    # s1 = sum(s0) - A
    # s3 = float((1/k)) * Total
    # s4 = [(len(s[i]) * (Mean[i] - s3))
        # for i in range(len(Mean))]
    # s2 = float((sum(s4))) / float((N - k))
    # statistic = float((s1 - s2)) / float((N - k))
    # return test(statistic, FDistribution(df1 = k, df2 = len(x)), confidence)

def ZCorrProportion(ssize, ny, yn, confidence):
    """
    Test 23: Z-test for correlated proportions

    To investigate the significance of the difference between two correlated
    proportions in opinion surveys. It can also be used for more general
    applications.

    Limitations
        1. The same people are questioned both times (correlated property).
        2. Sample size must be quite large.

    @param ssize: sample size
    @param ny: number answered 'no' in first poll and 'yes' in second poll
    @param yn: number answered 'yes' in first poll and 'no' in second poll
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    sigma = float((ny + yn) - (((ny - yn) ** 2.0) / ssize))
    sigma = float(sqrt(sigma / (ssize * (ssize - 1.0))))
    statistic = float((ny - yn) / (sigma * ssize))
    return test(statistic, NormalDistribution(), confidence)

def Chisq2Variance(ssize, svar, pvar, confidence):
    """
    Test 24: Chi-square test for an assumed population variance

    To investigate the significance of the difference between a population
    variance and an assumed variance value.

    Limitations
        1. Sample from normal distribution

    @param ssize: sample size
    @param svar: sample variance
    @param pvar: population variance (assumed)
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    statistic = float((ssize-1) * svar/pvar)
    return test(statistic, ChiSquareDistribution(df = ssize - 1), confidence)

def F2Count(count1, count2, confidence, time1=0, time2=0, repeat=False):
    """
    Test 25: F-test for two counts (Poisson distribution)

    To investigate the significance of the difference between two counted
    results (based on a Poisson distribution).

    Limitations
        1. Counts must satisfy a Poisson distribution
        2. Samples obtained under same conditions.

    @param count1: count of first sample
    @param count2: count of second sample
    @param repeat: flag for repeated sampling (default = False)
    @param time1: time at which first sample is taken
        (only needed if repeat = True)
    @param time2: time at which second sample is taken
        (only needed if repeat = True)
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    if not repeat:
        statistic = float(count1) / float(count2 + 1)
        numerator = 2 * (count2 + 1)
        denominator = 2 * count1
    else:
        statistic = (float(count1 + 0.5) / float(time1)) / \
                    (float(count2 + 0.5) / float(time2))
        numerator = 2 * count1 + 1
        denominator = 2 * count2 + 1
    return test(statistic, FDistribution(df1 = numerator,
        df2 = denominator), confidence)

#def t26(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t27(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t28(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t29(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t30(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t31(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t32(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t33(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t34(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t35(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def tKolmogorovSmirnov():
#    """Test 36: The Kolmogorov-Smirnov test for comparing two populations
#
#    To investigate the significance of the difference between two population
#    distributions based on the two sample distributions
#
#    Limitations
#        1. Best results obtained when samples are sufficiently large, 15
#        samples or more
#    """
#    return test(statistic, Distribution(), confidence)

def ChisqFit(observed, expected, confidence):
    """
    Test 37: Chi-square test for goodness of fit

    To investigate the significance of the differences between observed data
    arranged in K classes, and the theoretical expected frequencies in the
    K classes.

    Limitations
        1. Observed and theoretical distributions should have same number of
        elements
        2. Same class division for both distributions
        3. Expected frequency of each class should be at least 5

    @param observed: list of observed frequencies (index matched with expected)
    @param expected: list of expected frequencies (index matched with observed)
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    freq = [float((observed[i] - expected[i]) ** 2) / (float(expected[i]))
            for i in range(len(observed))]
    statistic = 0.0
    for x in freq: statistic = statistic + x
    return test(statistic, ChiSquareDistribution(df = len(observed) - 1),
                confidence)

def tx2testofKcounts(T, V, confidence):
    """
    Test 38: The x2-test for compatibility of K counts

    To investigate the significance of the differences between K counts.

    Limitations:
        1. The counts must be obtained under comparable conditions

    @param T: list of time under K counts
    @param V: list of values of K counts
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    R = float(sum(V)) / float(sum(T))
    freq = [((V[i] - (T[i] * R)) ** 2) / float(T[i] * R)
            for i in range(len(V))]
    statistic = sum(freq)
    return test(statistic, ChiSquareDistribution(df = len(V) - 1), confidence)

#def t39(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)

def Chisq2x2(s1, s2, ssize, confidence):
    """
    Test 40: Chi-square test for consistency in 2x2 table

    To investigate the significance of the differences between observed
    frequencies for two dichotomous distributions.

    Limitations
        1. Total sample size (sample 1 + sample 2) must be more than 20
        2. Each cell frequency more than 3

    @param s1: 2-element list or tuple of frequencies for sample #1
    @param s2: 2-element list or tuple of frequencies for sample #2
    @param ssize: sample size
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    s1c1 = s1[0]
    s1c2 = s1[1]
    s2c1 = s2[0]
    s2c2 = s2[1]
    statistic = (float(ssize - 1) * ((float(s1c1 * s2c2) - \
        float(s1c2 * s2c1))**2)) / (float(s1c1 + s1c2) * float(s1c1 + s2c1) * \
        float(s1c2 + s2c2) * float(s2c1 + s2c2))
    return test(statistic, ChiSquareDistribution(df = 1), confidence)

def ChisquareKx2table(c1, c2, k, confidence):
    """Test 41: The x2-test for consistency in a K x 2 table

    To investigate the significance of the differences between K observed
    frequency distributions with a dichotomous classification.

    Limitations:
        1. K sample sizes must be large enough.
        2. It is usually assumed to be satisfied if the cell frequencies are
        equal to 5

    @param c1: class #1 values of sample k
    @param c2: class #2 values of sample k
    @param k: number of samples
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    z = sum(c1)
    nx = sum(c2)
    n = [c1[i] + c2[i] for i in range(len(c1))]
    Total = sum(n)
    A = [x ** 2 for x in c1]
    B = sum([float(A[i]) / float(n[i]) for i in range(len(A))])
    C = (B - (float(z ** 2) / (float(Total))))
    D = float(Total ** 2) / float(z * (Total - z))
    statistic = D * C
    return test(statistic, ChiSquareDistribution(k-1), confidence)

#def t42(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)

def Chisquare2xKtable(s1, s2, k, confidence):
    """Test 43: The x2-test for consistency in a 2 x K table

    To investigate the significance of the differences between two
    distributions based on two samples spread over K classes

    Limitations:
        1. The two samples are sufficiently large
        2. The K classes when put together form a complete series

    @param s1: sample #1 of class k
    @param s2: sample #2 of class k
    @param k: number of classes
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    N1 = sum(s1)
    N2 = sum(s2)
    Total = N1 + N2
    n =[s1[i] + s2[i] for i in range(len(s1))]
    e1 = [float(N1 * x) / float(N1 + N2) for x in n]
    e2 = [float(N2 * x) / float(N1 + N2) for x in n]
    A = [((s1[i] - e1[i]) **2) / e1[i] for i in range(len(s1))]
    B = [((s2[i] - e2[i]) **2) / e2[i] for i in range(len(s2))]
    statistic = sum([A[i] + B[i] for i in range(len(A))])
    return test(statistic, ChiSquareDistribution(k-1), confidence)

# def ChisquarePxQ(d, confidence):
    # """Test 44: The x2-test for independence in a p x q table

    # To investigate the difference in frequency when classified by one
    # attribute after classification by a second attribute

    # Limitations:
        # 1. Sample should be sufficiently large. This condition will be
        # satisfied if each cell frequency is greater than 5

    # @param d: data given as rows
    # @param confidence: confidence level"""
    # p = len(d)
    # q = len(d[0])
    # n01 = [sum(d[i]) for i in range(q)
    # return test(statistic, ChiSquareDistribution((p-1) * (q-1)), confidence)

#def t45(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)

# def t2MediansPairedObs(x, y, confidence):
    # """Test 46: The sign test for two medians (paired observations)

    # To investigate the significance of the difference between the medians of
    # two distributions

    # Limitations:
        # 1. The observations in the two samples should be taken in pairs, one
        # from each distribution, taken under similar conditions. It is not
        # necessary that different pairs should be taken under similar conditions

    # @param x: A list of medians #1
    # @param y: A list of medians #2
    # @param confidence: confidence level"""
    # freq = [x[i] > y[i]
            # for i in range(len(x))]
    # statistic = sum(freq)
    # return test(statistic, Distribution(), confidence)

#def t47(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t2MeansPairedObs(x, y, confidence):
#    """
#    Test 48: The signed rank test fo two means (paired observations)
#
#    Limitations:
#        1.Observations in the two samples should be taken in pairs, one
#        from each distribution, taken under similar conditions. It is not
#        necessary that different pairs should be taken under similar conditions
#
#    @param x: A list of Means
#    @param y: A list of Means
#    @param confidence: confidence level"""
#    # freq = [x[i] - y[i]
#            # for i in range(len(x))]
#    # Rank the difference of means using 0 as the norm
#    # Tabulate the number of minus signs and plus signs
#    # If the number of minus>plus sign, add up the values of the rank of all minus rank values
#    # If the number of plus>minus sign, add up the values of the rank of all plus rank values
#    # return test(statistic, Distribution(), confidence)
#
#def WilcoxonInversion():
#    """Test 49: The Wilcoxon inversion test(U-test)
#
#    """
#    return test(statistic, Distribution(), confidence)

def MedianTestfor2Pop(s1=(9, 6), s2=(6, 9), confidence=0.95):
    """Test 50: The median test of two populations

    To test if two random samples could have come from two populations with
    same frequency distribution

    Limitations:
        1. The two samples are assumed to be reasonably large

    @param s1: 2-element list or tuple of frequencies for sample #1
    @param s2: 2-element list or tuple of frequencies for sample #2
    @param confidence: confidence level

    @see: Chay, ZE, Ling, MHT. 2010. COPADS, II: Chi-Square test, F-Test
    and t-Test Routines from Gopal Kanji's 100 Statistical Tests. The Python
    Papers Source Codes 2:3

    @status: Tested function
    @since: version 0.4
    """
    ls1 = s1[0]
    rs1 = s1[1]
    ls2 = s2[0]
    rs2 = s2[1]
    N = ls1+ls2+rs1+rs2
    statistic = float(((abs((ls1*rs2)-(ls2*rs1))-(N * 0.5))**2)*N) / \
    ((ls1+ls2)*(ls1+rs1)*(ls2+rs2)*(rs1+rs2))
    return test(statistic, ChiSquareDistribution(df=1), confidence)

#def t51(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t52(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t53(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t54(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t55(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t56(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t57(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)

def SpearmanCorrelation(ssize, confidence, R=None, series1=[], series2=[]):
    """
    Test 58: Spearman rank correlation test (paired observations)
    To investigate the significance of the correlation between two series of
    observations obtained in pairs.

    Limitations
        1. Assumes the two population distributions to be continuous
        2. Sample size must be more than 10

    @param R: sum of squared ranks differences
    @param ssize: sample size
    @param series1: ranks of series #1 (not used if R is given)
    @param series2: ranks of series #2 (not used if R is given)
    @param confidence: confidence level

    @see: Ling, MHT. 2009. Ten Z-Test Routines from Gopal Kanji's 100
    Statistical Tests. The Python Papers Source Codes 1:5

    @status: Tested function
    @since: version 0.1
    """
    if R == None:
        R = sum([((series1[i] - series2[i]) ** 2) for i in range(len(series1))])
    statistic = (6.0 * R) - (ssize * ((ssize ** 2) - 1.0))
    statistic = statistic / (ssize * (ssize + 1.0) * sqrt(ssize - 1.0))
    return test(statistic, NormalDistribution(), confidence)

#def t59(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t60(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t61(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t62(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t63(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t64(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t65(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t66(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t67(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t68(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t69(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t70(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t71(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t72(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t73(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t74(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t75(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t76(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t77(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t78(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t79(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t80(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t81(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t82(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t83(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)

def ZtestLogOddsRatio(group1, group2, confidence):
    """Test 84: Z-test for comparing sequential contingencies acoss two groups
    using the 'log odds ratio'

    To test the significance of the difference in sequential connections
    across groups

    Limitations:
        1. This test is applicable when a logit transformation can be used and
        2 X 2 contingency tables are available


    @param group1: group #1 values (row = x, y) & (column a, b) Provide values
    in xa, xb, ya, yb format
    @param group2: group #2 values (row = x, y) & (column a, b) Provide values
    in xa, xb, ya, yb format
    @param confidence: confidence level"""
    x1a1 = float(group1[0])
    x1b1 = float(group1[1])
    y1a1 = float(group1[2])
    y1b1 = float(group1[3])
    x2a2 = float(group2[0])
    x2b2 = float(group2[1])
    y2a2 = float(group2[2])
    y2b2 = float(group2[3])
    C = x1a1 * y1b1
    D = y1a1 * x1b1
    G = C/D
    E = x2a2 * y2b2
    F = y2a2 * x2b2
    H = E/F
    A = log(G, e)
    B = log(H, e)
    statistic = (A - B)/ (((1/x1a1) + (1/x1b1) + (1/y1a1) + (1/y1b1) + \
    (1/x2a2) + (1/x2b2) + (1/y2a2) + (1/y2b2)) **0.5)
    return test(statistic, NormalDistribution(), confidence)

#def t85(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t86(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t87(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t88(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t89(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t90(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t91(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)

#def DubinWatsontest(**kwargs):
#    """
#    Test 92: Dubin-Watson test
#
#    To test whether the error terms in a regression model are autocorrelated
#
#    Limitations:
#        This test is applicable if the autocorrelation parameter and error
#        terms are independently normally distributed with mean zero and
#        variance s2.
#
#    @param confidence: confidence level"""
#    return test(statistic, Distribution(), confidence)
#
#def t93(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def ChisquareProbModel(**kwargs):
#    """
#    Test 94: x2-test for a suitable probabilistic model
#
#    Many experiments yield a set of data, say x1, x2, x3, xn and the
#    experimenter often is interested in determining whether the data can be
#    treated as the observed values of the random sample x1, x2, xn from a
#    given distribution.
#
#    Limitations:
#        this test is applicable if both distributions have the same interval
#        classification and the number of elements. The observed data are
#        observed by random sampling.
#
#    @param confidence: confidence level
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t95(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t96(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t97(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t98(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t99(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)
#
#def t100(**kwargs):
#    """
#    """
#    return test(statistic, Distribution(), confidence)

