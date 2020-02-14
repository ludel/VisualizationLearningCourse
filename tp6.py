import pandas as pd

info_vin = pd.read_csv('dataset/winemag-data-130k-v2.csv', index_col=0)
info_ca_video = pd.read_csv('dataset/CAvideos.csv')
info_fr_video = pd.read_csv('dataset/FRvideos.csv')

info_vin_rename_region = info_vin[['region_1', 'region_2']].rename(columns={'region_1': 'region', 'region_2': 'locale'})

info_vin_renomme_index = info_vin.copy().rename_axis()

info_fr_video.set_index(['video_id', 'trending_date'], verify_integrity=True, inplace=True)
info_ca_video.set_index(['video_id', 'trending_date'], verify_integrity=True, inplace=True)
videos_communes = info_fr_video.join(info_ca_video, how='inner', lsuffix='_FR', rsuffix='_CA')

test_df = videos_communes.iloc[:50]


def cleaner(row):
    kset = []
    for i in videos_communes.keys():
        if videos_communes[i].dtype == 'bool' or videos_communes[i].dtype == 'int':
            if i[:-3] not in kset:
                kset.append(i[:-3])
                row[i[:-3]] = row[i]
            else:
                if videos_communes[i].dtype == 'bool':
                    row[i[:-3]] = row[i[:-3]] or row[i]
                if videos_communes[i].dtype == 'int':
                    row[i[:-3]] = max(row[i[:-3]], row[i])
    return row


video_propre = videos_communes.head(50).apply(cleaner, axis='columns')
l = []
for i in video_propre.keys():
    if '_FR' not in i and '_CA' not in i:
        l.append(i)

for i in l:
    del video_propre[i + '_FR']
    del video_propre[i + '_CA']
