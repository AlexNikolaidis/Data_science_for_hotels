import numpy as np
import io
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

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
    print('0 -> Exit script\n1 -> [ALOS] Average Length Of Stay (per month)\n'
          '2 -> [ALOS] Average Length Of Stay (per week)\n'
          '3 -> Cancellation rate (per month)\n4 -> Cancellation rate (per week)\n'
          '5 -> [ADR] Average Daily Rate (per month)\n6 -> [ADR] Average Daily Rate (per week)\n'
          '7 -> Bookings (per month)\n8 -> Bookings (per week)\n'
          '9 -> [DEN EXEI YLOPOIHTHEI] Bookings per customer type (per month)\n10 -> [DEN EXEI YLOPOIHTHEI] Bookings per customer type  (per week)\n'
          '11 -> test')
    text = int(input("Choose metric: "))
    if text == 0:
        break
    elif text == 1 or text == 2:
        if text == 1:
            temp = 'arrival_date_month'
        elif text == 2:
            temp = 'arrival_date_week_number'

        if year == 2015:
            months_short = months_short_og[6:]
            months = months_og[6:]
            weeks = weeks_og[6:]
        elif year == 2016:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og
        elif year == 2017:
            months_short = months_short_og[:7]
            months = months_og[:7]
            weeks = weeks_og[:7]
        else:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og

        result = metric.groupby(temp)[['stays_in_weekend_nights', 'stays_in_week_nights']].mean()
        if text == 1:
            result = result.reindex(months)

        if text == 1:
            x = np.arange(len(months_short))
        elif text == 2:
            x = np.arange(len(weeks))

        fig, ax = plt.subplots()

        width = 0.8
        ax.bar(x, result['stays_in_week_nights'], width, label='average length of stay (week nights)')
        ax.bar(x, result['stays_in_weekend_nights'], width, label='average length of stay (weekend nights)',
               bottom=result['stays_in_week_nights'])
        # rects1 = ax.bar(x - width / 2, result['stays_in_weekend_nights'], width, label='average weekend nights stayed')
        # rects2 = ax.bar(x + width / 2, result['stays_in_week_nights'], width, label='average week nights stayed')
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
        if text == 3:
            temp = 'arrival_date_month'
        elif text == 4:
            temp = 'arrival_date_week_number'

        if year == 2015:
            months_short = months_short_og[6:]
            months = months_og[6:]
            weeks = weeks_og[6:]
        elif year == 2016:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og
        elif year == 2017:
            months_short = months_short_og[:7]
            months = months_og[:7]
            weeks = weeks_og[:7]
        else:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og

        result_cancel = metric.groupby(temp)[['is_canceled']].sum()
        result_total = metric.groupby(temp)[['lead_time']].count()
        # print(result_cancel.loc['January'])
        if text == 3:
            cancellation_rate = [0] * len(months_short)
            for i, z in enumerate(months):
                cancellation_rate[i] = 100 * (result_cancel.loc[z].iat[0] / result_total.loc[z].iat[0])
        elif text == 4:
            cancellation_rate = [0] * len(weeks)
            for i, z in enumerate(weeks):
                cancellation_rate[i] = 100 * (result_cancel.loc[z].iat[0] / result_total.loc[z].iat[0])



        if text == 3:
            x = np.arange(len(months_short))
        elif text == 4:
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

        if text == 5:
            temp = 'arrival_date_month'
        elif text == 6:
            temp = 'arrival_date_week_number'

        if year == 2015:
            months_short = months_short_og[6:]
            months = months_og[6:]
            weeks = weeks_og[6:]
        elif year == 2016:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og
        elif year == 2017:
            months_short = months_short_og[:7]
            months = months_og[:7]
            weeks = weeks_og[:7]
        else:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og

        result = metric.groupby(temp)[['adr']].mean()  # ypologismos adr me ton mina / vdomada
        if text == 5:
            result = result.reindex(months)
        # print(result)

        if text == 5:
            x = np.arange(len(months_short))
        elif text == 6:
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
        if text == 7:
            temp = 'arrival_date_month'
        elif text == 8:
            temp = 'arrival_date_week_number'

        if year == 2015:
            months_short = months_short_og[6:]
            months = months_og[6:]
            weeks = weeks_og[6:]
        elif year == 2016:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og
        elif year == 2017:
            months_short = months_short_og[:7]
            months = months_og[:7]
            weeks = weeks_og[:7]
        else:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og

        result = metric.groupby(temp)[['lead_time']].count()
        if text == 7:
            result = result.reindex(months)

        if text == 7:
            booking_count = [0] * len(months_short)
            for i, z in enumerate(months):
                booking_count[i] = result.loc[z].iat[0]
        elif text == 8:
            booking_count = [0] * len(weeks)
            for i, z in enumerate(weeks):
                booking_count[i] = result.loc[z].iat[0]




        if text == 7:
            x = np.arange(len(months_short))
        elif text == 8:
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
        if text == 9:
            temp = 'arrival_date_month'
        elif text == 10:
            temp = 'arrival_date_week_number'

        if year == 2015:
            months_short = months_short_og[6:]
            months = months_og[6:]
            weeks = weeks_og[6:]
        elif year == 2016:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og
        elif year == 2017:
            months_short = months_short_og[:7]
            months = months_og[:7]
            weeks = weeks_og[:7]
        else:
            months_short = months_short_og
            months = months_og
            weeks = weeks_og

        if text == 9:
            # booking_count = [0] * len(months_short)
            booking_count = np.array([[0]*4]*len(months_short))
            for i, z in enumerate(months):
                result = metric[metric[temp] == z]
                booking_count[i] = result.groupby(['customer_type'])['hotel'].count()
        elif text == 10:
            # booking_count = [0] * len(weeks)
            booking_count = np.array([[0] * 4] * len(weeks))
            for i, z in enumerate(weeks):
                result = metric[metric[temp] == z]
                booking_count[i] = result.groupby(['customer_type'])['hotel'].count()

        print(booking_count)

        fig, ax = plt.subplots()
        ax.pie(booking_count[0], radius=3, center=(4, 4),
                wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
        plt.show()
        # if text == 9:
        #     x = np.arange(len(months_short))
        # elif text == 10:
        #     x = np.arange(len(weeks))
        #
        # width = 0.8
        # fig, ax = plt.subplots()
        # rects1 = ax.bar(x - width / 2, booking_count['stays_in_weekend_nights'], width, label='average weekend nights stayed')
        # rects2 = ax.bar(x + width / 2, booking_count['stays_in_week_nights'], width, label='average week nights stayed')
        # plt.xlabel(temp)
        # plt.ylabel('Count')
        # ax.legend()
        # if text == 9:
        #     ax.set_xticks(x, months_short)
        #     if year != 0:
        #         ax.set_title(hotel + ': Bookings per customer type per month [' + str(year) + ']')
        #     else:
        #         ax.set_title(hotel + ': Bookings per customer type per month [All years]')
        # elif text == 10:
        #     ax.set_xticks(x, weeks)
        #     if year != 0:
        #         ax.set_title(hotel + ': Bookings per customer type per week [' + str(year) + ']')
        #     else:
        #         ax.set_title(hotel + ': Bookings per customer type per week [All years]')
        # plt.show()

    elif text == 11:

        # gia to 2016 pigaino kathe mera kai metrao posa domatia typou A eixan kleistei

        # result_july = metric[metric['arrival_date_month'] == 'July']
        result_august = metric[metric['arrival_date_month'] == 'August']

        # result1j = result_july[result_july['arrival_date_day_of_month'] == 1]
        minoulides = np.linspace(1, 31, 31)
        minoulides = minoulides.astype('int32')
        rooms_august = [0]*31

        print(minoulides)

        for i in minoulides:
            result1a = result_august[result_august['arrival_date_day_of_month'] == i]
            rooms_august[i-1] = result1a[result_august['assigned_room_type'] == 'A']['lead_time'].count()

        # arrival_date_day_of_month

        # rooms_july = result1j.groupby('assigned_room_type').count()

        print(rooms_august)

        x = np.arange(31)

        fig, ax = plt.subplots()

        width = 0.8
        ax.bar(x, rooms_august, width, label='ADR')
        plt.show()
