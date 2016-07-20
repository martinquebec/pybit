import bitcoinchart.histo as histo
import pandas as pd
import datetime as dt
import numpy as np


df = histo.get_df_histo('bitfinexUSD')
df['date'] = pd.to_datetime(df['date'],unit='s')
start = dt.datetime(2015,1,1)
df = df.loc[df['date'] > start]
df.index = df['date']
del df['date']

min = df.resample('1min', how ={'price': np.mean, 'qty': np.sum})
min['minute'] = min.index.hour * 60 + min.index.minute
min['day'] =pd.to_datetime(min.index.year * 10000 + min.index.month * 100 + min.index.day,format='%Y%m%d')
volume = min.pivot(index='minute', columns='day', values='qty')
volume = volume.fillna(0)
volume_pct = volume / volume.sum()
volume_curve = volume_pct.mean(axis=1)
volume_curve.plot()