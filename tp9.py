import csv

import lxml.html as html_parser
import requests

page_list = requests.get('https://en.wikipedia.org/wiki/List_of_dog_breeds')
tree = html_parser.fromstring(page_list.content)
lines = tree.xpath("/html/body/div[3]/div[3]/div[4]/div/table/tbody/tr")

file = open('dataset/dogs.csv', 'w', newline='')
writer = csv.DictWriter(file, fieldnames=['id', 'name', 'picture', 'origin', 'url', 'other_name', 'weight', 'height',
                                          'coat', 'color', 'litter_size', 'life_span'])
writer.writeheader()

names, pictures, origins, url = [], [], [], []

for line in lines:
    name = line.xpath('./td[2]/a/text()')
    picture = line.xpath('./td[1]/a/img')

    if not len(name) or not len(picture):
        continue

    names.extend(name)
    pictures.extend(picture)
    origins.extend(line.xpath('./td[3]'))
    url.extend(line.xpath('./td[2]/a/@href'))


def get_text(page, paths: list):
    for path in paths:
        content = page.xpath(path+'/text()')

        if len(content) > 0:
            return ' '.join(c.replace('\n', '') for c in content)


def get_weight(page):
    content = page.xpath('./tr[5]/td/table/tbody/tr[2]/td/text()')

    return ''


for index, (name, picture, origin, url) in enumerate(zip(names, pictures, origins, url)):
    picture = 'https:' + picture.attrib['src'].replace('\\', '/') if picture is not None else 'NaN'
    origin = (origin.text or '').replace('\n', '')

    detail_page = requests.get(f'https://en.wikipedia.org{url}')
    page_dog = html_parser.fromstring(detail_page.content)

    dog_page_spec = page_dog.xpath("/html/body/div[3]/div[3]/div[4]/div/table[1]/tbody")[0]

    other_name = ' '.join(dog_page_spec.xpath("./tr[3]/td/text()"))

    writer.writerow({'id': index, 'name': name, 'picture': picture, 'origin': origin, 'url': url,
                     'other_name': ' '.join(dog_page_spec.xpath("./tr[3]/td/text()")),
                     'weight': get_weight(dog_page_spec),
                     'coat': get_text(dog_page_spec, ['./tr[5]/td/table/tbody/tr[4]/td', './tr[6]/td/table/tbody/tr[6]/td']),
                     'color': get_text(dog_page_spec, ['./tr[5]/td/table/tbody/tr[7]']),
                     'litter_size': get_text(dog_page_spec, ['./tr[5]/td/table/tbody/tr[8]/td']),
                     'life_span': get_text(dog_page_spec, ['./tr[5]/td/table/tbody/tr[9]/td']),
                     'height': ''})
    print(f'=> page {index}')
file.close()
