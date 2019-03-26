import os.path
from collections import Counter
from collections import OrderedDict

import pandas as pd


class Graph:

    def __init__(self):
        self.nodes_source = {}  # I am the pointing to the nodes in the list
        self.nodes_dest = {}  # I am being pointed by the nodes in the list
        self.page_rank = {}
        self.delta = 0.001
        self.beta = 0.85

    def load_graph(self, path):
        if not os.path.isfile(path):
            raise Exception('No such file')
        df = pd.read_csv(path, sep=',', names=['src', 'dst'])
        for index, row in df.iterrows():
            src = int(row['src'])
            dst = int(row['dst'])
            if src in self.nodes_source.keys():
                pointed_to = self.nodes_source[src]
                pointed_to.append(dst)

            else:
                pointed_to = [dst]
                self.nodes_source[src] = pointed_to

            if dst in self.nodes_dest.keys():
                pointed_from = self.nodes_dest[dst]
                pointed_from.append(src)

            else:
                pointed_from = [src]
                self.nodes_dest[dst] = pointed_from

            if src not in self.page_rank.keys():
                self.page_rank[src] = 0
        self.init_page_rank()

    def init_page_rank(self):
        size = len(self.page_rank)
        rank = 1 / size
        for node in self.page_rank.keys():
            self.page_rank[node] = rank

    def calculate_page_rank(self):
        new_page_rank = {}
        for i in range(0, 20):
            for node in self.page_rank.keys():
                sum_in_ranks = 0
                for source in self.nodes_dest[node]:
                    d_i = len(self.nodes_source[source])
                    former_rank = self.page_rank[source]
                    normalize_rank = self.beta * (former_rank / d_i)
                    sum_in_ranks += normalize_rank
                new_page_rank[node] = sum_in_ranks
            old_page_rank = self.page_rank
            self.page_rank = new_page_rank
            new_page_rank = {}
            if self.delta_check(old_page_rank):
                break

    def delta_check(self, page_rank):
        sum_delta = 0
        for node in self.page_rank.keys():
            new_delta = abs(page_rank[node] - self.page_rank[node])
            sum_delta += new_delta
        return self.delta > sum_delta

    def get_PageRank(self, node_name):
        node = int(node_name)
        if node not in self.page_rank.keys():
            return -1
        return self.page_rank[node]

    def get_top_nodes(self, n):
        top_n = Counter(self.page_rank).most_common(n)
        return top_n

    def get_all_PageRank(self):
        sorted_dict = OrderedDict(self.page_rank)
        return sorted_dict
