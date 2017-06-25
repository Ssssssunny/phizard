#!/usr/bin/env python
# encoding: utf-8

from phizard.models.arima.arima import Arima
from phizard.models.rnn.lstm import get_result
from phizard.models.rnn.lstm import STEP_LENGTH
from phizard.models.statistics import grubbs_test

def analyze(series, methods=['arima', 'lstm']):
    res = dict()
    # process data with arima model
    if 'arima' in methods:
        res['arima-graph'] = dict()
        res['arima-anomaly'] = dict()
        for k, v in series.items():
            arima = Arima()
            resid = arima.get_residue(v)
            anomaly = grubbs_test(resid, 0.01)
            res['arima-graph'][k] = list(resid)
            res['arima-anomaly'][k] = anomaly
    # process data with lstm model
    if 'lstm' in methods:
        res['lstm-graph'] = dict()
        res['lstm-anomaly'] = dict()
        for k, v in series.items():
            if len(v) > STEP_LENGTH:
                resid = get_result(v)
                anomaly = grubbs_test(resid, 0.01)
                for v in anomaly:
                    v[0] = v[0] + STEP_LENGTH
                res['lstm-graph'][k] = list(resid)
                res['lstm-anomaly'][k] = anomaly
            else:
                res['lstm-graph'][k] = None
                res['lstm-anomaly'][k] = None
    return res


if __name__ == '__main__':
    series1 = [0.49415735, 0.96479118, 0.6331718,  0.36432513, 0.58211649, 0.38080849,
           0.04657582, 0.48392074, 0.97764447, 0.65642632, 0.38863295, 0.62258502,
           0.35661317, 0.04377478, 0.52113207, 0.92915645, 0.64454011, 0.4599896,
           0.56170511, 0.34391158, 0.03752787, 0.47545123, 1.,         0.64043056,
           0.41360918, 0.58401346, 0.3532402,  0.09373201, 0.53521677, 0.90090211,
           0.61883604, 0.33472595, 0.57695819, 0.34490574, 0.03011273, 0.51494765,
           0.44489105, 0.86924711, 0.78922552, 0.62666652, 0.39975941, 0.03954748,
           0.49510621, 0.95926067, 0.60582642, 0.43714943, 0.60597288, 0.3396475,
           0.08410692, 0.54786727, 0.93095072, 0.6350027,  0.39361595, 0.60053582,
           0.34233749, 0.,         0.51494765, 0.6969983,  0.75704882, 0.5870512,
           0.62475035, 0.39802208, 0.06823464, 0.52510975, 0.97283277, 0.57889955,
           0.39572957, 0.62377444, 0.36187407, 0.05441733]
    
    series = dict(ser1=series1)
    res = analyze(series)
    print 'lstm-'*20
    print res['lstm-graph']
    print res['lstm-anomaly']
    print 'arima-'*20
    print res['arima-graph']
    print res['arima-anomaly']
