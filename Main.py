from graph import Graph

if __name__ == '__main__':
    g = Graph()
    g.load_graph(r"C:\Users\Shaked Eyal\IdeaProjects\Page_Rank\Resources\wiki.csv")
    g.calculate_page_rank()
    top_n = g.get_top_nodes(5)
    print("Specific page rank")
    print(g.get_PageRank(4037))
    print('=' * 80)
    print("Top N")
    for key, value in top_n:
        print(key, value)
    all_page_ranks = g.get_all_PageRank()
    print('=' * 80)
    print("All page ranks")
    for key, value in all_page_ranks:
        print(key, value)
