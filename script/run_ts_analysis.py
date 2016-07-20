import bitcoinchart.histo as histo
import pandas as pd
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt




left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.3   # 0.2the amount of width reserved for blank space between subplots
hspace = 0.6   # 0.5the amount of height reserved for white space between subplots


def get_volume_curves(min):
    volume = min.pivot_table(index='minute', columns='day', values='qty')
    volume = volume.fillna(0)
    volume_pct = volume / volume.sum()
    volume_curve = volume_pct.median(axis=1)
    volume_curve = volume_curve / volume_curve.sum()
    return volume_curve


markets = ['bitfinexUSD']

for market in markets:
    df = histo.get_df_histo('bitfinexUSD')
    #   df should look like:
    #          date   price        qty
    #  0  1364767668   93.25  12.671482
    #  1  1364767669   93.30  80.628518

    # converting the date in datetime, filtering and setting data as index
    df['date'] = pd.to_datetime(df['date'],unit='s')
    start = dt.datetime(2015,1,1)
    df = df.loc[df['date'] > start]
    df.index = df['date']
    del df['date']

    # minutly bucketing, adding minute, day and weekday columns
    min = df.resample('1min', how ={'price': np.mean, 'qty': np.sum})
    min['minute'] = min.index.hour * 60 + min.index.minute
    min['weekday'] = min.index.weekday
    min['day'] = pd.to_datetime(min.index.year * 10000 + min.index.month * 100 + min.index.day,format="%Y%m%d")

    daily_volume = min.groupby('day')['qty'].sum()
    log_daily_volume = np.log(daily_volume)

   # weekday_vol = min.pivot_table(index='minute', columns='weekday', values='qty',aggfunc=np.sum)
   # weekday_vol = weekday_vol.fillna(0)
    #week day vol should look like:
    #   weekday
    #   minute      0           1           2           ...
    #   0           1473.24     1641.79     6362.96     ...
    #   1           1898.03     1268.54     5457.49     ...


    plt.close()
    plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

    weekday_curves = pd.DataFrame({ "all" : get_volume_curves(min)})

    ax = plt.subplot(421)
    ax.set_title('all')
    ax.plot(weekday_curves)

    for day in range(7):
        weekday_curves[str(day)] = get_volume_curves(min.loc[min['weekday'] == day])
        ax = plt.subplot(422+day)
        ax.set_title(str(day))
        ax.plot(weekday_curves[str(day)])

    #plt.savefig(histo.local_histo_archive + market + ".weedday_curves_figure.pdf")
    #weekday_curves.to_csv(histo.local_histo_archive + market + ".weekday_curve.csv")

