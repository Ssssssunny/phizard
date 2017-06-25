##INTRODUCTION##

Phizard is a Microsoft Graph API-based service for employee-status-management. It captures time series of employee's expressions in certain time intervals. After obtaining each image, the Microsoft Graph API is utilized to obtain the emotion revealed by such picture. An analysis of each employee's emotion time-series is performed by two models:

1. An LSTM model as usually used for sequential data
2. An ARIMA model for time-series ananlysis

Based on the results from these two analysis, an anomaly detection is performed using Grubbs' Test.

##HOW TO USE IT##
Firstly, on the local machine, run /cam/cam.py as:
    
    python cam.py

, which takes images and calls the Microsoft Graph API to get emotions.

Then start the web service from /web, which provides a dashboard for data monitoring and visualization.

