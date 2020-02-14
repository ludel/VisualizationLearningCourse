import pandas as pd

info_vin = pd.read_csv('dataset/winemag-data-130k-v2.csv', index_col=0)
desc = info_vin.description
line = info_vin.iloc[0]
prov = info_vin.loc[:10, 'province']
example = info_vin.iloc[[1, 2, 3, 5, 8]]
sous_ensemble = info_vin.loc[:100:10, ['country', 'province', 'region_1', 'region_2']]
variety = info_vin.loc[:100, ['country', 'variety']]
vin_hungary = info_vin.loc[(info_vin.country == 'Hungary') & (info_vin.price < 20)]
vin_oceanie_top = info_vin.loc[(info_vin.country.isin(['Australia', 'New Zealand'])) & (info_vin.points >= 95)]
