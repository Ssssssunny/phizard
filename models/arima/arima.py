#!/usr/bin/env python
# encoding: utf-8
#
# To fit a time-series data with arima model and report any anomaly
#
# author: Umbriel
# date: 2017-06-24
#

import numpy as np
import statsmodels.api as sm
import statsmodels.tsa as st
from scipy.stats import t
#import matplotlib.pyplot as plt

from phizard.models.statistics import grubbs_test


class Arima():
    def __init__(self):
        pass

    def get_residue(self, series, max_arparam=4, max_maparam=2):
        """
        First fit the series using an arima model and return the residue
        """
        series = np.array(series)
        # print series
        # series = st.tsatools.detrend(series)
        # series = st.seasonal.seasonal_decompose(series, freq=7).resid
        res = sm.tsa.arma_order_select_ic(series, max_arparam, max_maparam,\
            ic=['aic'], trend='nc') 
        arparam, maparam = res.aic_min_order
        try:
            model = sm.tsa.ARIMA(series, order=(arparam, 1, maparam))
            res = model.fit(trend='c', display=-1)
        except Exception, e:
            model = sm.tsa.ARIMA(series, order=(arparam, 1, 0))  # handle the non-invertible situation
            res = model.fit(trend='c', display=-1)
        return res.resid


if __name__ == '__main__':
    arima = Arima()
    series = [1.0]*200
    series[10] = 20.0
    resid = arima.get_residue(series)
    print grubbs_test(resid, 0.01)
