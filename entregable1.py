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
    pabajo = bf_edge_traverser(lab,v_inicial)
    parriba = bf_edge_traverser(lab,v_final)
    for x in pabajo:
        print(mapitaPabajo[x])

    for vector in mapitaPabajo:
        r = vector[0]
        c = vector[1]  # Con esto buscamos el vector al que saltaremos desde vector
        if c + 1 < cols and mapitaPabajo[vector] + mapitaParriba[vector] < mapitaPabajo[v_final]:
            mejorVector = ((r, c), (r, c + 1))  #
            vectorbueno = vector
            print("Esta es la arista buena /de momento")
            # derecha --->(r,c) > (r+1,c)
        if r - 1 >= 0 and mapitaPabajo[vector] + mapitaParriba[vector] < mapitaPabajo[v_final]:
            mejorVector = ((r, c), (r + 1, c))
            vectorbueno = vector
            print("Esta es la arista buena /de momento")
            # abajo ---> (r,c) > (r,c-1)
        if c - 1 >= 0 and mapitaPabajo[vector] + mapitaParriba[vector] < mapitaPabajo[v_final]:
            mejorVector = ((r, c), (r, c - 1))
            vectorbueno = vector
            print("Esta es la arista buena /de momento")
            # izquierda --> (r,c) > (r-1,c)
        if r + 1 < rows and mapitaPabajo[vector] + mapitaParriba[vector] < mapitaPabajo[v_final]:
            mejorVector = ((r, c), (r - 1, c))
            vectorbueno = vector
            print("Esta es la arista buena /de momento")

    return None, 0, 0

def bf_edge_traverser(graph: IGraph[TVertex], v_initial: TVertex) -> Iterator[TEdge]:

    queue = Fifo()
    seen = set()
    mapitaPabajo[v_initial] = 0
    queue.push((v_initial, v_initial))
    seen.add(v_initial)
    while len(queue) > 0:
        u,v = queue.pop()
        z = mapitaPabajo[v]
        yield u,v, mapitaPabajo[v]
        for suc in graph.succs(v):
            mapitaPabajo[suc] = mapitaPabajo[v] + 1
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)





def sentinel(edges2: IGraph, rows: int, cols: int) -> Optional [TEdge]:


    print(rows,cols)
    print(mapitaPabajo[5,8])
    print(mapitaParriba[5,9])
    print("----------------------")
    mejorArista = ((0, 0), (0, 0)) #---> TEdge = ((1,2),(1,3)) Esto es el resultado si es que es la mejor arista de todas

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
