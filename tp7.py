import matplotlib.pyplot as plt
import pandas as pd

info_vin = pd.read_csv('dataset/winemag-data-130k-v2.csv')

info_vin = info_vin[(info_vin.points.notnull() & info_vin.price.notnull())]
tmp = info_vin.country.map(lambda l: str(l).lower().startswith('i'))
print(info_vin[tmp].shape)

vin_i = info_vin[tmp]
plt.hist(vin_i.country)
plt.yscale('log')

vin_i.plot.scatter(x='country', y='price')
group = vin_i.groupby(by='country').price.agg([min, max])
plt.plot(group)

plt.savefig('save/exemple.png', fomat='png')
plt.show()
