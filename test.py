import numpy as np
import io
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

data = pd.read_csv('hotel_booking.csv')
sns.set_style("darkgrid")
months_og = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
months_short_og = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
year = 0
weeks_og = np.linspace(1, 53, 53)
weeks_og = weeks_og.astype('int32')

while 1:
    print('0 -> Exit scipt\n1 -> Resort Hotel \n2 -> City Hotel')
    text = int(input("Choose hotel: "))
    if text == 0:
        break
    elif text == 1:
        metric1 = data[data['hotel'] == "Resort Hotel"]
        hotel = "Resort Hotel"
    elif text == 2:
        metric1 = data[data['hotel'] == "City Hotel"]
        hotel = "City Hotel"
    else:
        continue
    # print(metric)
    print('0 -> Exit scipt\n1 -> 2015\n2 -> 2016\n3 -> 2017\n4 -> All years')
    text = int(input("Choose year: "))
    if text == 1:
        year = 2015
        metric = metric1[metric1['arrival_date_year'] == year]
    elif text == 2:
        year = 2016
        metric = metric1[metric1['arrival_date_year'] == year]
    elif text == 3:
        year = 2017
        metric = metric1[metric1['arrival_date_year'] == year]
    elif text == 4:
        metric = metric1
    else:
        continue


    # transform categorical values column to numerical for use in prediction algorithm

    metric.loc[:, "country"] = metric.loc[:, "country"].astype('category')
    print(metric.dtypes)
    print(metric['country'])
    metric.loc[:, "country"] = metric.loc[:, "country"].cat.codes
    print(metric['country'])




