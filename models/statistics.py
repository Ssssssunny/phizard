#!/usr/bin/env python
# encoding: utf-8
#
# collections of statistics 
#
# author: Umbriel
# date: 2017-06-24
#

import numpy as np
import statsmodels.api as sm
from scipy.stats import t
import math

def grubbs_test(series, alpha=0.025):
    """
    Finds the anomaly using Grubbs' test
    """
    outliers = []
    series = np.array(series)
    vals = series
    start = 0
    end = len(vals) - 1

    while True:
        # find the Grubbs' test statistic
        y_ = np.nanmean(vals)
        s = np.nanstd(vals)
        n = len(vals) 
        g = 0
        z_stat = [abs(y - y_)/s for y in vals]
        g = max(z_stat)
        ind = np.argmax(z_stat)
        t2_alpha = math.pow(t.ppf(alpha/(2*n), n-2), 2)
        critical = (n-1)*math.sqrt(t2_alpha/(n - 2 + t2_alpha))/math.sqrt(n)
        if g > critical:
            outliers.append([ind, series[ind], g, critical])
        else:
            break
        # remove the outlier by setting its value to the new mean and iterate
        vals[ind] = (y_*n - vals[ind])/(n-1)

    return outliers

if __name__ == '__main__':
    series = [1]*100
    series[10] = 20
    print grubbs_test(series)