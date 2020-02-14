import pandas as pd

info_vin = pd.read_csv('dataset/winemag-data-130k-v2.csv', index_col=0)

testers = info_vin.groupby('taster_twitter_handle').taster_name.count().sort_values(ascending=False)

points_price = info_vin.groupby('price').points.max()

variety_price = info_vin.groupby('variety').price.agg([min, max])

variety_price_sort = variety_price.sort_values(['min', 'max'], ascending=False)

testers_points_mean = info_vin.groupby('taster_name').points.mean()

counter_country_variety = info_vin.groupby(['country', 'variety']).description.count().sort_values(ascending=False)

title_price = info_vin.groupby('price').apply(lambda l: l.loc[l.points.idxmax()]).title
