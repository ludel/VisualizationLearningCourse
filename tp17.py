import json
import os
from collections import deque

import lxml.html as html_parser
import requests

OUTPUT_PRINT = 'print'
OUTPUT_FILE = 'file'


class Scraping:
    def __init__(self, initial_tag='cat', output_type=OUTPUT_PRINT, nb_iteration=50):
        if output_type == OUTPUT_FILE:
            os.makedirs('dataset', exist_ok=True)
            self.output = open('dataset/cats.csv', 'w')
        else:
            self.output = None
            self.output_detail = None

        print('main_tag', 'post_code', 'dimensions', 'post_timestamp', 'owner_id', 'like_count', 'img', 'text', sep=',',
              file=self.output)

        self.nb_iteration = nb_iteration
        self.current_json = None

        self.set_config(initial_tag)
        self.saved_tags = []
        self.saved_post = []
        self.related_tags = deque([initial_tag])

    @property
    def shortcut(self):
        return self.current_json['entry_data']['TagPage'][0]['graphql']['hashtag']

    def set_config(self, tag):
        page = requests.get(f'https://www.instagram.com/explore/tags/{tag}/')
        tree = html_parser.fromstring(page.content)
        flat_json = tree.xpath('..//script[contains(text(), "window._sharedData")]/text()')[0][21:-1]
        self.current_json = json.loads(flat_json)

    def export_tag_post(self):
        tags = self.shortcut
        top_posts = tags['edge_hashtag_to_top_posts']['edges']
        self.saved_tags.append(tags['name'])
        self.update_related_tags()

        for post in top_posts:
            node = post['node']

            if node['shortcode'] in self.saved_post:
                continue

            self.saved_post.append(node['shortcode'])

            dimension = f"{node['dimensions']['height']}x{node['dimensions']['width']}"

            try:
                text = node['edge_media_to_caption']['edges'][0]['node']['text'].replace('\n', '').replace(',', '')
            except IndexError:
                text = ''

            print(tags['name'], node['shortcode'], dimension, node['taken_at_timestamp'], node['owner']['id'],
                  node['edge_liked_by']['count'], node['display_url'], text, sep=',', file=self.output)

    def update_related_tags(self):
        for tag in self.get_related_tag():
            if tag not in self.saved_tags and tag not in self.related_tags:
                self.related_tags.append(tag)

    def get_related_tag(self):
        tags = self.shortcut['edge_hashtag_to_related_tags']['edges']
        return [t['node']['name'] for t in tags if t not in self.saved_tags]

    def run(self):
        for i in range(self.nb_iteration):
            current_tag = self.related_tags.popleft()
            self.set_config(current_tag)
            self.export_tag_post()
            print(f"=> tag <{current_tag}> - {i + 1}/{self.nb_iteration}")

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            self.output.close()


if __name__ == '__main__':
    with open('dataset/config_insta.json', 'r') as f:
        data = json.loads(f.read())

    s = Scraping('cat', output_type=OUTPUT_FILE, nb_iteration=50)
    s.run()
