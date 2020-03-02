import collections
import json
import os

import requests
from tulip import tlp
from tulipgui import tlpgui


class Visualisation:
    def __init__(self, site_url, backup=None):
        self.site_url = site_url
        self.data = self.get_backup(backup) if backup else {}
        self.graph_post = tlp.newGraph()
        self.graph_user = tlp.newGraph()
        self.viewLabelPost = self.graph_post.getStringProperty("viewLabel")
        self.viewLabelUser = self.graph_user.getStringProperty("viewLabel")

        os.makedirs('dataset', exist_ok=True)

    def set_category(self):
        print('=> Get all categories')
        self.data['categories'] = {}

        res_categories = requests.get(f'{self.site_url}/categories.json')
        for category in res_categories.json()['category_list']['categories']:
            self.data['categories'][category['id']] = category
            print(f"    => category: {category['name']}")

    def set_top_topics(self, nb_page=5):
        print(f'=> Get top topics')
        self.data['topics'] = {}

        for page in range(nb_page):
            res_topics = requests.get(f'{self.site_url}/top.json?page={page}')
            print(f"    => topic page: {page}")

            for topic in res_topics.json()['topic_list']['topics']:
                self.data['topics'][topic['id']] = topic

    def set_posts(self):
        print('=> Get topic posts')
        self.data['posts'] = {}

        for index, topic_id in enumerate(self.data['topics'].keys()):
            res_posts = requests.get(f"{self.site_url}/t/{topic_id}/posts.json")
            print(f"    => topic post: {topic_id} - {index + 1}/{len(self.data['topics'])}")

            for post in res_posts.json()['post_stream']['posts']:
                self.data['posts'][post['id']] = post

    def set_users(self):
        print('=> Get user')
        self.data['users'] = {}

        for post in self.data['posts'].values():
            username = post['username']
            if self.data['users'].get(username):
                self.data['users'][username]['posts'].append(post['id'])
            else:
                self.data['users'][username] = {'username': username, 'name': post['name'], 'posts': [post['id']]}

    @staticmethod
    def get_backup(path_file):
        with open(path_file, 'r') as f:
            return json.loads(f.readline())

    def dump_data(self, path_file):
        with open(path_file, 'w') as f:
            f.write(json.dumps(self.data))

    def build_graph_post(self):
        for category_id, category in self.data['categories'].items():
            category_node = self.graph_post.addNode()
            self.viewLabelPost[category_node] = category['name']
            self.data['categories'][category_id]['node'] = category_node

        for topic_id, topic in self.data['topics'].items():
            topic_node = self.graph_post.addNode()
            self.viewLabelPost[topic_node] = topic['title']
            self.data['topics'][topic_id]['node'] = topic_node
            topic_category = str(topic['category_id'])

            if self.data['categories'].get(topic_category):
                category_node = self.data['categories'][topic_category]['node']
                self.graph_post.addEdge(category_node, topic_node)

        for post_id, post in self.data['posts'].items():
            post_node = self.graph_post.addNode()
            self.viewLabelPost[post_node] = str(post_id)
            self.data['posts'][post_id] = post_node
            post_topic = post['topic_id']

            if self.data['topics'].get(post_topic):
                if not self.data['users'][post['username']].get('node'):
                    user_node = self.graph_post.addNode()
                    self.viewLabelPost[user_node] = post['username']
                    self.data['users'][post['username']]['node'] = user_node

                topic_node = self.data['topics'][post_topic]['node']
                self.graph_post.addEdge(topic_node, self.data['users'][post['username']]['node'])
                self.graph_post.addEdge(self.data['users'][post['username']]['node'], post_node)

    def build_graph_user(self):
        topics = collections.defaultdict(list)
        for post_id, post in self.data['posts'].items():
            topics[post['topic_id']].append(post)
        user_nodes = {}

        for topic_id, posts in topics.items():
            users = []
            for post in posts:
                if post['username'] not in user_nodes.keys():
                    user_node = self.graph_user.addNode()
                    self.viewLabelUser[user_node] = post['username']
                    user_nodes[post['username']] = user_node

                users.append(user_nodes[post['username']])

            for user_1 in users:
                for user_2 in users:
                    if user_1 == user_2:
                        continue
                    self.graph_user.addEdge(user_1, user_2)

    def show_graph(self):
        params_post = tlp.getDefaultPluginParameters('Bubble Tree')
        self.graph_post.applyLayoutAlgorithm('Bubble Tree', params_post)
        nodeLinkView = tlpgui.createView("Node Link Diagram view", self.graph_post, {}, True)
        nodeLinkView.centerView()

        params_user = tlp.getDefaultPluginParameters('Circular')
        self.graph_user.applyLayoutAlgorithm('Circular', params_user)
        nodeLinkView = tlpgui.createView("Node Link Diagram view", self.graph_user, {}, True)
        nodeLinkView.centerView()

    def save_graph(self, path):
        tlp.saveGraph(self.graph_post, path + '/post.tlpbz')
        tlp.saveGraph(self.graph_user, path + '/user.tlpbz')

    def set_all_data(self):
        self.set_category()
        self.set_top_topics()
        self.set_posts()
        self.set_users()


if __name__ == '__main__':
    v = Visualisation('https://forums.docker.com/')
    v.set_all_data()
    # v.dump_data('save')

    # le premier graphique montre les relations entre les utilisateurs en fonction des topics
    v.build_graph_user()

    # Le deuxieme graphique montre la hiérarchie entre les categories, les topics, les utilisateurs et les postes.
    v.build_graph_post()
    v.show_graph()
    # v.save_graph('save/docker.tlpbz')
