import pandas as pd

info_vin = pd.read_csv('dataset/winemag-data-130k-v2.csv', index_col=0)
median_price = info_vin.price.median()
list_country = info_vin.country.unique()
count_country = info_vin.country.value_counts()
ecart_prix_median = info_vin.price - median_price

# min_price_vin = info_vin.loc[info_vin.price == info_vin.price.min()]
# best_wine_1 = min_price_vin.sort_values('points', ascending=False).iloc[0]

info_vin['score_by_price'] = info_vin.price * info_vin.points
best_wine = info_vin.sort_values('score_by_price', ascending=True).iloc[0]


def map_type(v):
    if 'tropical' in v:
        return 'tropical'
    elif 'fruity' in v:
        return 'fruity'


info_vin['type'] = info_vin.description.map(map_type)
tropical = info_vin.type.loc[info_vin.type == 'tropical']
fruity = info_vin.type.loc[info_vin.type == 'fruity']
counter = pd.Series([tropical.count(), fruity.count()])


def star_value(v):
    if v <= 85:
        return 1
    elif v <= 90:
        return 2
    elif v <= 95:
        return 3
    else:
        return 4


info_vin['star'] = info_vin.points.map(star_value)
