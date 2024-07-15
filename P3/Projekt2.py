from scipy.integrate import nquad
import pandas as pd
import numpy as np


def integrate3d(function, xlim, ylim, n):
    x_range = np.linspace(start=min(xlim), stop=max(xlim), num=n)
    y_range = np.linspace(start=min(ylim), stop=max(ylim), num=n)
    df = pd.DataFrame(columns=x_range)
    df['y'] = y_range
    df.set_index('y')
    area = (max(xlim)-min(xlim))*(max(ylim)-min(ylim))
    fsum = 0
    for x in x_range:
        for y in y_range:
            fsum += function(x, y)

    return area*fsum


def integrate3d2(function, xlim, ylim, n):
    x_range = np.linspace(start=min(xlim), stop=max(xlim), num=n)
    y_range = np.linspace(start=min(ylim), stop=max(ylim), num=n)
    df = pd.DataFrame(columns=x_range)
    df['y'] = y_range
    df.set_index('y')
    area = (max(xlim)-min(xlim))*(max(ylim)-min(ylim))/n**2
    for x in x_range:
        df[x] = pd.Series(y_range).apply(lambda row: function(x, row))

    return area*df.sum().sum()


def function(x, y):
    return np.cos(x*y)


xlim = [0, 1]
ylim = [0, 1]
n = 10000
integral = integrate3d2(function, xlim, ylim, n)
print('calculated=', integral)

check = nquad(function, [xlim, ylim])
print('real=', check[0])
