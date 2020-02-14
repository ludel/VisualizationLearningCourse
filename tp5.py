import pandas as pd

info_vin = pd.read_csv('dataset/winemag-data-130k-v2.csv', index_col=0)

type_point = info_vin.points.dtype

chain_point = info_vin.points.astype('str')

n_price_nan = pd.isnull(info_vin.price)

region_2_missing = info_vin.region_2.fillna('Unknown').value_counts()
