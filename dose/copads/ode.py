'''
Ordinary Differential Equation (ODE) Solvers.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 20th December 2014
'''

def boundary_checker(y, boundary, type):
    '''
    Private function - called by ODE solvers to perform boundary checking 
    of variable values and reset them to specific values if the original 
    values fall out of the boundary values.
    
    Boundary parameter takes the form of a dictionary with variable number 
    as key and a list of [<boundary value>, <value to set if boundary is 
    exceeded>]. For example, the following dictionary for lower boundary 
    (type = 'lower') {'1': [0.0, 0.0], '5': [2.0, 2.0]} will set the lower 
    boundary of variable y[0] and [5] to 0.0 and 2.0 respectively. This 
    also allows for setting to a different value - for example, {'1': [0.0, 
    1.0]} will set variable y[0] to 2.0 if the original y[0] value is 
    negative.
    
    @param y: values for variables
    @type y: list
    @param boundary: set of values for boundary of variables
    @type boundary: dictionary
    @param type: the type of boundary to be checked, either 'upper' (upper 
    boundary) or 'lower' (lower boundary)
    '''
    for k in list(boundary.keys()):
        if y[int(k)] < boundary[k][0] and type == 'lower':
            y[int(k)] = boundary[k][1]
        if y[int(k)] > boundary[k][0] and type == 'upper':
            y[int(k)] = boundary[k][1]
    return y

def Euler(funcs, x0, y0, step, xmax, nonODEfunc=None,
          lower_bound=None, upper_bound=None,
          overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y0' = funcs(x0, y0), using 
    Euler method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        y1 = [0]*n
        for i in range(n):
            try: y1[i] = y0[i] + (step*funcs[i](x0, y0))
            except TypeError: pass
            except ZeroDivisionError: y0[i] = zerodivision
            except OverflowError: y0[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0

def Heun(funcs, x0, y0, step, xmax, nonODEfunc=None,
         lower_bound=None, upper_bound=None,
         overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y0' = funcs(x0, y0), using Heun's 
    method, which is also known as Runge-Kutta 2nd method or Trapezoidal method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1 = [0]*n
        y1, y2 = [0]*n, [0]*n
        for i in range(n): 
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for i in range(n): 
            try: y1[i] = y0[i] + step*f1[i]
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y2[i] = overflow
        for i in range(n): 
            try: y2[i] = y0[i] + 0.5*step*(f1[i] + funcs[i](x0+step, y1))
            except TypeError: pass
            except ZeroDivisionError: y2[i] = zerodivision
            except OverflowError: y2[i] = overflow
        return y2
    while x0 < xmax:
        y2 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y2 = boundary_checker(y2, lower_bound, 'lower')
        if upper_bound: 
            y2 = boundary_checker(y2, upper_bound, 'upper')
        y0 = y2
        x0 = x0 + step
        yield [x0] + y0
    
def RK3(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y0' = funcs(x0, y0), using third
    order Runge-Kutta method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3 = [0]*n, [0]*n, [0]*n
        y1, y2 = [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n): 
            try: f1[i] = step * funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for i in range(n): 
            y1[i] = y0[i] + 0.5*f1[i]
        for i in range(n): 
            try: f2[i] = step * funcs[i](x0 + 0.5*step, y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for i in range(n): 
            y1[i] = y0[i] - f1[i] + 2*f2[i]
        for i in range(n): 
            try: f3[i] = step * funcs[i](x0 + step, y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for i in range(n): 
            try: y1[i] = y0[i] + (f1[i] + 4*f2[i] + f3[i])/6.0
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0
        
def RK4(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fourth
    order Runge-Kutta method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3, f4 = [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.5*step*f1[j])
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(0.5*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.5*step*f2[j])
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(0.5*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (step*f3[j])
        for i in range(n):
            try: f4[i] = funcs[i]((x0+step), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    (f1[i] + (2.0*f2[i]) + (2.0*f3[i]) + f4[i]) / 6.0)
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0
        
def RK38(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fourth
    order Runge-Kutta method, 3/8 rule.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3, f4 = [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (step*f1[j]/3.0)
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(step/3.0)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (-1*step*f1[j]/3.0) + (step*f2[j])
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(2*step/3.0)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (step*f1[j]) + (-step*f2[j]) + (step*f3[j])
        for i in range(n):
            try: f4[i] = funcs[i]((x0+step), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    (f1[i] + (3.0*f2[i]) + (3.0*f3[i]) + f4[i]) / 8.0)
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0

def CK4(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fourth 
    order Cash-Karp method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3, f4, f5, f6 = [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.2*step*f1[j])
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(0.2*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.075*step*f1[j]) + (0.225*step*f2[j])
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(0.3*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.3*step*f1[j]) + (-0.9*step*f2[j]) + \
                    (1.2*step*f3[j])
        for i in range(n):
            try: f4[i] = funcs[i]((x0+(0.6*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (-11*step*f1[j]/54.0) + (2.5*step*f2[j]) + \
                    (-70*step*f3[j]/27.0) + (35*step*f4[j]/27.0)
        for i in range(n):
            try: f5[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f5[i] = zerodivision
            except OverflowError: f5[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (1631*step*f1[j]/55296) + (175*step*f2[j]/512) + \
                    (575*step*f3[j]/13824) + (44275*step*f4[j]/110592) + \
                    (253*step*f5[j]/4096)
        for i in range(n):
            try: f6[i] = funcs[i](x0+(0.875*step), y1)
            except TypeError: pass
            except ZeroDivisionError: f6[i] = zerodivision
            except OverflowError: f6[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    ((2825*f1[i]/27648) + (18575*f3[i]/48384) + \
                     (13525*f4[i]/55296) + (277*f5[i]/14336) + \
                     (0.25*f6[i])))
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0
        
def CK5(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fifth 
    order Cash-Karp method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3, f4, f5, f6 = [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.2*step*f1[j])
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(0.2*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.075*step*f1[j]) + (0.225*step*f2[j])
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(0.3*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.3*step*f1[j]) + (-0.9*step*f2[j]) + \
                    (1.2*step*f3[j])
        for i in range(n):
            try: f4[i] = funcs[i]((x0+(0.6*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (-11*step*f1[j]/54.0) + (2.5*step*f2[j]) + \
                    (-70*step*f3[j]/27.0) + (35*step*f4[j]/27.0)
        for i in range(n):
            try: f5[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f5[i] = zerodivision
            except OverflowError: f5[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (1631*step*f1[j]/55296.0) + \
                    (175*step*f2[j]/512.0) + (575*step*f3[j]/13824.0) + \
                    (44275*step*f4[j]/110592.0) + (253*step*f5[j]/4096.0)
        for i in range(n):
            try: f6[i] = funcs[i](x0+(0.875*step), y1)
            except TypeError: pass
            except ZeroDivisionError: f6[i] = zerodivision
            except OverflowError: f6[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    ((37*f1[i]/378.0) + (250*f3[i]/621.0) + \
                     (125*f4[i]/594.0) + (512*f6[i]/1771.0)))
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0
        
def RKF4(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fourth 
    order Runge-Kutta-Fehlberg method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3, f4, f5, f6 = [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.25*step*f1[j])
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(0.25*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (3*step*f1[j]/32.0) + (9*step*f2[j]/32.0)
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(3*step/8.0)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (1932*step*f1[j]/2197.0) + \
                    (-7200*step*f2[j]/2197.0) + \
                    (7296*step*f3[j]/2197.0)
        for i in range(n):
            try: f4[i] = funcs[i]((x0+(12*step/13.0)), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (439*step*f1[j]/216.0) + (-8.0*step*f2[j]) + \
                    (3680*step*f3[j]/513.0) + (-845*step*f4[j]/4104.0)
        for i in range(n):
            try: f5[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f5[i] = zerodivision
            except OverflowError: f5[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (-8*step*f1[j]/27.0) + (2.0*step*f2[j]) + \
                    (-3544*step*f3[j]/2565.0) + (1859*step*f4[j]/4104.0) + \
                    (-11*step*f5[j]/40.0)
        for i in range(n):
            try: f6[i] = funcs[i](x0+(0.5*step), y1)
            except TypeError: pass
            except ZeroDivisionError: f6[i] = zerodivision
            except OverflowError: f6[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    ((25*f1[i]/216.0) + (1408*f3[i]/2565.0) + \
                     (2197*f4[i]/4104.0) + (-0.2*f5[i])))
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0
      
def RKF5(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fifth 
    order Runge-Kutta-Fehlberg method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3, f4, f5, f6 = [0]*n, [0]*n, [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.25*step*f1[j])
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(0.25*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (3*step*f1[j]/32.0) + (9*step*f2[j]/32.0)
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(3*step/8.0)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (1932*step*f1[j]/2197.0) + \
                    (-7200*step*f2[j]/2197.0) + \
                    (7296*step*f3[j]/2197.0)
        for i in range(n):
            try: f4[i] = funcs[i]((x0+(12*step/13.0)), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (439*step*f1[j]/216.0) + \
                    (-8.0*step*f2[j]) + (3680*step*f3[j]/513.0) + \
                    (-845*step*f4[j]/4104.0)
        for i in range(n):
            try: f5[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f5[i] = zerodivision
            except OverflowError: f5[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (-8*step*f1[j]/27.0) + (2.0*step*f2[j]) + \
                    (-3544*step*f3[j]/2565.0) + (1859*step*f4[j]/4104.0) + \
                    (-11*step*f5[j]/40.0)
        for i in range(n):
            try: f6[i] = funcs[i](x0+(0.5*step), y1)
            except TypeError: pass
            except ZeroDivisionError: f6[i] = zerodivision
            except OverflowError: f6[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    ((16*f1[i]/135.0) + (6656*f3[i]/12825.0) + \
                     (28561*f4[i]/56430.0) + (-9*f5[i]/50) + \
                     (2*f6[i]/55)))
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0
        
def DP4(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fourth 
    order Dormand-Prince method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3 = [0]*n, [0]*n, [0]*n
        f4, f5, f6, f7 = [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.2*step*f1[j])
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(0.2*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (3*step*f1[j]/40.0) + (9*step*f2[j]/40.0)
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(0.3*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (44*step*f1[j]/45.0) + (-56*step*f2[j]/15.0) + \
                    (32*step*f3[j]/9.0)
        for i in range(n):
            try: f4[i] = funcs[i]((x0+(0.8*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (19372*step*f1[j]/6561.0) + \
                    (-25360*step*f2[j]/2187.0) + \
                    (64448*step*f3[j]/6561.0) + \
                    (-212*step*f4[j]/729.0)
        for i in range(n):
            try: f5[i] = funcs[i](x0+(8*step/9.0), y1)
            except TypeError: pass
            except ZeroDivisionError: f5[i] = zerodivision
            except OverflowError: f5[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (9017*step*f1[j]/3168.0) + \
                    (-355*step*f2[j]/33.0) + (46732*step*f3[j]/5247.0) + \
                    (49*step*f4[j]/176.0) + (-5103*step*f5[j]/18656.0)
        for i in range(n):
            try: f6[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f6[i] = zerodivision
            except OverflowError: f6[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (35*step*f1[j]/384.0) + \
                    (500*step*f3[j]/1113.0) + (125*step*f4[j]/192.0) + \
                    (-2187*step*f5[j]/6784.0) + (11*step*f6[j]/84.0)
        for i in range(n):
            try: f7[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f7[i] = zerodivision
            except OverflowError: f7[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    ((5179*f1[i]/57600.0) + (7571*f3[i]/16695.0) + \
                     (393*f4[i]/640.0) + (-92097*f5[i]/339200.0) + \
                     (187*f6[i]/2100.0) + (f7[i]/40.0)))
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0
        
def DP5(funcs, x0, y0, step, xmax, nonODEfunc=None,
        lower_bound=None, upper_bound=None,
        overflow=1e100, zerodivision=1e100):
    '''
    Generator to integrate a system of ODEs, y' = f(x, y), using fifth 
    order Dormand-Prince method.
    
    A function (as nonODEfunc parameter) can be included to modify one or 
    more variables (y0 list). This function will not be an ODE (not a 
    dy/dt). This can be used to consolidate the modification of one or 
    more variables at each ODE solving step. For example, y[0] = y[1] / y[2] 
    can be written as 
    
    >>> def modifying_function(y, step):
            y[0] = y[1] / y[2]
            return y
    
    This function must take 'y' (variable list) and 'step' (time step) as 
    parameters and must return 'y' (the modified variable list). This 
    function will execute before boundary checking at each time step.
    
    Upper and lower boundaries of one or more variable can be set using 
    upper_bound and lower_bound parameters respectively. These parameters 
    takes the form of a dictionary with variable number as key and a list 
    of [<boundary value>, <value to set if boundary is exceeded>]. For 
    example, the following dictionary for lower boundary {'1': [0.0, 0.0], 
    '5': [2.0, 2.0]} will set the lower boundary of variable y[0] and y[5] 
    to 0.0 and 2.0 respectively. This also allows for setting to a different 
    value - for example, {'1': [0.0, 1.0]} will set variable y[0] to 2.0 if 
    the original y[0] value is negative.
    
    @param funcs: system of differential equations
    @type funcs: list
    @param x0: initial value of x-axis, which is usually starting time
    @type x0: float
    @param y0: initial values for variables
    @type y0: list
    @param step: step size on the x-axis (also known as step in calculus)
    @type step: float
    @param xmax: maximum value of x-axis, which is usually ending time
    @type xmax: float
    @param nonODEfunc: a function to modify the variable list (y0)
    @type nonODEfunc: function
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    '''
    yield [x0] + y0
    def solver(funcs, x0, y0, step):
        n = len(funcs)
        f1, f2, f3 = [0]*n, [0]*n, [0]*n
        f4, f5, f6, f7 = [0]*n, [0]*n, [0]*n, [0]*n
        y1 = [0]*n
        for i in range(n):
            try: f1[i] = funcs[i](x0, y0)
            except TypeError: pass
            except ZeroDivisionError: f1[i] = zerodivision
            except OverflowError: f1[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (0.2*step*f1[j])
        for i in range(n):
            try: f2[i] = funcs[i]((x0+(0.2*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f2[i] = zerodivision
            except OverflowError: f2[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (3*step*f1[j]/40.0) + (9*step*f2[j]/40.0)
        for i in range(n):
            try: f3[i] = funcs[i]((x0+(0.3*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f3[i] = zerodivision
            except OverflowError: f3[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (44*step*f1[j]/45.0) + (-56*step*f2[j]/15.0) + \
                    (32*step*f3[j]/9.0)
        for i in range(n):
            try: f4[i] = funcs[i]((x0+(0.8*step)), y1)
            except TypeError: pass
            except ZeroDivisionError: f4[i] = zerodivision
            except OverflowError: f4[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (19372*step*f1[j]/6561.0) + \
                    (-25360*step*f2[j]/2187.0) + \
                    (64448*step*f3[j]/6561.0) + \
                    (-212*step*f4[j]/729.0)
        for i in range(n):
            try: f5[i] = funcs[i](x0+(8*step/9.0), y1)
            except TypeError: pass
            except ZeroDivisionError: f5[i] = zerodivision
            except OverflowError: f5[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (9017*step*f1[j]/3168.0) + \
                    (-355*step*f2[j]/33.0) + (46732*step*f3[j]/5247.0) + \
                    (49*step*f4[j]/176.0) + (-5103*step*f5[j]/18656.0)
        for i in range(n):
            try: f6[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f6[i] = zerodivision
            except OverflowError: f6[i] = overflow
        for j in range(n):
            y1[j] = y0[j] + (35*step*f1[j]/384.0) + \
                    (500*step*f3[j]/1113.0) + (125*step*f4[j]/192.0) + \
                    (-2187*step*f5[j]/6784.0) + (11*step*f6[j]/84.0)
        for i in range(n):
            try: f7[i] = funcs[i](x0+step, y1)
            except TypeError: pass
            except ZeroDivisionError: f7[i] = zerodivision
            except OverflowError: f7[i] = overflow
        for i in range(n):
            try: y1[i] = y0[i] + (step * \
                    ((35*f1[i]/384.0) + (500*f3[i]/1113.0) + \
                     (125*f4[i]/192.0) + (-2187*f5[i]/6784.0) + \
                     (11*f6[i]/84.0)))
            except TypeError: pass
            except ZeroDivisionError: y1[i] = zerodivision
            except OverflowError: y1[i] = overflow
        return y1
    while x0 < xmax:
        y1 = solver(funcs, x0, y0, step)
        if nonODEfunc:
            y1 = nonODEfunc(y1, step)
        if lower_bound: 
            y1 = boundary_checker(y1, lower_bound, 'lower')
        if upper_bound: 
            y1 = boundary_checker(y1, upper_bound, 'upper')
        y0 = y1
        x0 = x0 + step
        yield [x0] + y0

def _equation_constructor(expressions={},
                          parameters={},
                          variables=[]):
    '''
    Private function to support ODE_constructor to generate ODE function 
    for each ODE.
    
    @param expressions: dictionary of expressions for ODE(s). Please see 
    above documentation. 
    @param parameters: dictionary of parameter values to be substituted 
    into the ODE equations
    @param variables: list of additional variables to be tagged for 
    substitution(s)
    @return: tuple of (<list of generated ODE functions>, <list of tagged 
    variables>) 
    '''
    statements = []
    # Generate ODE function, one at a time
    for name in expressions.keys():
        # Generate ODE function definition
        stmt = '\ndef %s(t, y):' % str(name)
        expression = expressions[name]
        if type(expression) == type(''): expression = [expression]
        count = 1
        # Generate list of expression(s) for current ODE function
        exp_list = []
        variables = list(set(list(variables) + list(expressions.keys())))
        for exp in expression:
            # Substitute parameter/variable values 
            for k in parameters.keys():
                exp = exp.replace(str(k), str(parameters[k]))
            #variables = list(set(variables + expressions.keys()))
            
            for v in variables:
                exp = exp.replace(str(v), 'v@'+str(v))
            # Generate expression codes
            stmt = stmt + '\n    exp_%s = %s' % (str(count), str(exp))
            exp_list.append('exp_%s' % str(count))
            count = count + 1
        # Compile generated expressions into return value
        return_stmt = '\n    return ' + ' + '.join(exp_list)
        stmt = stmt + return_stmt
        statements.append(stmt)
    return (statements, variables)

def _modifying_constructor(modifying_expressions):
    '''
    Private function to support ODE_constructor to generate function code 
    for modifying expressions.
    
    @param modifying_expressions: list of expressions to modify the 
    variables
    @return: generated function code
    '''
    stmt = '\ndef modifying_expression(y, step):'
    for exp in modifying_expressions:
        stmt = stmt + '\n    %s' % str(exp)
    stmt = stmt + '\n    return y'
    return stmt

def ODE_constructor(scriptfile,
                    resultsfile,
                    time=(0.0, 0.1, 100.0),
                    ODE_solver='RK4',
                    expressions={},
                    parameters={},
                    initial_conditions={},
                    modifying_expressions=[],
                    lower_bound=None, 
                    upper_bound=None,
                    overflow=1e100, 
                    zerodivision=1e100):
    '''
    Function to construct an ODE simulation script file from given 
    definitions.
    
    For example, the following system of ODEs::
    
        d(human)/dt = birth - zombied - death
        d(zombie)/dt = zombied + resurrected - destroyed
        d(dead)/dt = death + destroyed - resurrected
        
        birth = 0
        zombied = 0.0095 * human * zombie
        death = 0.0001 * human
        resurrected = 0.0002 * dead
        destroyed = 0.0003 * human * zombie
         
        where initially (t0), 
         
        number of humans = 500
        number of zombies = 0
        number of dead = 0
         
        and with the following boundaries
         
        number of humans > 0
        number of zombies < 10000
        number of dead < 10000
         
        and there is an influx of 5 humans per day into the infected village
    
    can be specified as 
    
    >>> scriptfile = 'zombie_attack.py'
        resultsfile = 'zombie_data.csv'
        time = (0.0, 0.1, 100.0)
        ODE_solver = 'RK4'
        expressions = {'human': ['birth_rate',
                                 '- (transmission_rate * human * zombie)',
                                 '- (death_rate * human)'],
                       'zombie': ['(transmission_rate * human * zombie)',
                                  '(resurrection_rate * dead)',
                                  '- (destroy_rate * human * zombie)'],
                       'dead': ['(death_rate * human)',
                                '(destroy_rate * human * zombie)',
                                '- (resurrection_rate * dead)']}
        parameters = {'birth_rate': 0.0,           # birth rate
                      'transmission_rate': 0.0095, # transmission percent   
                      'death_rate': 0.0001,        # natural death percent  
                      'resurrection_rate': 0.0002, # resurect percent  
                      'destroy_rate':0.0003        # destroy percent   
                      }
        initial_conditions = {'human': 500.0,
                              'zombie': 0.0, 
                              'dead': 0.0}
        modifying_expression = ['human = human + (5 * step)']
        lower_bound = {'human': [0.0, 0.0]}
        upper_bound = {'zombie': [10000.0, 10000.0],
                       'dead': [10000.0, 10000.0]}
        overflow = 1e100
        zerodivision = 1e100
    
    @param scriptfile: name of Python file for the generated ODE script 
    file
    @type scriptfile: string
    @param resultsfile: name of ODE simulation results file (CSV file), 
    which will be included into the generated simulation script file
    @type resultsfile: string    
    @param time: tuple of time parameters for simulation in the format of 
    (<start time>, <time step>, <end time>). Default = (0.0, 0.1, 100.0)
    @param ODE_solver: name of ODE solver to use. Default = RK4
    @param expressions: dictionary of expressions for ODE(s). Please see 
    above documentation. 
    @param parameters: dictionary of parameter values to be substituted 
    into the ODE equations
    @param modifying_expressions: list of expressions to modify the 
    variables
    @param initial_conditions: dictionary of initial conditions for each 
    ODE
    @param lower_bound: set of values for lower boundary of variables
    @type lower_bound: dictionary
    @param upper_bound: set of values for upper boundary of variables
    @type upper_bound: dictionary
    @param overflow: value (usually a large value) to assign in event of 
    over flow error (usually caused by a large number) during integration. 
    Default = 1e100.
    @type overflow: float
    @param zerodivision: value (usually a large value) to assign in event 
    of zero division error, which results in positive infinity, during 
    integration. Default = 1e100.
    @type zerodivision: float
    @return: generated ODE codes for the entire script
    @rtype: list
    '''
    statements = [] 
    initial_conditions_list = initial_conditions.keys()
    # Construct ODE functions
    (ODE_functions,
     variables) = _equation_constructor(expressions,
                                        parameters,
                                        initial_conditions_list)
    # Construct modifying expression
    mexpression = _modifying_constructor(modifying_expressions)
    # Generate ODE functions/equations table
    table = {}
    count = 0
    for v in initial_conditions_list:
        table[str(v)] = str(count)
        count = count + 1
    # Generate lower boundary table
    if lower_bound != None:
        lbound = {}
        for k in lower_bound.keys():
            lbound[table[k]] = lower_bound[k]
    else:
        lbound = None
    # Generate upper boundary table
    if upper_bound != None:
        ubound = {}
        for k in upper_bound.keys():
            ubound[table[k]] = upper_bound[k]
    else:
        ubound = None
    # Write ode module import
    statements.append('import ode\n\n')  
    # Generate variable array and statements
    statements.append('y = range(%s)\n' % str(len(variables)))
    count = 0
    for k in initial_conditions_list:
        statements.append('y[%s] = %s\n' % \
                          (str(count), str(initial_conditions[k])))
        count = count + 1
    statements.append('\n')
    # Perform variable replacements in ODE functions, and write functions
    for funct in ODE_functions:
        for v in table.keys():
            funct = funct.replace('v@'+v, 'y[%s]' % table[v])
        statements.append(funct)
    statements.append('\n\n')
    # Perform variable replacements in modifying expression, and write out
    for v in table.keys():
        mexpression = mexpression.replace(v, 'y[%s]' % table[v])
    statements.append(mexpression)
    statements.append('\n\n')
    # Generate ODE assignment array and statements
    statements.append('ODE = range(%s)\n' % str(len(variables)))
    count = 0
    for k in initial_conditions_list:
        statements.append('ODE[%s] = %s\n' % (str(count), str(k)))
        count = count + 1
    statements.append('\n')
    # Generate ODE execution codes
    statements.append('stime = %s \n' % str(time[0]))
    statements.append('step = %s \n' % str(time[1]))
    statements.append('etime = %s \n' % str(time[2]))
    statements.append('lower_bound = %s \n' % str(lbound))
    statements.append('upper_bound = %s \n' % str(ubound))
    statements.append('overflow = %s \n' % str(overflow))
    statements.append('zerodivision = %s \n' % str(zerodivision))
    statements.append('\n')
    statements.append("f = open('%s', 'w')\n" % str(resultsfile))
    headers = ['time'] + [str(k)for k in initial_conditions.keys()]
    headers = ','.join(headers)
    statements.append("f.write('%s' + '\\n') \n" % headers)
    statements.append('\n')
    statements.append('for x in ode.%s(ODE, stime, y, step, etime, \n' % \
                      str(ODE_solver))
    statements.append('        modifying_expression, \n') 
    statements.append('        lower_bound, upper_bound, \n') 
    statements.append('        overflow, zerodivision): \n')
                      
    statements.append("    f.write(','.join([str(item) for item in x]) + '\\n')")
    statements.append('\n')
    statements.append('f.close()')
    # Write generated codes into script file
    sfile = open(scriptfile, 'w')
    sfile.writelines(statements)
    sfile.close()
    return statements
    