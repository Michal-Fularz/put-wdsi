import queue


def create_graph() -> dict[int, list[int]]:
    graph = {
        1: [2, 3],
        2: [1, 5],
        3: [1, 4],
        4: [3, 6],
        5: [2, 6, 8],
        6: [4, 5, 6, 8],
        7: [6],
        8: [5, 6],
    }

    return graph


def bfs(s: int, g: int, graph: dict[int, list[int]]) -> list[int]:
    # s - wierzchołek startowy
    # g - wierzchołek docelowy
    # nodes - lista wierzchołków
    nodes = list(graph.keys())

    # lista odwiedzonych wierzchołków
    visited = set()
    # słownik poprzedników
    parent = {n: None for n in nodes}

    q = queue.Queue()

    # dodaj wierzchołek startowy
    # push(q, s)
    q.put(s)
    # ustaw jego poprzednika jako jego samego, aby oznaczyć go jako odwiedzony
    parent[s] = s
    # dopóki kolejka nie jest pusta, czyli są jeszcze jakieś wierzchołki do odwiedzenia
    # while not empty(q):
    while not q.empty():
        # pobierz następny wierzchołek i usuń go z kolejki
        # cur_n = front(q)
        # pop(q)
        cur_n = q.get()

        # przerwij jeśli dotarliśmy do celu
        if cur_n == g:
            break

        # dla wszystkich krawędzi z aktualnego wierzchołka
        # for nh in edges(cur_n):
        for nh in graph[cur_n]:
            # jeśli sąsiad nie był jeszcze odwiedzony
            if nh not in visited:
                # oznacz jako odwiedzony i dodaj do kolejki
                parent[nh] = cur_n
                # add(visited, nh)
                visited.add(nh)
                # push(q, nh)
                q.put(nh)

    # ścieżka do wierzchołka docelowego
    path = []

    # zaczynamy od wierzchołka docelowego i cofamy się po znalezionej ścieżce
    cur_n = g
    # dopóki nie dotrzemy do startu
    while cur_n != s:
        # dodajemy aktualny wierzchołek i przechodzimy do poprzednika
        # add(path, cur_n)
        path.append(cur_n)
        cur_n = parent[cur_n]
    path.append(s)
    # wierzchołki są w odwrotnej kolejności, więc odwracamy listę
    # reverse(path)
    path.reverse()
    return path


def ex_1():
    graph = create_graph()
    path = bfs(1, 4, graph)
    print(path)

    assert bfs(1, 4, graph) == [1, 3, 4]
    assert bfs(1, 8, graph) == [1, 2, 5, 8]
    assert bfs(3, 5, graph) == [3, 1, 2, 5]
    # despite the length being the same does not work, as bfs returns first shortest path
    # assert bfs(3, 5, graph) == [3, 4, 6, 5]


if __name__ == '__main__':
    ex_1()
