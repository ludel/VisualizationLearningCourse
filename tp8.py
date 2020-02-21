import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class Resume:
    def __init__(self):
        if not os.path.isdir('./image'):
            os.makedirs('./image')

        try:
            arg = sys.argv[1]
        except IndexError:
            self.output = None
        else:
            self.output = open(f'./{arg}', 'w')
            self.output.writelines('# Visualisation \n')
        self.df_car = self.clean_df()

    @staticmethod
    def clean_df():
        df = pd.read_csv('dataset/cars data.csv', index_col=0, sep=';')
        df.replace('*', np.nan, inplace=True)
        df['Weight'] = df['Weight'].astype(np.float)
        df['Len'] = df['Len'].astype(np.float)
        df['HP'] = df['HP'].astype(np.float)
        df['Width'] = df['HP'].astype(np.float)
        df['City MPG'] = df['City MPG'].astype(np.float)

        df['Retail Price'] = df['Retail Price'].astype(np.float)
        df['margin price'] = df['Retail Price'] - df['Dealer Cost']
        df['margin amount'] = df['margin price'] / df['Dealer Cost']
        df['surface'] = df['Len'] * df['Width']
        return df

    def write_image(self, title, path):
        plt.savefig(f'image/{path}.png', bbox_inches='tight', format='png')
        print(f'## {title}', f'![{path}](./image/{path}.png)', sep='\n', file=self.output)
        plt.clf()

    def run(self):
        self.sale()
        self.car_stats()
        self.group()
        self.weight()
        self.rate()
        self.compare()

    def sale(self):
        print('## Calcules des ventes', file=self.output)
        # Min, Mean, Max for retail price
        print('### Prix de vente',
              f"- minimun: {self.df_car['Retail Price'].min()}",
              f"- moyen: {self.df_car['Retail Price'].mean()}",
              f"- maximun: {self.df_car['Retail Price'].max()}",
              sep='\n', end='\n' * 2, file=self.output)

        # Min, Mean, Max for margin price
        print('### Marge',
              f"- minimun: {self.df_car['margin price'].min()}",
              f"- moyen: {self.df_car['margin price'].mean()}",
              f"- maximun: {self.df_car['margin price'].max()}",
              sep='\n', end='\n' * 2, file=self.output)

    def car_stats(self):
        # Most expensive, cheaper, profitable car
        print('## Prix des voitures', file=self.output)
        most_expensive = self.df_car.loc[self.df_car['Retail Price'].idxmax()]
        most_cheaper = self.df_car.loc[self.df_car['Retail Price'].idxmin()]
        most_profitable = self.df_car.loc[self.df_car['margin price'].idxmax()]
        print(f"- Voiture la plus chère: '{most_expensive.name}' (prix: {most_expensive['Retail Price']} $)",
              f"- Voiture la moins chère: '{most_cheaper.name}' (prix: {most_cheaper['Retail Price']} $)",
              f"- Voiture la plus rentable: '{most_profitable.name}' (marge: {most_profitable['margin price']} $)",
              '> On observe que la voiture la plus chère possède aussi la marge la plus élevé',
              sep='\n', end='\n' * 2, file=self.output)

        self.df_car.sort_values('Retail Price').head(10)['Retail Price'].plot.bar()
        plt.ylabel('Prix')
        plt.title('Top 10 des voitures les moins chères')
        self.write_image('Top 10 des voitures les moins chères', 'top_cheap')

        self.df_car.sort_values('Retail Price', ascending=False).head(10)['Retail Price'].plot.bar()
        plt.title('Top 10 des voitures les plus chère')
        plt.ylabel('Prix')
        self.write_image('Top 10 des voitures les plus chères', 'top_expensive')

    def group(self):
        groups = {'count': [], 'mean_price': [], 'len': [], 'MPG': [], 'weight': []}
        labels = ['Small/Sporty/ Compact/Large Sedan', 'Sports Car', 'SUV', 'Wagon', 'Minivan', 'Pickup']
        for label in labels:
            group = self.df_car.loc[self.df_car[label] == 1]
            groups['count'].append(group[label].count())
            groups['mean_price'].append(group['Retail Price'].mean())
            groups['len'].append(group['Len'].mean())
            groups['MPG'].append(group['City MPG'].mean())
            groups['weight'].append(group['Weight'].mean())

        plt.pie(groups['count'], labels=labels, startangle=90, autopct='%1.1f%%')
        plt.title('Répartition des véhicules par catégories')
        self.write_image('Répartition des véhicules par catégories', 'repartition')

        fig, axs = plt.subplots(2, 2)
        fig.set_size_inches(12, 4)
        plt.subplots_adjust(bottom=3, top=5)
        labels[0] = 'compact'

        axs[0, 0].bar(labels, groups['mean_price'])
        axs[0, 0].set_title('Moyenne des prix')

        axs[1, 0].bar(labels, groups['len'])
        axs[1, 0].set_title('Moyenne de la taille')

        axs[0, 1].bar(labels, groups['MPG'])
        axs[0, 1].set_title('Autonomie moyenne en ville')

        axs[1, 1].bar(labels, groups['weight'])
        axs[1, 1].set_title('Poids moyen')

        self.write_image('Catégorie de vehicules', 'category')

    def weight(self):
        # Weight function len
        self.df_car.dropna().plot.scatter(x='Weight', y='surface')
        plt.ylabel('Poids')
        plt.xlabel('Surface')

        x_test = self.df_car.dropna()['Weight'].to_numpy()
        y_test = self.df_car.dropna()['surface'].to_numpy()
        reg = LinearRegression().fit(x_test.reshape(x_test.size, 1), y_test.reshape(y_test.size, 1))
        y_prediction = reg.predict(x_test.reshape(y_test.size, 1))
        plt.plot(x_test, y_prediction, c='red')

        plt.savefig('image/weight_surface.png', format='png')

        self.write_image('Surface en fonction du poids', 'weight_surface')
        print("> La surface correspond à la longueur mutiplié à la largeur et "
              " la droite est un modèle de régression linéaire", end='\n',
              file=self.output)

        self.df_car.dropna().plot.scatter(x='Cyl', y='Weight')
        plt.ylabel('Poids')
        plt.xlabel('Cylindrée')
        x_test = self.df_car.dropna()['Cyl'].to_numpy()
        y_test = self.df_car.dropna()['Weight'].to_numpy()
        reg = LinearRegression().fit(x_test.reshape(x_test.size, 1), y_test.reshape(y_test.size, 1))
        y_prediction = reg.predict(x_test.reshape(y_test.size, 1))
        plt.plot(x_test, y_prediction, c='red')
        self.write_image('Poids en fonction de la cylindrée', 'cyl_weight')

    def rate(self):
        self.df_car['rate_weight_cyl'] = self.df_car['Weight'] / self.df_car['Cyl']
        self.df_car['tonne'] = self.df_car['Weight'] / 1000
        self.df_car.dropna().sort_values('rate_weight_cyl').head(10).plot(y=["tonne", "Cyl"], kind="bar")
        plt.title('Voitures ayant le meilleur rapport poids/puissance')
        plt.legend(['Poids en tonne', 'Cyclindrée'])
        self.write_image('Voitures ayant le meilleur rapport poids/puissance', 'rate_weight_cyl')

    def compare(self):
        fig, axs = plt.subplots(2, 2)
        plt.subplots_adjust(bottom=5, top=6)
        df_car = self.df_car.dropna()
        # create a horizontal plot
        axs[0, 0].scatter(df_car['Retail Price'], df_car['City MPG'])
        axs[0, 0].set_title('Prix')

        # create a vertical plot
        axs[1, 0].scatter(df_car['Weight'], df_car['City MPG'])
        axs[1, 0].set_title('Poids')

        # create a horizontal plot
        axs[0, 1].scatter(df_car['Len'], df_car['City MPG'])
        axs[0, 1].set_title('Longueur')

        # create a vertical plot
        axs[1, 1].scatter(df_car['HP'], df_car['City MPG'])
        axs[1, 1].set_title('Cylindrée')
        self.write_image("Comparatif de l'autonomie en ville", 'compare')

        print("> Il y a une correlation entre le prix, le poids, la cylindrée avec l'autonomie."
              " Plus ces facteurs sont élevés moins l'autonomie est grande. La longueur n'a pas vraiment d'influence.",
              end='\n', file=self.output)

    def __exit__(self, *args):
        if self.output:
            self.output.close()


if __name__ == '__main__':
    resume = Resume()
    resume.run()
