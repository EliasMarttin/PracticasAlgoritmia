#!/usr/bin/env python3
import sys
from collections.abc import Iterator, Iterable
from random import shuffle, seed
from typing import TextIO, Optional

import algoritmia.algorithms.shortest_path
from algoritmia.algorithms.shortest_path import TPath
from algoritmia.datastructures.graphs import UndirectedGraph, TVertex, IGraph, TEdge
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.queues import Fifo
from algoritmia.algorithms import traversers
from algoritmia.algorithms import shortest_path

mapitaPabajo = {}
mapitaParriba = {}
TVertex = tuple[int, int]
Tpath = list[TVertex]

NO_VALID_WALL = 'NO VALID WALL'


# Función ya implementada
# Esta función utiliza un MFSet para crear un laberinto, pero le añade n aristas
# adicionales que provocan que el laberinto tenga ciclos.
def create_labyrinth(rows: int, cols: int, n: int, s: int) -> UndirectedGraph[TVertex]:
    vertices: list[TVertex] = [(r, c) for r in range(rows) for c in range(cols)]
    mfs: MergeFindSet[TVertex] = MergeFindSet((v,) for v in vertices)
    edges: list[TEdge] = [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    edges.extend([((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)])
    seed(s)
    shuffle(edges)
    corridors: list[TEdge] = []
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))
        elif n > 0:
            n -= 1
            corridors.append((u, v))
    return UndirectedGraph(E=corridors)


def read_data(f: TextIO) -> tuple[UndirectedGraph[TVertex], int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    n = int(f.readline())
    s = int(f.readline())
    grafo = create_labyrinth(rows, cols, n, s)
    return grafo, rows, cols

def process(lab: UndirectedGraph[TVertex], rows: int, cols: int) -> tuple[Optional[TEdge], int, int]:
    v_inicial = (0, 0)
    v_final = (rows - 1, cols - 1)
    bf_edge_traverserPabajo(lab, v_inicial)
    bf_edge_traverserParriba(lab, v_final)
    minDist = mapitaPabajo[v_final]
    TEdge = None
    print(len(mapitaParriba))
    print(len(mapitaPabajo))
    for x in mapitaPabajo:
        r, c = x
        y = mapitaPabajo[x]
        if r > 0 and y + mapitaParriba[(r - 1, c)] < minDist:
            minDist = y + mapitaParriba[(r - 1, c)]
            TEdge = ((r - 1, c), (r, c))

        if c > 0 and y + mapitaParriba[(r, c - 1)] < minDist:
            minDist = y + mapitaParriba[(r, c - 1)]
            TEdge = ((r, c - 1), (r, c))

        if r < rows - 1 and y + mapitaParriba[(r + 1, c)] < minDist:
            minDist = y + mapitaParriba[(r + 1, c)]
            TEdge = ((r, c), (r + 1, c))

        if c < cols - 1 and y + mapitaParriba[(r, c + 1)] < minDist:
            minDist = y + mapitaParriba[(r, c + 1)]
            TEdge = ((r, c), (r, c + 1))

        print(TEdge)
    return TEdge, mapitaPabajo[v_final], minDist


def bf_edge_traverserPabajo(graph: IGraph[TVertex], v_initial: TVertex):

    queue = Fifo()
    seen = set()
    mapitaPabajo[v_initial] = 0
    queue.push(v_initial)
    seen.add(v_initial)
    while len(queue) > 0:
        v = queue.pop()
        for suc in graph.succs(v):
            if suc not in seen:
                mapitaPabajo[suc] = mapitaPabajo[v] + 1
                queue.push(suc)
                seen.add(suc)


def bf_edge_traverserParriba(graph: IGraph[TVertex], v_initial: TVertex):
    queue = Fifo()
    seen = set()
    mapitaParriba[v_initial] = 1
    queue.push(v_initial)
    seen.add(v_initial)
    while len(queue) > 0:
        v = queue.pop()
        for suc in graph.succs(v):
            if suc not in seen:
                mapitaParriba[suc] = mapitaParriba[v] + 1
                queue.push(suc)
                seen.add(suc)


def sentinel(edges2: IGraph, rows: int, cols: int):
    print(rows, cols)
    print(mapitaPabajo[5, 8])
    print(mapitaParriba[5, 9])
    print("----------------------")
    mejorArista = (
        (0, 0), (0, 0))  # ---> TEdge = ((1,2),(1,3)) Esto es el resultado si es que es la mejor arista de todas

    return mejorArista


def path_recover(edges: Iterable[TEdge], v: TVertex) -> TPath:
    # Creates backpointer dictionary (bp)
    bp = {}
    for o, d, e in edges:
        bp[d] = o
        if d == v:  # I have all I need
            break
    # Recover the path jumping back
    path = [v]
    while v != bp[v]:
        v = bp[v]
        path.append(v)
    # reverse the path
    path.reverse()
    return path


def show_results(edge_to_add: Optional[TEdge], length_before: int, length_after: int):
  #Esto se tiene que cambiar.
   print("NO VALID WALL")
   print(length_before)
   print(length_after)


if __name__ == '__main__':
    graph0, rows0, cols0 = read_data(sys.stdin)
    edge_to_add0, length_before0, length_after0 = process(graph0, rows0, cols0)
    show_results(edge_to_add0, length_before0, length_after0)
