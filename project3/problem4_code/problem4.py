def floyd_warshall_algorithm(graph):

    nodes = list(graph.keys())
    n = len(nodes)
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}
    pred = {u: {v: u for v in nodes} for u in nodes} # we need this to get the cycle after

    for u in graph:
        for v in graph[u]:
            dist[u][v] = graph[u][v]
    # get the distances as per the paper
    for k in nodes:
        for i in nodes:
            for j in nodes:
                #calculate the shortest path
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
    
    cycle = []
    # check for negative cycles
    for u in nodes:
        if dist[u][u] < 0:
            # get the negative cycle
            node = u
            while node not in cycle:
                cycle.append(node)
                node = pred[u][node]
            return None, cycle, "Negative cycle detected. Problem is inconsistent as per Theorem 3.1 of the paper provided."
    
    # set the diagonal to 0 (distance to itself, no need for negative cycle check anymore)
    for u in nodes:
        dist[u][u] = 0
    return dist, cycle, "No inconsistencies. Shortest paths computed."

graph_myproblem = {
    'X0': {'X1': 10},
    'X1': {'X0': 0, 'X2': 40},
    'X2': {'X1': -30, 'X4': 15},
    'X3': {'X4': 15},
    'X4': {'X2': -15, 'X3': -5}
}

graph_paperproblem = {
    '0': {'1': 20, '4': 70},
    '1': {'0': -10, '2': 40},
    '2': {'1': -30, '3': -10},
    '3': {'2': 20, '4': 50},
    '4': {'3': -40, '0': -60}
}


solution, cycle, result_message = floyd_warshall_algorithm(graph_myproblem)
if solution:
    print("Shortest path solution on my graph (d-graph):")
    for i in solution:
        print (i, solution[i])
    print("\n", end="")
    print("Problem solution (max times):")
    for j in solution['X0']:
        print(f"{j}: {solution['X0'][j]}")
print(result_message)
if cycle:
    print("Negative cycle:", cycle)
print("\n", end="")

solution, cycle, result_message = floyd_warshall_algorithm(graph_paperproblem)
if solution:
    print("Shortest path solution on the paper's graph (d-graph):")
    for i in solution:
        print (i, solution[i])
    print("\n", end="")
    print("Problem solution (max times):")
    for j in solution['0']:
        print(f"{j}: {solution['0'][j]}")
print(result_message)
if cycle:
    print("Negative cycle:", cycle)

