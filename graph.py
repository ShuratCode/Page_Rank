import os.path
from collections import Counter
from operator import itemgetter

import pandas as pd


class Graph:

    def __init__(self):
        self.nodes_source = {}  # I am the pointing to the nodes in the list
        self.nodes_dest = {}  # I am being pointed by the nodes in the list
        self.page_rank = {}

    def load_graph(self, path):
        """
        Load the graph from csv file. Init the page rank as 1/graph size for each node.
        :param path: full path for the csv file
        """
        if not os.path.isfile(path):
            raise Exception('No such file')
        df = pd.read_csv(path, sep=',', names=['src', 'dst'])
        for index, row in df.iterrows():
            src = int(row['src'])
            dst = int(row['dst'])
            if src in self.nodes_source.keys():  # already saw this node as an edge source
                pointed_to = self.nodes_source[src]
                pointed_to.append(dst)

            else:  # first time as source node
                pointed_to = [dst]
                self.nodes_source[src] = pointed_to

            if dst in self.nodes_dest.keys():   # already saw this node as an edge destination
                pointed_from = self.nodes_dest[dst]
                pointed_from.append(src)

            else:   # first time as edge destination
                pointed_from = [src]
                self.nodes_dest[dst] = pointed_from

            if src not in self.page_rank.keys():    # first time we saw the node (source)
                self.page_rank[src] = 0
            if dst not in self.page_rank.keys():    # first time we saw the node (destination)
                self.page_rank[dst] = 0
        self.init_page_rank()

    def init_page_rank(self):
        """
        Initialize the page rank for each node.
        The first value is 1/(number of nodes)
        """
        size = len(self.page_rank)
        rank = 1 / size
        for node in self.page_rank.keys():
            self.page_rank[node] = rank

    def calculate_page_rank(self, beta=0.85, delta=0.001):
        """
        Calculate the graph page rank. We use 20 iterates and for each iteration we check the delta.
        :param beta: the probability to random jump to another node
        :param delta: if the total difference is smaller from the delta stop the algorithm
        """
        new_page_rank = {}
        for i in range(0, 20):
            for node in self.page_rank.keys():
                sum_in_ranks = 0
                if node in self.nodes_dest.keys():
                    for source in self.nodes_dest[node]:
                        if source in self.nodes_source.keys():
                            d_i = len(self.nodes_source[source])
                            former_rank = self.page_rank[source]
                            normalize_rank = beta * (former_rank / d_i)
                            sum_in_ranks += normalize_rank
                new_page_rank[node] = sum_in_ranks
            new_page_rank = self.re_insert_leaked_page_rank(new_page_rank)
            old_page_rank = self.page_rank
            self.page_rank = new_page_rank
            new_page_rank = {}
            if self.delta_check(old_page_rank, delta):
                break

    def re_insert_leaked_page_rank(self, page_rank):
        """
        Normalize the page rank so we don't have any zero.
        The normalization is with (1-S)/N where S is the total page rank and N is the size of the graph
        :param page_rank: dictionary of nodes and their page rank
        :return: dictionary of the normalize page rank
        """
        copy_page_rank = page_rank.copy()
        sum_of_page_ranks = self.sum_of_ranks(page_rank) # This is S
        num_of_nodes = len(page_rank) # This is N
        for node in page_rank.keys():
            rank = page_rank[node]
            addition = (1 - sum_of_page_ranks) / num_of_nodes
            copy_page_rank[node] = rank + addition
        return copy_page_rank

    def sum_of_ranks(self, page_rank):
        """
        Sum all the page rank
        :param page_rank: dictionary of nodes and their page rank
        :return:  The total sum
        """
        sum_of_ranks = 0
        for rank in page_rank.values():
            sum_of_ranks += rank
        return sum_of_ranks

    def delta_check(self, page_rank, delta):
        """
        Check if the difference between the new page rank and the new one is smaller or bigger from the delta
        :param page_rank: dictionary of the old page rank (from last iteration)
        :param delta: the delta threshold
        :return: true if delta is bigger, false otherwise
        """
        sum_delta = 0
        for node in self.page_rank.keys():
            new_delta = abs(page_rank[node] - self.page_rank[node])
            sum_delta += new_delta
        return delta > sum_delta

    def get_PageRank(self, node_name):
        """
        Return a specific page rank for a specific node
        :param node_name: The node name (Can be string)
        :return: the page rank of the node if found. -1 otherwise
        """
        node = int(node_name)
        if node not in self.page_rank.keys():
            return -1
        return self.page_rank[node]

    def get_top_nodes(self, n):
        """
        return the top n nodes with the highest page rank
        :param n: the number of nodes to return
        :return: list of pairs of key, value. The key is the node number and the value is the page rank
        """
        return Counter(self.page_rank).most_common(n)

    def get_all_PageRank(self):
        """
        Return all nodes and page rank, sorted from highest to lowest
        :return:
        """
        sorted_dict = sorted(self.page_rank.items(), key=itemgetter(1), reverse=True)
        return sorted_dict
