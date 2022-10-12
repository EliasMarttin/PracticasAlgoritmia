#!/usr/bin/env python3
import sys
from random import shuffle, seed
from typing import TextIO, Optional

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.queues import Fifo

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]

NO_VALID_WALL = 'NO VALID WALL'


# Función ya implementada
# Esta función utiliza un MFSet para crear un laberinto, pero le añade n aristas
# adicionales que provocan que el laberinto tenga ciclos.
def create_labyrinth(rows: int, cols: int, n: int, s: int) -> UndirectedGraph[Vertex]:
    vertices: list[Vertex] = [(r, c) for r in range(rows) for c in range(cols)]
    mfs: MergeFindSet[Vertex] = MergeFindSet((v,) for v in vertices)
    edges: list[Edge] = [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    edges.extend([((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)])
    seed(s)
    shuffle(edges)
    corridors: list[Edge] = []
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))
        elif n > 0:
            n -= 1
            corridors.append((u, v))
    return UndirectedGraph(E=corridors)


def read_data(f: TextIO) -> tuple[UndirectedGraph[Vertex], int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    n = int(f.readline())
    s = int(f.readline())
    grafo = create_labyrinth(rows, cols, n, s)
    return grafo, rows, cols


def process(lab: UndirectedGraph[Vertex], rows: int, cols: int) -> tuple[Optional[Edge], int, int]:
    mapita = {'v_start':0}

    lejitudDelInicio = 0# número de saltos que hemos dado hasta llegar a este nodo. y esto es lo qeu vamoa a guardar en el mapa
    #lejituddelFinal = 0
    v_start = (0, 0)
    mapita[v_start] = lejitudDelInicio
    v_final = (rows, cols)
    queue = Fifo()
    seen = set()
    queue.push(v_start)
    seen.add(v_start)
    listaCamino = []
    while len(queue) > 0:
        v = queue.pop()
        listaCamino.append(v)
    # Tenemos que guardar el camino
    if v == v_final:
        return v
    for suc in lab.succs(v):
        if suc not in seen:
            lejitudDelInicio += lejitudDelInicio + 1
            mapita[suc] = lejitudDelInicio
            seen.add(suc)
            queue.push(suc)
    return None

def show_results(edge_to_add: Optional[Edge], length_before: int, length_after: int):
    raise NotImplementedError()


if __name__ == '__main__':
    graph0, rows0, cols0 = read_data(sys.stdin)
    edge_to_add0, length_before0, length_after0 = process(graph0, rows0, cols0)
    show_results(edge_to_add0, length_before0, length_after0)
