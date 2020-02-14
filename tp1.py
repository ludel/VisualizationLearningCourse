import pandas as pd

fruit_1 = pd.Series([21, 34])
fruit_2 = pd.Series([35, 41])
fruits_sales = pd.DataFrame({'Bananes': fruit_1, 'Pommes': fruit_2}, index=['Vente 2017', 'Vente 2018'])

ingredients = pd.Series(['400g'])

df = pd.read_csv(
    'dataset/winemag-data-130k-v2.csv',
    usecols=['description', 'designation', 'title', 'variety', 'winery'],
    nrows=50
)

df.to_csv('dataset/1_exercice_info_vin.csv')

