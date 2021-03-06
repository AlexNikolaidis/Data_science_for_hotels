import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import preprocessing

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
        months_short = months_short_og[6:]
        months = months_og[6:]
        weeks = weeks_og[26:]
    elif text == 2:
        year = 2016
        metric = metric1[metric1['arrival_date_year'] == year]
        months_short = months_short_og
        months = months_og
        weeks = weeks_og
    elif text == 3:
        year = 2017
        metric = metric1[metric1['arrival_date_year'] == year]
        months_short = months_short_og[:7]
        months = months_og[:7]
        weeks = weeks_og[:35]
    elif text == 4:
        metric = metric1
        months_short = months_short_og
        months = months_og
        weeks = weeks_og
    else:
        continue

    print('0 -> Exit script\n1 -> [ALOS] Average Length Of Stay (per month)\n'
          '2 -> [ALOS] Average Length Of Stay (per week)\n'
          '3 -> Cancellation rate (per month)\n4 -> Cancellation rate (per week)\n'
          '5 -> [ADR] Average Daily Rate (per month)\n6 -> [ADR] Average Daily Rate (per week)\n'
          '7 -> Bookings (per month)\n8 -> Bookings (per week)\n'
          '9 -> [Cancellation Prediction] K-Nearest Neighbor\n10 -> [Cancellation Prediction] Decision tree')
    text = int(input("Choose metric: "))

    if text%2:
        temp = 'arrival_date_month'
    else:
        temp = 'arrival_date_week_number'

    if text == 0:
        break
    elif text == 1 or text == 2:

        result = metric.groupby(temp)[['stays_in_weekend_nights', 'stays_in_week_nights']].mean()
        print(len(result['stays_in_week_nights']))
        if text == 1:
            result = result.reindex(months)
            x = np.arange(len(months_short))

        if text == 2:
            x = np.arange(len(weeks))

        fig, ax = plt.subplots()

        width = 0.8
        ax.bar(x, result['stays_in_week_nights'], width, label='average length of stay (week nights)')
        ax.bar(x, result['stays_in_weekend_nights'], width, label='average length of stay (weekend nights)',
               bottom=result['stays_in_week_nights'])
        plt.xlabel(temp)
        plt.ylabel('Length of stay')
        ax.legend()

        if text == 1:
            ax.set_xticks(x, months_short)
            if year != 0:
                ax.set_title(hotel + ': Average length of stay per month [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': Average length of stay per month [All years]')
        elif text == 2:
            ax.set_xticks(x, weeks)
            if year != 0:
                ax.set_title(hotel + ': Average length of stay per month [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': Average length of stay per month [All years]')
        plt.show()

    elif text == 3 or text == 4:

        result_cancel = metric.groupby(temp)[['is_canceled']].sum()
        result_total = metric.groupby(temp)[['lead_time']].count()
        # print(result_cancel.loc['January'])
        if text == 3:
            cancellation_rate = [0] * len(months_short)
            for i, z in enumerate(months):
                cancellation_rate[i] = 100 * (result_cancel.loc[z].iat[0] / result_total.loc[z].iat[0])
            x = np.arange(len(months_short))
        elif text == 4:
            cancellation_rate = [0] * len(weeks)
            for i, z in enumerate(weeks):
                cancellation_rate[i] = 100 * (result_cancel.loc[z].iat[0] / result_total.loc[z].iat[0])
            x = np.arange(len(weeks))

        width = 0.8
        fig, ax = plt.subplots()
        ax.bar(x, cancellation_rate, width, label='Cancellation rate')
        plt.xlabel(temp)
        plt.ylabel('Cancellation %')
        ax.legend()
        if text == 3:
            ax.set_xticks(x, months_short)
            if year != 0:
                ax.set_title(hotel + ': Cancellation rate per month [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': Cancellation rate per month [All years]')
        elif text == 4:
            ax.set_xticks(x, weeks)
            if year != 0:
                ax.set_title(hotel + ': Cancellation rate per month [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': Cancellation rate per month [All years]')
        plt.show()

    elif text == 5 or text == 6:

        result = metric.groupby(temp)[['adr']].mean()  # ypologismos adr me ton mina / vdomada
        if text == 5:
            result = result.reindex(months)
            x = np.arange(len(months_short))

        if text == 6:
            x = np.arange(len(weeks))

        fig, ax = plt.subplots()

        width = 0.8
        ax.bar(x, result['adr'], width, label='ADR')
        plt.xlabel(temp)
        plt.ylabel('Currency')
        ax.legend()

        if text == 5:
            ax.set_xticks(x, months_short)
            if year != 0:
                ax.set_title(hotel + ': ADR [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': ADR [All years]')
        elif text == 6:
            ax.set_xticks(x, weeks)
            if year != 0:
                ax.set_title(hotel + ': ADR [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': ADR [All years]')
        plt.show()

    elif text == 7 or text == 8:

        result = metric.groupby(temp)[['lead_time']].count()

        if text == 7:
            result = result.reindex(months)
            booking_count = [0] * len(months_short)
            for i, z in enumerate(months):
                booking_count[i] = result.loc[z].iat[0]
            x = np.arange(len(months_short))
        elif text == 8:
            booking_count = [0] * len(weeks)
            for i, z in enumerate(weeks):
                booking_count[i] = result.loc[z].iat[0]
            x = np.arange(len(weeks))

        width = 0.8
        fig, ax = plt.subplots()
        ax.bar(x, booking_count, width, label='Bookings')
        plt.xlabel(temp)
        plt.ylabel('Count')
        ax.legend()
        if text == 7:
            ax.set_xticks(x, months_short)
            if year != 0:
                ax.set_title(hotel + ': Bookings per month [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': Bookings per month [All years]')
        elif text == 8:
            ax.set_xticks(x, weeks)
            if year != 0:
                ax.set_title(hotel + ': Bookings per week [' + str(year) + ']')
            else:
                ax.set_title(hotel + ': Bookings per week [All years]')
        plt.show()

    elif text == 9 or text == 10:
        categorical = ['country', 'customer_type', 'market_segment', 'distribution_channel',
                       'reserved_room_type', 'assigned_room_type']

        for temp in categorical:
            metric.loc[:, temp] = metric.loc[:, temp].astype('category')
            metric.loc[:, temp] = metric.loc[:, temp].cat.codes

        X = metric[['arrival_date_week_number', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults',
                    'children', 'adr', 'country', 'customer_type', 'market_segment', 'distribution_channel',
                    'reserved_room_type', 'assigned_room_type']].values  # .astype(float)
        y = metric['is_canceled'].values

        if text == 9:

            # After tests the max accuracy of ~0.8135 can be achieved with a k value of 4
            X = preprocessing.StandardScaler().fit(X).transform(X.astype(float))

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=4)

            k = 4
            # Train Model and Predict
            neigh = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)
            yhat = neigh.predict(X_test)
            train_accuracy = metrics.accuracy_score(y_train, neigh.predict(X_train))
            test_accuracy = metrics.accuracy_score(y_test, yhat)
            print("For booking cancellation prediction:")
            print("Train set Accuracy [k = " + str(k) + "]: ", train_accuracy)
            print("Test set Accuracy: [k = " + str(k) + "]: ", test_accuracy)

        elif text == 10:

            # After tests the max accuracy of ~0.8193 can be achieved with a max depth of 11
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=4)
            cancel_tree = DecisionTreeClassifier(criterion="entropy", max_depth=11)

            cancel_tree.fit(X_train, y_train)
            pred_tree = cancel_tree.predict(X_test)

            print(pred_tree[0:25])
            print(y_test[0:25])
            print("DecisionTrees's Accuracy: ", metrics.accuracy_score(y_test, pred_tree))

    else:
        continue