import networkx as nx
import sys
import json

def add_nodes(input):
    G=nx.Graph()
    # Add nodes to G
    for line in input:
        point = json.loads(line)
        G.add_edge(point[0],point[1])
    return G

def shortest_path_to_nodes(G, s):
    Search = []
    Level = {}
    Parent = {}
    p_x={}

    # Initialize parent nodes
    for node in G:
        Parent[node] = []

    # Initialize shortest path to nodes p(x)
    # p_x = dict.fromkeys(G, 0.0)
    for node in G.nodes():
        p_x[node]=0.0

    p_x[s] = 1.0  # p(root) = 1
    Level[s] = 0  # level(root)=0
    Queue = [s]   # Queue of each level, starting from root

    # use BFS to find shortest paths
    while Queue:
        node = Queue.pop(0)
        Search.append(node)
        Levelv = Level[node]
        p_xv = p_x[node]

        for w in G[node]:
            if w not in Level:
                Queue.append(w)
                Level[w] = Levelv + 1
            if Level[w] == Levelv + 1:   # -> shortest path, count paths
                p_x[w] += p_xv
                Parent[w].append(node)  # Add to parent

    return Search, Parent, p_x

def shortest_path_through_edges(G,Search, Parent, p_x, s):
    betweenness = dict.fromkeys(G, 0.0)
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    child_p_prime_total = dict.fromkeys(Search, 0)
    while Search:
        w = Search.pop()
        coef = (1.0 + child_p_prime_total[w]) / p_x[w]
        for v in Parent[w]:
            # shortest_path_through_nodes
            p_prime = p_x[v] * coef
            if (v, w) not in betweenness:
                betweenness[(w, v)] += p_prime
            else:
                betweenness[(v, w)] += p_prime
            child_p_prime_total[v] += p_prime
        if w != s:
            betweenness[w] += child_p_prime_total[w]

    # Return edges only
    for n in G:
        del betweenness[n]
    betweenness={k:v for k,v in betweenness.items() if v!=0}
    return betweenness

def betweenness(G):
    bet=[]
    for node in G.nodes():
        Search, Parent, p_x=shortest_path_to_nodes(G, node)
        dict=shortest_path_through_edges(G,Search, Parent, p_x, node)
        for key, value in dict.iteritems():
            temp = [sorted(key),value]
            bet.append(temp)

    for edge in G.edges():
        sum=0
        jenc = json.JSONEncoder()
        for i in bet:
            if sorted(edge)==i[0]:
                sum+=i[1]
        print jenc.encode(sorted(edge)),": ",sum/2

if __name__ == '__main__':
    input_lines = open(sys.argv[1])
    Graph_G=add_nodes(input_lines)
    betweenness(Graph_G)