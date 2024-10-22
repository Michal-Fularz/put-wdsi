import queue
import math


def create_graph() -> dict[int, list[(int, int)]]:
    graph = {
        1: [(2, 1), (3, 1)],
        2: [(1, 1), (5, 7)],
        3: [(1, 1), (4, 2)],
        4: [(3, 2), (6, 1)],
        5: [(2, 7), (6, 3), (8, 2)],
        6: [(4, 1), (5, 3), (7, 5), (8, 6)],
        7: [(6, 5)],
        8: [(5, 2), (6, 6)],
    }

    return graph


def bfs(s: int, g: int, graph: dict[int, list[(int, int)]]) -> list[int]:
    # s - wierzchołek startowy
    # g - wierzchołek docelowy
    # nodes - lista wierzchołków
    nodes = list(graph.keys())

    # lista odwiedzonych wierzchołków
    visited = set()
    # słownik kosztów
    cost = {n: math.inf for n in nodes}
    # słownik poprzedników
    parent = {n: None for n in nodes}

    # utwórz kolejke, w której elementy są ułożone nie w kolejności wprowadzania, lecz w kolejności priorytetu.
    q = queue.PriorityQueue()
    # dodaj wierzchołek startowy
    # push(q, (0, s))
    q.put((0, s))
    cost[s] = 0
    # ustaw jego poprzednika jako jego samego, aby oznaczyć go jako odwiedzony
    parent[s] = s
    # dopóki kolejka nie jest pusta, czyli są jeszcze jakieś wierzchołki do odwiedzenia
    # while not empty(q):
    while not q.empty():
        # pobierz następny wierzchołek i usuń go z kolejki
        # cur_n = front(q)
        # pop(q)
        cur_n = q.get()[1]

        # przerwij jeśli odwiedzony
        if cur_n in visited:
            continue

        # przerwij jeśli dotarliśmy do celu
        if cur_n == g:
            break

        # dla wszystkich krawędzi z aktualnego wierzchołka
        # for nh, distance in edges(cur_n):
        for nh, distance in graph[cur_n]:
            # przerwij jeśli sąsiad był już odwiedzony
            if nh in visited:
                continue
            # pobierz koszt sąsiada lub przypisz mu inf
            old_cost = cost[nh]
            # oblicz koszt dla danego wierzchołka
            new_cost = cost[cur_n] + distance
            # rozważ nową ścieżkę tylko wtedy, gdy jest lepsza niż dotychczas najlepsze ścieżka
            if new_cost < old_cost:
                # zaktualizuj wartość sąsiada w słowniku kosztów
                cost[nh] = new_cost
                # ustaw poprzednika
                parent[nh] = cur_n
                # dodaj sąsiada do kolejki
                # push(q, (new_cost, nh))
                q.put((new_cost, nh))

            #     # jeśli sąsiad nie był jeszcze odwiedzony
            # if nh not in visited:
            #     # oznacz jako odwiedzony i dodaj do kolejki
            #     parent[nh] = cur_n
            #     # add(visited, nh)
            #     visited.add(nh)
            #     # push(q, nh)
            #     q.put(nh)

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
    path = bfs(1, 8, graph)
    print(path)

    assert bfs(1, 4, graph) == [1, 3, 4]
    assert bfs(1, 8, graph) == [1, 3, 4, 6, 5, 8]
    assert bfs(3, 5, graph) == [3, 4, 6, 5]


if __name__ == '__main__':
    ex_1()
