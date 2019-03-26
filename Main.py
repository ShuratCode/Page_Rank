from graph import Graph

if __name__ == '__main__':
    g = Graph()
    g.load_graph(r"C:\Users\Shaked Eyal\IdeaProjects\Page_Rank\Resources\example.csv")
    g.calculate_page_rank()
    print(g.page_rank)
