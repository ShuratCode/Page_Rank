from graph import Graph

if __name__ == '__main__':
    g = Graph()
    g.load_graph(r"C:\Users\Shaked Eyal\IdeaProjects\Page_Rank\Resources\wiki.csv")
    g.calculate_page_rank()
    all_page_ranks = g.get_all_PageRank()
    for key, value in all_page_ranks:
        print(key, value)
