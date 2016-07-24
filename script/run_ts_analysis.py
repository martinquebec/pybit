import bitcoinchart.bitcoinchart as histo
import pandas as pd
import datetime as dt
import numpy as np
import bitcoinchart.market_model as market_model

from matplotlib import pyplot as plt




left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.3   # 0.2the amount of width reserved for blank space between subplots
hspace = 0.6   # 0.5the amount of height reserved for white space between subplots


def get_intraday_curves(min):
    volume = min.pivot_table(index='minute', columns='day', values='qty')
    volume = volume.fillna(0)
    volume_pct = volume / volume.sum()
    volume_curve = volume_pct.median(axis=1)
    volume_curve = volume_curve / volume_curve.sum()
    return volume_curve

def get_daily_curves(minutely_df):
    daily_volume = minutely_df[['day', 'qty']].groupby('day').sum()
    daily_volume['weekday'] = daily_volume.index.weekday
    weekday_volume = daily_volume.groupby('weekday').mean()
    weekday_adj = (weekday_volume / weekday_volume.loc[0, 'qty']).to_dict().get('qty')
#   weekday_volume['weeekday_adj']=[ weekday_adj.get(x) for x in daily_volume.weekday ]
    daily_volume['weeekday_adj'] = [weekday_adj.get(x) for x in daily_volume.weekday]
    daily_volume['qty_adj'] = daily_volume.qty / daily_volume.weeekday_adj
    daily_volume['log_adj'] = np.log(daily_volume.qty_adj)
    daily_volume['adv_log_adj'] = daily_volume.log_adj.ewm(halflife=10).mean()

markets = ['bitfinexUSD']

market = markets[0]
#for market in markets:
df = histo.get_df_histo(market)
    #   df should look like:
    #          date   price        qty
    #  0  1364767668   93.25  12.671482
    #  1  1364767669   93.30  80.628518

    # converting the date in datetime, filtering and setting data as index
#df['date'] = pd.to_datetime(df['date'],unit='s')
#start = dt.datetime(2015,1,1)
#df = df.loc[df['date'] > start]
#df.index = df['date']
#del df['date']

# minutly bucketing, adding minute, day and weekday columns
minutely_df = df.resample('1min', how ={'price': np.mean, 'qty': np.sum})
minutely_df['minute'] = minutely_df.index.hour * 60 + minutely_df.index.minute
minutely_df['weekday'] = minutely_df.index.weekday
minutely_df['day'] = pd.to_datetime(minutely_df.index.year * 10000 + minutely_df.index.month * 100 + minutely_df.index.day, format="%Y%m%d")
#   minutely_df now looks like that:
#                        price        qty  minute  weekday        day
#   date
#   2015-01-01 00:00:00  322.253333  62.098597       0        3 2015-01-01
#   2015-01-01 00:01:00  321.800000   5.929470       1        3 2015-01-01


daily_volume = minutely_df[['day','qty']].groupby('day').sum()
daily_volume['weekday'] = daily_volume.index.weekday
weekday_volume = daily_volume.groupby('weekday').mean()
weekday_adj  = (weekday_volume / weekday_volume.loc[0,'qty']).to_dict().get('qty')
#   weekday_volume['weeekday_adj']=[ weekday_adj.get(x) for x in daily_volume.weekday ]
daily_volume['weeekday_adj']=[ weekday_adj.get(x) for x in daily_volume.weekday]
daily_volume['log_adj'] = np.log(daily_volume.qty / daily_volume.weeekday_adj)

daily_volume['adv_log_adj'] = daily_volume.log_adj.ewm(halflife=10).mean().shift(1)
daily_volume['predicted_qty'] = np.exp(daily_volume.adv_log_adj) * daily_volume.weeekday_adj
pred_qty = daily_volume.predicted_qty.iloc[-1]


#                   qty  weekday  weeekday_adj       qty_adj
#day
#2015-01-01   5177.991896        3      1.050329   5438.596399
#2015-01-02   3834.544008        4      1.039678   3986.692428
#2015-01-03  47380.812581        5      0.851738  40356.037254

weekday_intraday_curves = pd.DataFrame({"all" : get_intraday_curves(minutely_df)})

#ax = plt.subplot(421)
#ax.set_title('all')
#ax.plot(weekday_intraday_curves)

for day in range(7):
    weekday_intraday_curves[str(day)] = get_intraday_curves(minutely_df.loc[minutely_df['weekday'] == day])
#    ax = plt.subplot(422+day)
#    ax.set_title(str(day))
#    ax.plot(weekday_intraday_curves[str(day)])
#    def __init__(self, name, weekday_adj,predicted_volume,weekday_intraday_curves):
mm = market_model.MarketAnalytics(market, weekday_adj, pred_qty, weekday_intraday_curves)
#mm.save(market)
print 'done'
        #plt.savefig(histo.local_histo_archive + market + ".weedday_curves_figure.pdf")
    #weekday_curves.to_csv(histo.local_histo_archive + market + ".weekday_curve.csv")

