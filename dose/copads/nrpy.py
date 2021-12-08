"""
Numerical Recipes in Python.

References:
    - Press, William H., Flannery, Brian P., Teukolsky, Saul A., and Vetterling,
    William T. 1989. Numerical Recipes in Pascal. Cambridge University Press,
    Cambridge (ISBN 978-0521375160)
    - Press, William H., Flannery, Brian P., Teukolsky, Saul A., and Vetterling,
    William T. 1992. Numerical Recipes in C, 2nd edition. Cambridge University
    Press, Cambridge (ISBN 978-0521431088)

Numerical Recipes in C, 2nd edition is freely browsable online at
http://www.nrbook.com/a/bookcpdf.php but is not intended as a substitution
for purchasing the book.

Functions will be named as in the references and will be referred to section
number. For example, the reference "NRP 5.2" refers to Numerical Recipes
in Pascal chapter 5 section 2.

The authors of Numerical Recipes in Pascal (NRP) and Numerical Recipes in
C, 2nd edition (NRC2) explicitly allows the reader to analyze the mathematical
ideas in the codes within the book and owns the re-implemented functions as
stated in NRP and NRC2 that "If you analyze the ideas contained in a program,
and then express those ideas in your own distinct implementation, then that new
program implementation belongs to you" (page xv of NRP; page xviii of NRC2).
Not mentioned in NRP, NRC2 allows the reader a "free licence" (page xviii of
NRC2) which allows the reader to make one machine-readable copy of the C codes
in the book for his/her own use (not distribution) in his/her work, provided
that the source codes are not distributed. As such, the codes in this file
will be called by other functions in COPADS but not for direct use by users
of COPADS - if you intend to call these functions directly, the simplest way
is to own a copy of both NRP and NRC2.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 19th March 2008
"""

import math

from . import constants
from .copadsexceptions import FunctionParameterTypeError
from .copadsexceptions import FunctionParameterValueError
from .copadsexceptions import MaxIterationsException

# medfit global data
ndatat = 0
xt = []
yt = []
aa = 0
abdevt = 0

# Support Functions

def showvec(x, f='%0.6f'):
  s = ''
  for i in x:
    s = s + str(f%i) + ', '
  s = s.strip(', ')
  return '['+s+']'

def nrerror(s):
  print(s)
  sys.exit()

def vector(n, value=0.0):
  a = []
  for i in range(n+1):
    a.append(value)
  return a

def matrix(n, m, value=0.0):
  a = []
  for i in range(n+1):
    a.append(vector(m, value))
  return a

def SQR(a):
  sqrarg = a
  if sqrarg == 0:
    return 0
  return sqrarg*sqrarg

def MAX(a, b):
  if a > b:
    return a
  else:
    return b

def MIN(a, b):
  if a < b:
    return a
  else:
    return b

def SIGN(a, b):
  if b >= 0.0:
    return math.fabs(a)
  return -math.fabs(a)

# End of Support Functions

def bessi0(x):
    """
    Modified Bessel function I-sub-0(x).
    @see: NRP 6.5

    @param x: float number
    @return: modified Bessel function base 0 of x

    @status: Tested function
    @since: version 0.1
    """
    if abs(x) < 3.75:
        y = (x/3.75)*(x/3.75)
        return 1.0 + y * (3.5156229 + y * (3.0899424 + y * (1.2067492 + y * \
                (0.2659732 + y * (0.360768e-1 + y * 0.45813e-2)))))
    else:
        ax = abs(x)
        y = 3.75/ax
        return (math.exp(ax)/math.sqrt(ax)) * (0.39894228 + y * \
            (0.1328592e-1 + \
             y * (0.225319e-2 + y * (-0.157565e-2 + y * (0.916281e-2 + y * \
             (-0.2057706e-1 + y * (0.2635537e-1 + y * (-0.1647633e-1 + y * \
               0.392377e-2))))))))

def bessi1(x):
    """
    Bessel function I-sub-1(x).
    @see: NRP 6.5

    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    if abs(x) < 3.75:
        y = (x/3.75)*(x/3.75)
        return x * (0.5 + y * (0.87890594 + y * (0.51498869 + y * \
            (0.15084934 + \
               y * (0.2658733e-1 + y * (0.301532e-2 + y * 0.32411e-3))))))
    else:
        ax = abs(x)
        y = 3.75/ax
        ans = 0.2282967e-1 + y * (-0.2895312e-1 + y * (0.1787654e-1 - y * \
               0.420059e-2))
        ans = 0.39894228 + y * (-0.3988024e-1 + y * (-0.362018e-2 + y * \
                 (0.163801e-1 + y * (-0.1031555e-1 + y * ans))))
        ans = (math.exp(ax)/math.sqrt(ax))*ans
        if x < 0.0: return -ans
        else: return ans

def bessj0(x):
    """
    Bessel function J-sub-0(x).
    @see: NRP 6.4

    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    if abs(x) < 8.0:
        y = x*x
        return (57568490574.0 + y * (-13362590354.0 + y * (651619640.7 + \
               y * (-11214424.18 + y * (77392.33017 + y * \
                                        (-184.9052456))))))/ \
               (57568490411.0 + y * (1029532985.0 + y * (9494680.718 + y * \
               (59272.64853 + y * (267.8532712 + y * 1.0)))))
    else:
        ax = abs(x)
        z = 8.0/ax
        y = z*z
        xx = ax - 0.785398164
        ans1 = 1.0 + y * (-0.1098628627e-2 + y * (0.2734510407e-4 + y * \
              (-0.2073370639e-5 + y * 0.2093887211e-6)))
        ans2 = -0.156249995e-1 + y * (0.1430488765e-3 + y * \
                                      (-0.6911147651e-5 + \
             y * (0.7621095161e-6 - y * 0.934945152e-7)))
        return math.sqrt(0.636619772 / ax) * (math.cos(xx) * ans1 - z * \
               math.sin(xx) * ans2)

def bessj1(x):
    """
    Bessel function J-sub-1(x).
    @see: NRP 6.4

    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    if abs(x) < 8.0:
        y = x*x
        ans1 = x * (72362614232.0 + y * (-7895059235.0 + y * \
                                         (242396853.1 + y * \
              (-2972611.439 + y * (15704.4826 + y * (-30.16036606))))))
        ans2 = 144725228442.0 + y * (2300535178.0 + y * (18583304.74 + y * \
             (99447.43394 + y * (376.9991397 + y))))
        return ans1 / ans2
    else:
        ax = abs(x)
        x = 8.0 / ax
        y = z*z
        xx = ax - 2.356194491
        ans1 = 1.0 + y * (0.183105e-2 + y * (-0.3516396496e-4 + y * \
             (0.2457520174e-5 + y * (-0.240337019e-6))))
        ans2 = 0.04687499995 + y * (-0.2002690873e-3 + y * \
                                    (0.8449199096e-5 + y * \
            (-0.88228987e-6 + y * 0.105787412e-6)))
        if x < 0.0:
            return math.sqrt(0.636619772 / ax) * \
                   (math.cos(xx) * ans1 - z * \
                    math.sin(xx) * ans2)
        else:
            return -1 * math.sqrt(0.636619772 / ax) * \
                   (math.cos(xx) * ans1 - \
                  z * math.sin(xx) * ans2)

def bessk(n, x):
    """Bessel function K-sub-n(x). @see: NRP 6.5

    @param n: integer, more than 1 - modified n-th Bessel function
    @param x: positive integer
    @return: modified n-th Bessel function of x
    """
    if n < 2:
        raise FunctionParameterValueError('''n must be more than 1 - \
            use bessk0 or bessk1 for n = 0 or 1 respectively''')
    else:
        tox = 2.0/x
        bkm = bessk0(x)
        bk = bessk1(x)
        for j in range(1, n):
            bkp = bkm * j * tox * bk
            bkm = bk
            bk = bkp
        return bk

def bessk0(x):
    """Bessel function K-sub-0(x).
    @see: NRP 6.5

    @param x: positive integer
    @return: n-th Bessel function of x"""
    if x <= 2.0:
        y = x * x/4.0
        return (-math.log(x/2.0) * bessi0(x)) + (-0.57721566 + y * \
                (0.4227842 + y * (0.23069756 + y * (0.348859e-1 + y * \
                (0.262698e-2 + y * (0.1075e-3 + y * 0.74e-5))))))
    else:
        y = 2.0/x
        return (math.exp(-x)/math.sqrt(x)) * (1.25331414 + y * \
                (-0.7832358e-1 + y * (0.2189568e-1 + y * (-0.1062446e-1 + \
                y * (0.587872e-2 + y * (-0.25154e-2 + y * 0.53208e-3))))))

def bessk1(x):
    """
    Bessel function K-sub-1(x).
    @see: NRP 6.5

    @param x: positive integer
    @return: n-th Bessel function of x"""
    if x <= 2.0:
        y = x*x/4.0
        return (math.log(x/2.0) * bessi1(x)) + (1.0/x) * (1.0 + y * \
                (0.15443144 + y * (-0.67278579 + y * (-0.18156897 + y * \
                (-0.1919402e-2 + y * (-0.110404e-2 + y * (-0.4686e-4)))))))
    else:
        y = 2.0/x
        return (math.exp(-x)/math.sqrt(x)) * (1.25331414 + y * \
                (0.23498619 + y * (-0.365562e-1 + y * (0.1504268e-1 + y * \
                (-0.780353e-2 + y * (0.325614e-2 + y * (-0.68245e-3)))))))

def bessy(n, x):
    """
    Bessel function Y-sub-n(x).
    @see: NRP 6.4

    @param n: integer, more than 1 - n-th Bessel function
    @param x: positive integer
    @return: n-th Bessel function of x

    @status: Tested function
    @since: version 0.1
    """
    if n < 2:
        raise FunctionParameterValueError('''n must be more than 1 - \
            use bessy0 or bessy1 for n = 0 or 1 respectively''')
    else:
        tox = 2.0/x
        by = bessy1(x)
        bym = bessy0(x)
        for j in range(1, n):
            byp = j * tox * by - bym
            bym = by
            by = byp
        return by

def bessy0(x):
    """
    Bessel function Y-sub-0(x).
    @see: NRP 6.4
    Depend: bessj0

    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    if x < 8.0:
        y = x*x
        ans1 = -2957821389.0 + y * (7062834065.0 + y * (-512359803.6 + y * \
                (10879881.29 + y * (-86327.92757 + y * 228.4622733))))
        ans2 = 40076544269.0 + y * (745249964.8 + y * (7189466.438 + y * \
               (47447.2647 + y * (226.1030244 + y * 1.0))))
        return (ans1 / ans2) + 0.636619772 * bessj0(x) * math.log(x)
    else:
        z = 8.0 / x
        y = z*z
        xx = x - 0.785398164
        ans1 = 1.0 + y * (-0.1098628627e-2 + y * (0.2734510407e-4 + y * \
              (-0.2073370639e-5 + y * 0.2093887211e-6)))
        ans2 = -0.1562499995e-1 + y * (0.1430488765e-3 + y * \
                (-0.6911147651e-5 + y * (0.7621095161e-6 + y * \
                (-0.934945152e-7))))
        ans = math.sin(xx) * ans1 + z * math.cos(xx) * ans2
        return math.sqrt(0.636619772 / x) * ans

def bessy1(x):
    """
    Bessel function Y-sub-1(x).
    @see: NRP 6.4
    Depend: bessj1

    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    if abs(x) < 8.0:
        y = x*x
        ans1 = x * (-0.4900604943e13 + y * (0.1275274390e13 + y * \
                (-0.5153438139e11 + y * (0.7349264551e9 + y * \
                (-0.4237922726e7 + y * 0.8511937935e4)))))
        ans2 = 0.2499580570e14 + y * (0.4244419664e12 + y * (0.3733650367e10 + \
                y * (0.2245904002e8 + y * (0.1020426050e6 + y * \
                (0.3549632885e3 + y)))))
        return (ans1/ans2) + 0.636619772 * (bessj1(x) * math.log(x, math.e) - (1.0/x))
    else:
        z = 8.0 / x
        y = z*z
        xx = x - 2.356194491
        ans1 = 1.0 + y * (0.183105e-2 + y * (-0.3516396496e-4 + y * \
             (0.2457520174e-5 + y * (-0.240337019e-6))))
        ans2 = 0.04687499995 + y * (-0.2002690873e-3 + y * (0.8449199096e-5 + \
                y * (-0.88228987e-6 + y * 0.105787412e-6)))
        if x < 0.0: return math.sqrt(0.636619772 / x) * (math.cos(xx) * \
                            ans1 + z * math.sin(xx) * ans2)
        else: return math.sqrt(0.636619772 / x) * (math.sin(xx) * \
                    ans1 + z * math.cos(xx) * ans2)

def beta(z, w):
    """
    Beta function.
    Depend: gammln
    @see: NRP 6.1
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @param z: float number
    @param w: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    return math.exp(gammln(z) + gammln(w) - gammln(z+w))

def betacf(a, b, x):
    """
    Continued fraction for incomplete beta function.
    Adapted from salstat_stats.py of SalStat (www.sf.net/projects/salstat)
    @see: NRP 6.3
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4
    """
    iter_max = 200
    eps = 3.0e-7

    bm = az = am = 1.0
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    bz = 1.0 - qab * x / qap
    for i in range(iter_max + 1):
        em = float(i + 1)
        tem = em + em
        d = em * (b - em) * x / ((qam + tem) * (a + tem))
        ap = az + d * am
        bp = bz + d * bm
        d = -(a + em) * (qab + em) * x / ((qap + tem) * (a + tem))
        app = ap + d * az
        bpp = bp + d * bz
        aold = az
        am = ap / bpp
        bm = bp / bpp
        az = app / bpp
        bz = 1.0
        if (abs(az - aold) < (eps * abs(az))):
            return az

def betai(a, b, x):
    """
    Incomplete beta function

    I-sub-x(a,b) = 1/B(a,b)*(Integral(0,x) of t^(a-1)(1-t)^(b-1) dt)

    where a,b>0 and B(a,b) = G(a)*G(b)/(G(a+b)) where G(a) is the gamma
    function of a.

    Adapted from salstat_stats.py of SalStat (www.sf.net/projects/salstat)
    Depend: betacf, gammln
    @see: NRP 6.3

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @status: Tested function
    @since: version 0.1
    """
    if (x < 0.0 or x > 1.0):
        raise ValueError('Bad value for x: %s' % x)
    if (x == 0.0 or x == 1.0):
        bt = 0.0
    else:
        bt = math.exp(gammln(a+b) - gammln(a) - gammln(b) + a *
                      math.log(x) + b * math.log(1.0-x))
    if (x < (a + 1.0) / (a + b + 2.0)):
        return bt * betacf(a, b, x) / float(a)
    else:
        return 1.0 - bt * betacf(b, a, 1.0 - x) / float(b)

def bico(n, k):
    """
    Binomial coefficient. Returns n!/(k!(n-k)!)
    Depend: factln, gammln
    @see: NRP 6.1

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @param n: total number of items
    @param k: required number of items
    @return: floating point number

    @status: Tested function
    @since: version 0.1
    """
    return math.floor(math.exp(factln(n) - factln(k) - factln(n-k)))

def chebev(a, b, c, m, x):
    """Chebyshev evaluation.
    @see: NRP 5.6

    @param a: float number
    @param b: float number
    @param c: list of Chebyshev coefficients produced by chebft with the
    same 'a' and 'b'
    @param m:
    @param x:
    @return: float number - function value
    """
    if (x-a)*(x-b) > 0.0:
        raise FunctionParameterValueError('x must be between a and b')
    else:
        d, dd = 0.0, 0.0
        y = (2.0 * x - a - b) / (b - a)
        y2 = 2.0 * y
        for i in range(m, 0, -1):
            sv = d
            d = y2 * d - dd + c[i]
            dd = sv
        return y * d - dd + 0.5 * c[0]

def covsrt(covar, ma, ia, mfit):
    '''
    '''
    for i in range(mfit+1, ma+1):
        for j in range(1,i+1):
            covar[i][j] = 0.0
            covar[j][i] = 0.0
    k = mfit
    for j in range(ma, 0, -1):
        if (ia[j] == 1):
            for i in range(1, ma+1):
                covar[i][k] = covar[i][j]
                covar[i][j] = covar[i][k]
            for i in range(1, ma+1):
                covar[k][i] = covar[j][i]
                covar[j][i] = covar[k][i]
            k = k - 1
    return (covar, ma, ia)

def erf(x):
    """
    Error function (a special incomplete gamma function) equivalent to
    gammp(0.5, x^2) for x => 0. In this routine, gammp is by-passed and gser
    and gcf are used directly.
    Depend: gser. gcf, gammln
    @see: NRP 6.2

    @param x: float number
    @return: float number
    """
    if x < 1.5:
        return -1*gser(0.5, x)[0]
    else:
        return 1.0-gcf(0.5, x)[0]

def erfc(x):
    """
    Complementary error function (a special incomplete gamma function)
    equivalent to gammq(0.5, x^2) which is equivalent to 1 - gammp(0.5, x^2)
    for x => 0.0
    Depend: gammp, gammq, gser, gcf, gammln
    @see: NRP 6.2

    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    if x < 0.0: return 1.0 + gammp(0.5, x*x)
    else: return gammq(0.5, x*x)

def erfcc(x):
    """
    Complementary error function similar to erfc(x) but with fractional error
    lesser than 1.2e-7.
    @see: NRP 6.2

    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    z = abs(x)
    t = 1.0 / (1.0 + 0.5*z)
    r = t * math.exp(-z*z-1.26551223+t*(1.00002368+t*(0.37409196+
        t*(0.09678418+t*(-0.18628806+t*(0.27886807+
        t*(-1.13520398+t*(1.48851587+t*(-0.82215223+
        t*0.17087277)))))))))
    if (x >= 0.0):
        return r
    else:
        return 2.0 - r

def expdev(x):
    """Depends: ran3
    @see: NRP 7.2"""
    return -1.0 * math.log(ran3(x))

def factln(n):
    """
    Natural logarithm of factorial: ln(n!)
    @see: NRP 6.1

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @param n: positive integer
    @return: natural logarithm of factorial of n
    """
    return gammln(n + 1.0)

def fgauss(x, a, y, dyda, na):
    y = 0.0
    for i in range(1, na, 3):
        arg = (x-a[i+1]) / a[i+2]
        ex = exp(-arg*arg)
        fac = a[i] * ex * 2.0 * arg
        y = y + (a[i]*ex)
        dyda[i] = ex
        dyda[i+1] = fac / a[i+2]
        dyda[i+2] = (fac*arg) / a[i+2]
    return (y, dyda)

def gammln(n):
    """
    Complete Gamma function.
    @see: NRP 6.1
    @see: http://mail.python.org/pipermail/python-list/2000-June/671838.html
    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @param n: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    gammln_cof = [76.18009173, -86.50532033, 24.01409822,
                  -1.231739516e0, 0.120858003e-2, -0.536382e-5]
    x = n - 1.0
    tmp = x + 5.5
    tmp = (x + 0.5) * math.log(tmp) - tmp
    ser = 1.0
    for j in range(6):
        x = x + 1.
        ser = ser + gammln_cof[j] / x
    return tmp + math.log(2.50662827465 * ser)

def gammp(a, x):
    """
    Gamma incomplete function, P(a,x).
    P(a,x) = (1/gammln(a)) * integral(0, x, (e^-t)*(t^(a-1)), dt)
    Depend: gser, gcf, gammln
    @see: NRP 6.2

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @param a: float number
    @param x: float number
    @return: float number

    @status: Tested function
    @since: version 0.1
    """
    if (x < 0.0 or a <= 0.0):
        raise ValueError('Bad value for a or x: %s, %s' % (a, x))
    if (x < a + 1.0):
        return gser(a, x)[0]
    else:
        return 1.0 - gcf(a, x)[0]

def gammq(a, x):
    """
    Incomplete gamma function: Q(a, x) = 1 - P(a, x) = 1 - gammp(a, x)
    Also commonly known as Q-equation.
    @see: http://mail.python.org/pipermail/python-list/2000-June/671838.html

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @status: Tested function
    @since: version 0.1
    """
    if (x < 0.0 or a <= 0.0):
        raise ValueError('Bad value for a or x: %s, %s' % (a, x))
    if (x < a + 1.0):
        a = gser(a, x)[0]
        return 1.0 - a
    else:
        return gcf(a, x)[0]

def gcf(a, x, itmax=200, eps=3.e-7):
    """
    Continued fraction approx'n of the incomplete gamma function.
    @see: http://mail.python.org/pipermail/python-list/2000-June/671838.html

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @status: Tested function
    @since: version 0.1
    """
    gln = gammln(a)
    gold = 0.0
    a0 = 1.0
    a1 = x
    b0 = 0.0
    b1 = 1.0
    fac = 1.0
    n = 1
    while n <= itmax:
        an = n
        ana = an - a
        a0 = (a1 + a0 * ana) * fac
        b0 = (b1 + b0 * ana) * fac
        anf = an * fac
        a1 = x * a0 + anf * a1
        b1 = x * b0 + anf * b1
        if (a1 != 0.0):
            fac = 1.0 / a1
            g = b1 * fac
            if (abs((g - gold) / g) < eps):
                return (g * math.exp(-x + a * math.log(x) - gln), gln)
            gold = g
        n = n + 1
    raise MaxIterationsException('Maximum iterations reached: %s'
                                 % abs((g - gold) / g))

def gser(a, x, itmax=700, eps=3.e-7):
    """
    Series approximation to the incomplete gamma function.
    @see: http://mail.python.org/pipermail/python-list/2000-June/671838.html

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @status: Tested function
    @since: version 0.1
    """
    gln = gammln(a)
    if (x < 0.0):
        raise ValueError('Bad value for x: %s' % a)

    if (x == 0.0):
        return(0.0, 0.0)
    ap = a
    total = 1.0 / a
    delta = total
    n = 1
    while n <= itmax:
        ap = ap + 1.0
        delta = delta * x / ap
        total = total + delta
        if (abs(delta) < abs(total) * eps):
            return (total * math.exp(-x + a * math.log(x) - gln), gln)
        n = n + 1
    raise MaxIterationsException('Maximum iterations reached: %s, %s'
                                 % (abs(delta), abs(total) * eps))

def mdian1(data):
    """Calculates the median of a list of numerical values using sorting.
    @see: NRP 13.2

    @param data: a 1-dimensional list of numerical data
    @return: value of median
    """
    data.sort()
    n2 = len(data) % 2
    if n2 % 2 == 1: return data[n2+1]
    else: return 0.5*(data[n2] + data[n2+1])

def mnbrak(ax, bx, func):
    '''
    '''
    GOLD = 1.618034
    GLIMIT = 100.0
    TINY = 1.0e-20
    dum = 0
    def SHFT(a, b, c, d):
        return (b, c, d)
    fa = func(ax)
    fb = func(bx)
    if (fb > fa):
        (dum, ax, bx) = SHFT(dum, ax, bx, dum)
        (dum, fb, fa) = SHFT(dum, fb, fa, dum)
    cx = bx + (GOLD * (bx-ax))
    fc = func(cx)
    while (fb > fc):
        r = (bx-ax) * (fb-fc)
        q = (bx-cx) * (fb-fa)
        u = bx - \
            ((((bx-cx) * q) - ((bx-ax) * r)) / \
            (2.0 * SIGN(FMAX(fabs(q-r), TINY), q-r)))
        ulim = bx + (GLIMIT * (cx-bx))
        if ((bx-u) * (u-cx)) > 0.0:
            fu = func(u)
            if (fu < fc):
                ax = bx
                bx = u
                fa = fb
                fb = fu
                return (ax, bx, cx, fa, fb, fc)
            elif (fu > fb):
                cx = u
                fc = fu
                return (ax, bx, cx, fa, fb, fc)
            u = cx + (GOLD * (cx-bx))
            fu = func(u)
        elif ((cx-u) * (u-ulim)) > 0.0:
            fu = func(u)
            if (fu < fc):
                (bx, cx, u) = SHFT(bx, cx, u, cx+GOLD*(cx-bx))
                (fb, fc, fu) = SHFT(fb, fc, fu, func(u))
        elif ((u-ulim) * (ulim-cx)) >= 0.0:
            u = ulim
            fu = func(u)
        else:
            u = cx + (GOLD * (cx-bx))
            fu = func(u)
        (ax, bx, cx) = SHFT(ax, bx, cx, u)
        (fa, fb, fc) = SHFT(fa, fb, fc, fu)
    return (ax, bx, cx, fa, fb, fc)

def moment(data):
    """Calculates moment from a list of numerical data. @see: NRP 13.1

    @param data: a 1-dimensional list of numerical values
    @return: (ave, adev, sdev, var, skew, kurt) where
        - ave = mean
        - adev = average deviation
        - sdev = standard deviation
        - var = variance
        - skew = skew
        - kurt = kurtosis
    """
    s = 0.0
    for d in data: s = s + d
    ave = s/len(data)
    adev = 0.0
    svar = 0.0
    skew = 0.0
    kurt = 0.0
    for d in data:
        s = d - ave
        adev = adev + abs(s)
        p = s*s
        svar = svar + p
        p = p*s
        skew = skew + p
        p = p*s
        kurt = kurt + p
    adev = adev/len(data)
    svar = svar/(len(data) - 1)
    sdev = math.sqrt(svar)
    if svar != 0.0:
        skew = skew/(len(data)*sdev*sdev*sdev)
        kurt = (kurt/(len(data)*svar*svar)) - 3.0
    return (ave, adev, sdev, var, skew, kurt)

def pythag(a, b):
    '''
    '''
    a = math.fabs(a)
    b = math.fabs(b)
    if (a > b):
        return a * math.sqrt(1.0 + SQR(b/a))
    else:
        if (b == 0.0):
            return 0.0
        else:
            return b * math.sqrt(1.0 + SQR(a/b))

def qgaus(a, b, func):
    """
    @see: NRP 4.5"""
    x = [0.1488743389, 0.4333953941, 0.6794095682, 0.8650633666, 0.97390652]
    w = [0.2955242247, 0.2692667193, 0.2190863625, 0.1494513491, 0.06667134]
    xm = 0.5 * (b + a)
    xr = 0.5 * (b - a)
    ss = 0.0
    for i in range(5):
        dx = xr * x[i]
        ss = ss + w[i] * (func(xm + dx) + func(xm - dx))
    return xr * ss

def svdvar(v, ma, w, cvm):
    '''
    '''
    wti = vector(ma)
    for i in range(1, ma+1):
        wti[i] = 0.0
        if (w[i] > 0):
            wti[i] = 1.0 / (w[i]*w[i])
    for i in range(1, ma+1):
        for j in range(1, i+1):
            sum = 0.0
        for k in range(1, ma+1):
            sum = sum + (v[i][k]*v[j][k]*wti[k])
        cvm[j][i] = sum
        cvm[i][j] = sum
    return cvm

#def adi(): raise NotImplementedError
#def amoeba(): raise NotImplementedError
#def anneal(): raise NotImplementedError
#def avevar(): raise NotImplementedError
#def badluk(): raise NotImplementedError
#def balanc(): raise NotImplementedError
#def bcucof(): raise NotImplementedError
#def bcuint(): raise NotImplementedError
#def bnldev(): raise NotImplementedError
#def brent(): raise NotImplementedError
#def bsstep(): raise NotImplementedError
#def caldat(): raise NotImplementedError
#def cel(): raise NotImplementedError
#def chder(): raise NotImplementedError
#def chebtf(): raise NotImplementedError
#def chebpc(): raise NotImplementedError
#def chint(): raise NotImplementedError
#def chsone(): raise NotImplementedError
#def chstwo(): raise NotImplementedError
#def cntab1(): raise NotImplementedError
#def cntab2(): raise NotImplementedError
#def convlv(): raise NotImplementedError
#def correl(): raise NotImplementedError
#def cosft(): raise NotImplementedError
#def dbrent(): raise NotImplementedError
#def ddpoly(): raise NotImplementedError
#def des(): raise NotImplementedError
#def df1dim(): raise NotImplementedError
#def dfpmin(): raise NotImplementedError
#def eclass(): raise NotImplementedError
#def eclazz(): raise NotImplementedError
#def eigsrt(): raise NotImplementedError
#def el2(): raise NotImplementedError
#def elmhes(): raise NotImplementedError
#def eulsum(): raise NotImplementedError
#def evlmem(): raise NotImplementedError
#def f1dim(): raise NotImplementedError
#def fit(): raise NotImplementedError
#def fixrts(): raise NotImplementedError
#def fleg(): raise NotImplementedError
#def flmoon(): raise NotImplementedError
#def four1(): raise NotImplementedError
#def fourn(): raise NotImplementedError
#def fpoly(): raise NotImplementedError
#def frprmn(): raise NotImplementedError
#def ftest(): raise NotImplementedError
#def gamdev(): raise NotImplementedError
#def gasdev(): raise NotImplementedError
#def gauleg(): raise NotImplementedError
#def gaussj(): raise NotImplementedError
#def golden(): raise NotImplementedError
#def hqr(): raise NotImplementedError
#def hunt(): raise NotImplementedError
#def indexx(): raise NotImplementedError
#def irbit1(): raise NotImplementedError
#def irbit2(): raise NotImplementedError
#def jacobi(): raise NotImplementedError
#def julday(): raise NotImplementedError
#def kendl1(): raise NotImplementedError
#def kendl2(): raise NotImplementedError
#def ksone(): raise NotImplementedError
#def kstwo(): raise NotImplementedError
#def laguer(): raise NotImplementedError
#def lfit(): raise NotImplementedError
#def linmin(): raise NotImplementedError
#def locate(): raise NotImplementedError
#def lubksb(): raise NotImplementedError
#def ludcmp(): raise NotImplementedError
#def mdian2(): raise NotImplementedError
#def medfit(): raise NotImplementedError
#def memcof(): raise NotImplementedError
#def midexp(): raise NotImplementedError
#def midinf(): raise NotImplementedError
#def midpnt(): raise NotImplementedError
#def midsql(): raise NotImplementedError
#def midsqu(): raise NotImplementedError
#def mmid(): raise NotImplementedError
#def mnbrak(): raise NotImplementedError
#def mnewt(): raise NotImplementedError
#def mprove(): raise NotImplementedError
#def mrqmin(): raise NotImplementedError
#def odeint(): raise NotImplementedError
#def pcshft(): raise NotImplementedError
#def pearsn(): raise NotImplementedError
#def piksr2(): raise NotImplementedError
#def piksrt(): raise NotImplementedError
#def plgndr(): raise NotImplementedError
#def poidev(): raise NotImplementedError
#def poicoe(): raise NotImplementedError
#def polcof(): raise NotImplementedError
#def poldiv(): raise NotImplementedError
#def polin2(): raise NotImplementedError
#def polint(): raise NotImplementedError
#def powell(): raise NotImplementedError
#def predic(): raise NotImplementedError
#def probks(): raise NotImplementedError
#def pzextr(): raise NotImplementedError
#def qcksrt(): raise NotImplementedError
#def qromb(): raise NotImplementedError
#def qromo(): raise NotImplementedError
#def qroot(): raise NotImplementedError
#def qsimp(): raise NotImplementedError
#def qtrap(): raise NotImplementedError
#def quad3d(): raise NotImplementedError
#def ran0(): raise NotImplementedError
#def ran1(): raise NotImplementedError
#def ran2(): raise NotImplementedError
#def ran3(): raise NotImplementedError
#def ran4(): raise NotImplementedError
#def rank(): raise NotImplementedError
#def ratint(): raise NotImplementedError
#def realft(): raise NotImplementedError
#def rk4(): raise NotImplementedError
#def rkdumb(): raise NotImplementedError
#def rkqc(): raise NotImplementedError
#def rtbis(): raise NotImplementedError
#def rtflsp(): raise NotImplementedError
#def rtnewt(): raise NotImplementedError
#def rtsafe(): raise NotImplementedError
#def rtsec(): raise NotImplementedError
#def rzextr(): raise NotImplementedError
#def scrsho(): raise NotImplementedError
#def sfroid(): raise NotImplementedError
#def shell(): raise NotImplementedError
#def shoot(): raise NotImplementedError
#def shootf(): raise NotImplementedError
#def simplx(): raise NotImplementedError
#def sinft(): raise NotImplementedError
#def smooft(): raise NotImplementedError
#def sncndn(): raise NotImplementedError
#def solvde(): raise NotImplementedError
#def sor(): raise NotImplementedError
#def sort(): raise NotImplementedError
#def sort2(): raise NotImplementedError
#def sort3(): raise NotImplementedError
#def sparse(): raise NotImplementedError
#def spctrm(): raise NotImplementedError
#def spear(): raise NotImplementedError
#def splie2(): raise NotImplementedError
#def splin2(): raise NotImplementedError
#def spline(): raise NotImplementedError
#def splint(): raise NotImplementedError
#def svbksb(): raise NotImplementedError
#def svdcmp(): raise NotImplementedError
#def svdfit(): raise NotImplementedError
#def toeplz(): raise NotImplementedError
#def tptest(): raise NotImplementedError
#def tqli(): raise NotImplementedError
#def trapzd(): raise NotImplementedError
#def tred2(): raise NotImplementedError
#def tridag(): raise NotImplementedError
#def ttest(): raise NotImplementedError
#def tutest(): raise NotImplementedError
#def twofft(): raise NotImplementedError
#def vander(): raise NotImplementedError
#def zbrac(): raise NotImplementedError
#def zbrak(): raise NotImplementedError
#def zbrent(): raise NotImplementedError
#def zroots(): raise NotImplementedError
#def airy(): raise NotImplementedError
#def amebsa(): raise NotImplementedError
#def anorm2(): raise NotImplementedError
#def arcmak(): raise NotImplementedError
#def arcode(): raise NotImplementedError
#def arcsum(): raise NotImplementedError
#def banbks(): raise NotImplementedError
#def bandec(): raise NotImplementedError
#def banmul(): raise NotImplementedError
#def beschb(): raise NotImplementedError
#def bessik(): raise NotImplementedError
#def bessjy(): raise NotImplementedError
#def broydn(): raise NotImplementedError
#def choldc(): raise NotImplementedError
#def cholsl(): raise NotImplementedError
#def cisi(): raise NotImplementedError
#def cosft1(): raise NotImplementedError
#def cosft2(): raise NotImplementedError
#def crank(): raise NotImplementedError
#def cyclic(): raise NotImplementedError
#def daub4(): raise NotImplementedError
#def dawson(): raise NotImplementedError
#def decchk(): raise NotImplementedError
#def dfridr(): raise NotImplementedError
#def dftint(): raise NotImplementedError
#def ei(): raise NotImplementedError
#def elle(): raise NotImplementedError
#def ellf(): raise NotImplementedError
#def ellpi(): raise NotImplementedError
#def expint(): raise NotImplementedError
#def fasper(): raise NotImplementedError
#def fitexy(): raise NotImplementedError
#def fourfs(): raise NotImplementedError
#def fred2(): raise NotImplementedError
#def fredex(): raise NotImplementedError
#def fredin(): raise NotImplementedError
#def frenel(): raise NotImplementedError
#def gaucof(): raise NotImplementedError
#def gauher(): raise NotImplementedError
#def gaujac(): raise NotImplementedError
#def gaulag(): raise NotImplementedError
#def hpsel(): raise NotImplementedError
#def hpsort(): raise NotImplementedError
#def hufapp(): raise NotImplementedError
#def hufdec(): raise NotImplementedError
#def hufenc(): raise NotImplementedError
#def hufmak(): raise NotImplementedError
#def hypdrv(): raise NotImplementedError
#def hypgeo(): raise NotImplementedError
#def hypser(): raise NotImplementedError
#def icrc(): raise NotImplementedError
#def icrc1(): raise NotImplementedError
#def igray(): raise NotImplementedError
#def ks2d1s(): raise NotImplementedError
#def ks2d2s(): raise NotImplementedError
#def linbcg(): raise NotImplementedError
#def lnsrch(): raise NotImplementedError
#def lop(): raise NotImplementedError
#def machar(): raise NotImplementedError
#def mgfas(): raise NotImplementedError
#def mglin(): raise NotImplementedError
#def miser(): raise NotImplementedError
#def mp2dfr(): raise NotImplementedError
#def mpdiv(): raise NotImplementedError
#def mpinv(): raise NotImplementedError
#def mppi(): raise NotImplementedError
#def mrqcof(): raise NotImplementedError
#def newt(): raise NotImplementedError
#def orthog(): raise NotImplementedError
#def pade(): raise NotImplementedError
#def pccheb(): raise NotImplementedError
#def period(): raise NotImplementedError
#def psdes(): raise NotImplementedError
#def pwt(): raise NotImplementedError
#def pwtest(): raise NotImplementedError
#def qrdcmp(): raise NotImplementedError
#def qrsolv(): raise NotImplementedError
#def qrupdt(): raise NotImplementedError
#def quadvl(): raise NotImplementedError
#def ratlsq(): raise NotImplementedError
#def ratval(): raise NotImplementedError
#def rc(): raise NotImplementedError
#def rd(): raise NotImplementedError
#def rf(): raise NotImplementedError
#def rj(): raise NotImplementedError
#def rkqs(): raise NotImplementedError
#def rlft3(): raise NotImplementedError
#def rofunc(): raise NotImplementedError
#def savgol(): raise NotImplementedError
#def select(): raise NotImplementedError
#def selip(): raise NotImplementedError
#def simpr(): raise NotImplementedError
#def sobseq(): raise NotImplementedError
#def sphbes(): raise NotImplementedError
#def sphfpt(): raise NotImplementedError
#def sphoot(): raise NotImplementedError
#def spread(): raise NotImplementedError
#def sprsax(): raise NotImplementedError
#def sprsin(): raise NotImplementedError
#def sprspm(): raise NotImplementedError
#def sprstm(): raise NotImplementedError
#def sprstp(): raise NotImplementedError
#def sprstx(): raise NotImplementedError
#def stifbs(): raise NotImplementedError
#def stiff(): raise NotImplementedError
#def stoerm(): raise NotImplementedError
#def vegas(): raise NotImplementedError
#def voltra(): raise NotImplementedError
#def wt1(): raise NotImplementedError
#def wtn(): raise NotImplementedError
#def wwghts(): raise NotImplementedError
#def zrhqr(): raise NotImplementedError
#def zriddr(): raise NotImplementedError

def cdf_binomial(k, n, p):
    """
    Cummulative density function of Binomial distribution. No reference
    implementation.
    Depend: betai, betacf, gammln
    @see: NRP 6.3

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @param k: number of times of event occurrence in n trials
    @param n: total number of trials
    @param p: probability of event occurrence per trial
    @return: float number - Binomial probability
    """
    return betai(k, n - k + 1, p)

def cdf_poisson(k, x):
    """
    Cummulative density function of Poisson distribution from 0 to k - 1
    inclusive. No reference implementation.
    Depend: gammq, gser, gcf, gammln
    @see: NRP 6.2

    @see: Ling, MHT. 2009. Compendium of Distributions, I: Beta, Binomial, Chi-
    Square, F, Gamma, Geometric, Poisson, Student's t, and Uniform. The Python
    Papers Source Codes 1:4

    @param k: number of times of event occurrence
    @param x: mean of Poisson distribution
    @return: float number - Poisson probability of k - 1 times of occurrence
    with the mean of x
    """
    return gammq(k, x)
