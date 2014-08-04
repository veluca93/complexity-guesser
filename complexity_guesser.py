#!/usr/bin/env python2

import math

def poly(val, deg):
    return val**deg

def polylog(val, deg):
    return math.log(1+val)**deg

def mean(l):
    return sum(l)/len(l)

def cov(l1, l2):
    m1 = mean(l1)
    m2 = mean(l2)
    return sum([(l1[i] - m1)*(l2[i] - m2) for i in xrange(len(l1))])

def stddev(l):
    m = mean(l)
    return (cov(l, l)/len(l))**.5

def getdim(variables, function):
    val = 1
    for i in xrange(len(function)):
        for f, p in function[i].iteritems():
            val *= f(variables[i], p)
    return val

def getcoeff(function, data):
    dims = [getdim(i[0], function) for i in data]
    times = [i[1] for i in data]
    if cov(dims, dims) == 0:
        b = 0
        a = sum(times)/sum(dims)
    else:
        b = cov(dims, times) / cov(dims, dims)
        a = mean(times) - b * mean(dims)
    err = abs((times[0] - (a*dims[0]+b))/dims[0])
    return (a, b, err)

def guess(varnames, data):
    data = dict(data).items()
    data.sort()
    function = []
    for i in varnames:
        tmp = dict()
        tmp[poly] = 1
        tmp[polylog] = 0
        function.append(tmp)
    steps = []
    for i in range(len(varnames)):
        steps.append((i, poly, 1))
        steps.append((i, poly, -1))
#    for i in range(len(varnames)):
#        steps.append((i, poly, 0.5))
#        steps.append((i, poly, 0.5))
#    for i in range(len(varnames)):
#        steps.append((i, poly, 1./3))
#        steps.append((i, poly, 1./3))
    for i in range(len(varnames)):
        steps.append((i, polylog, 1))
        steps.append((i, polylog, -1))
    while True:
        err = getcoeff(function, data)[2]
        improved = False
        for step in steps:
            function[step[0]][step[1]] += step[2]
            errn = getcoeff(function, data)[2]
            if errn < err:
                improved = True
                continue
            function[step[0]][step[1]] -= step[2]
        if improved:
            continue
        break
    if sum(fn != {poly: 0, polylog: 0} for fn in function) == 0:
        desc = "O(1)"
    else:
        desc = "O("
        for i in xrange(len(function)):
            if function[i][poly] == 1:
                desc += "%s " % varnames[i]
            elif function[i][poly] != 0:
                desc += "%s^%s " % (varnames[i], function[i][poly])
        for i in xrange(len(function)):
            if function[i][polylog] == 1:
                desc += "log %s " % varnames[i]
            elif function[i][polylog] != 0:
                desc += "log^%s %s " % (function[i][polylog], varnames[i])
        desc = desc.strip() + ")"
    info = getcoeff(function, data)
    return "%s with coefficient %f and error %f" % (desc, info[0], info[2])
