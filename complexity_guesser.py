#!/usr/bin/env python2

import math
import random
import operator

def poly(val, deg):
    return val**deg

def polylog(val, deg):
    return math.log(1+val)**deg

def mean(l):
    return sum(l)/len(l)

def gmean(l):
    return reduce(operator.mul, l, 1)**(1./len(l))

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
    dims = [getdim(i[0], function) for i in data if i[1] > 0]
    times = [i[1] for i in data if i[1] > 0]
    idx = xrange(len(times))
    b = 0
    a = mean([dims[i]/times[i] for i in idx]) / \
        mean([(dims[i]/times[i])**2 for i in idx])
    err = mean([(a*dims[i]/times[i]-1)**2 for i in idx])
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
    nit = 10000
    def tfun(t):
        return (float(nit-t)/nit)**3
    for t in xrange(nit):
        temp = tfun(t) * 0.0001
        err = getcoeff(function, data)[2]
        step = []
        for i in varnames:
            a = random.uniform(-1, 1) * tfun(t)
            b = random.uniform(-1, 1) * tfun(t)
            step.append([a, b])
        for i in xrange(len(varnames)):
            function[i][poly] += step[i][0]
            function[i][polylog] += step[i][1]
        errn = getcoeff(function, data)[2]
        if -(errn - err)/temp < math.log(random.random()):
            for i in xrange(len(varnames)):
                function[i][poly] -= step[i][0]
                function[i][polylog] -= step[i][1]
    info = getcoeff(function, data)
    for i in xrange(len(varnames)):
        function[i][poly] = round(function[i][poly]*10)/10
        function[i][polylog] = round(function[i][polylog]*10)/10
    if sum(fn != {poly: 0, polylog: 0} for fn in function) == 0:
        desc = "O(1)"
    else:
        desc = "O("
        for i in xrange(len(function)):
            if function[i][poly] == 1:
                desc += "%s " % varnames[i]
            elif function[i][poly] != 0:
                desc += "%s^%.1f " % (varnames[i], function[i][poly])
        for i in xrange(len(function)):
            if function[i][polylog] == 1:
                desc += "log %s " % varnames[i]
            elif function[i][polylog] != 0:
                desc += "log^%.1f %s " % (function[i][polylog], varnames[i])
        desc = desc.strip() + ")"
    return "%s with coefficient %f and error %s" % (desc, info[0], info[2])
