"""
Data Structures and Algorithms for Data Collected from One or More Samples.

The following functions were adapted from http://www.nmr.mgh.harvard.edu/
Neural_Systems_Group/gary/python/stats.py (assumes 1-dimensional list as 
input):
    - geometricMean
    - harmonicMean
    - arithmeticMean
    - median
    - medianScore
    - mode
    - moment
    - variation
    - skew
    - kurtosis

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>
"""

import math

from .statisticsdistribution import Distribution
from .copadsexceptions import FunctionParameterTypeError
from .copadsexceptions import FunctionParameterValueError
from .operations import summation

from . import nrpy

class SingleSample:
    """
    Class to hold a single sample, and provides calculations on the sample
    """
    data = None
    rowcount = 0
    name = None
    summary = {}
    
    def __init__(self, data, name='Sample 1'):
        self.data = data
        self.rowcount = len(self.data)
        self.name = name
        
    def geometricMean(self):
        """
        Calculates the geometric mean of the data
        
        @status: Tested method
        @since: version 0.1
        """
        mult = 1.0
        one_over_n = 1.0 / len(self.data)
        for item in self.data: mult = mult * math.pow(item, one_over_n)
        return mult
    
    def harmonicMean(self):
        """
        Calculates the harmonic mean of the data
        
        @status: Tested method
        @since: version 0.1
        """
        sum = 0.000001
        for item in self.data:
            if item != 0: sum = sum + 1.0/item
            else: sum = sum + 1.0/0.001
        return len(self.data) / sum
    
    def arithmeticMean(self):
        """
        Returns the arithematic mean of the data
        
        @status: Tested method
        @since: version 0.1
        """
        sum = 0
        for item in self.data: sum = sum + item
        return sum / float(len(self.data))
    
    def moment(self, moment=1):
        """
        Calculates the nth moment about the mean for the data
        """
        if moment == 1:
            return 0.0
        else:
            mn = self.arithmeticMean()
            n = len(self.data)
            s = 0
            for x in self.data:
                s = s + (x - mn) ** moment
            return s / float(n)
        
    def skew(self):
        """
        Returns the skewness of the data, as defined in Numerical
        Recipies (alternate defn in CRC Standard Probability and
        Statistics, p.6.)
        
        @status: Tested method
        @since: version 0.1
        """
        return self.moment(3) / math.pow(self.moment(2), 1.5)

    def kurtosis(self):
        """
        Returns the kurtosis of the data, as defined in Numerical
        Recipies (alternate defn in CRC Standard Probability and
        Statistics, p.6.)
        
        @status: Tested method
        @since: version 0.1
        """
        return self.moment(4) / math.pow(self.moment(2), 2.0)
    
    def variation(self):
        """
        Returns the coefficient of variation in percentage, as
        defined in CRC Standard Probability and Statistics, p.6.
        Ref: http://en.wikipedia.org/wiki/Coefficient_of_variation
        
        @status: Tested method
        @since: version 0.1
        """
        return 100.0 * self.summary['stdev'] / self.summary['aMean']

    def range(self):
        """
        Returns the range of the data (maximum - minimum)
        
        @status: Tested method
        @since: version 0.1
        """
        self.data.sort()
        return float(self.data[-1]) - float(self.data[0])

    def variance(self):
        """
        Returns the variance of the data
        
        @status: Tested method
        @since: version 0.1
        """
        sum = 0.0
        mean = self.arithmeticMean()
        for item in self.data:
            sum = sum + (float(item) - float(mean)) ** 2
        return sum / float(len(self.data) - 1)
    
    def __str__(self):
        return str(self.summary)
        
    def fullSummary(self):
        self.summary['gMean'] = self.geometricMean()
        self.summary['hMean'] = self.harmonicMean()
        self.summary['aMean'] = self.arithmeticMean()
        self.summary['skew'] = self.skew()
        self.summary['kurtosis'] = self.kurtosis()
        self.summary['variance'] = self.variance()
        self.summary['stdev'] = self.summary['variance'] ** 0.5
        self.summary['variation'] = self.variation()
        self.summary['range'] = self.range()
        self.summary['median'] = nrpy.mdian1(self.data)
    
    
class SampleDistribution(Distribution):
    def __init__(self, sampleData):
        self.sample = sampleData

        
class TwoSample:
    """
    Class to hold a two samples, and provides calculations on the samples
    """
    sample = {}
    sample_name = []
    def __init__(self, data1, name1, data2, name2):
        if name1 == '': name1 = 'Sample 1'
        if name2 == '': name2 = 'Sample 2'
        self.sample_name = [name1, name2]
        self.sample[name1] = SingleSample(list(data1), name1)
        self.sample[name2] = SingleSample(list(data2), name2)

    def getSample(self, name):
        try: return self.sample[name].data
        except KeyError: return []

    def listSamples(self):
        return self.sample_name

    def covariance(self):
        """
        Calculates covariance using the formula: Cov(xy) = E(xy) - E(x)E(y)
        
        @status: Tested method
        @since: version 0.3
        """
        sname = self.listSamples()
        if self.sample[sname[0]].data == self.sample[sname[1]].data: return 1.0
        if self.sample[sname[0]].rowcount == self.sample[sname[1]].rowcount:
            slen = self.sample[sname[0]].rowcount
        elif self.sample[sname[0]].rowcount > self.sample[sname[1]].rowcount:
            slen = self.sample[sname[1]].rowcount
        else: slen = self.sample[sname[0]].rowcount
        xy = SingleSample([self.sample[sname[0]].data[i] * \
                            self.sample[sname[1]].data[i]
                            for i in range(slen)], 'temporary')
        mean_xy = xy.arithmeticMean()
        mean_x = self.sample[sname[0]].arithmeticMean()
        mean_y = self.sample[sname[1]].arithmeticMean()
        return mean_xy - (mean_x * mean_y)
    
    def linear_regression(self):
        '''
        Calculates the first order linear regression model in the form of
        "y = mx + c" from the 2 samples where the first sample (data1 and
        name1 in initialization method) is taken as "X" and the second 
        sample (data2 and name2 in initialization method is taken as "Y".
        
        @return: Tuple of (gradient, intercept)
        
        @status: Tested method
        @since: version 0.1
        '''
        sname = self.listSamples()
        if self.sample[sname[0]].rowcount == self.sample[sname[1]].rowcount:
            slen = self.sample[sname[0]].rowcount
        elif self.sample[sname[0]].rowcount > self.sample[sname[1]].rowcount:
            slen = self.sample[sname[1]].rowcount
        else: slen = self.sample[sname[0]].rowcount
        mean_x = self.sample[sname[0]].arithmeticMean()
        mean_y = self.sample[sname[1]].arithmeticMean()
        error_x = [self.sample[sname[0]].data[i] - mean_x 
                   for i in range(slen)]
        error_y = [self.sample[sname[1]].data[i] - mean_y 
                   for i in range(slen)]
        gradient = sum([error_x[index] * error_y[index]
                        for index in range(len(error_x))]) / \
                   sum([error_x[index] * error_x[index]
                        for index in range(len(error_x))])
        intercept = mean_y - (gradient * mean_x)
        return (gradient, intercept)
    
    def pearson(self):
        """
        Calculates the Pearson's product-moment coefficient by the formula
        
        (N * sum_xy) - (sum_x * sum_y)
        --------------------------------------------------------------
        ((N * sum_x2 - (sum_x)**2) * (N * sum_y2 - (sum_y)**2)) ** 0.5
        
        @status: Tested method
        @since: version 0.1
        """
        sname = self.listSamples()
        if self.sample[sname[0]].rowcount == self.sample[sname[1]].rowcount:
            slen = self.sample[sname[0]].rowcount
        elif self.sample[sname[0]].rowcount > self.sample[sname[1]].rowcount:
            slen = self.sample[sname[1]].rowcount
        else: slen = self.sample[sname[0]].rowcount
        sum_x = summation([self.sample[sname[0]].data[i] 
                            for i in range(slen)])
        sum_x2 = summation([self.sample[sname[0]].data[i] * \
                            self.sample[sname[0]].data[i] 
                            for i in range(slen)])
        sum_y = summation([self.sample[sname[1]].data[i] 
                            for i in range(slen)])
        sum_y2 = summation([self.sample[sname[1]].data[i] * \
                            self.sample[sname[1]].data[i]
                            for i in range(slen)])
        sum_xy = summation([self.sample[sname[0]].data[i] * \
                            self.sample[sname[1]].data[i]
                            for i in range(slen)])
        numerator = (slen * sum_xy) - (sum_x * sum_y)
        denominator_x = (slen * sum_x2) - (sum_x * sum_x)
        denominator_y = (slen * sum_y2) - (sum_y * sum_y)
        return float(numerator / ((denominator_x * denominator_y) ** 0.5))
    
"""        
class MultiSample:
    sample = {}
    def __init__(self): pass
    
    def addSample(self, data, name):
        if name == '':
            try:
                temp = self.sample['Sample ' + str(len(self.sample))]
                import random
                name = 'Sample ' + str(int(random.random() * 1000000))
            except KeyError:
                name = 'Sample ' + str(len(self.sample) + 1)
        if type(sample) == list or type(sample) == tuple:
            sample = SingleSample(list(sample), name)
            self.sample[name] = sample
        else:
            self.sample[sample.name] = sample
            
    def getSample(self, name):
        try: return self.sample[name].data
        except KeyError: return []

    def listSamples(self):
        return self.sample.keys()
"""    
    
