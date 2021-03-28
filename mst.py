#!/usr/bin/env python3

# Kruskal's algorithm. Aiming for implementation simplicity, rather than efficiency.

import random

def read_instance(path):
    """Reads a TSPLIB-formatted TSP instance (not tour) file. """
    coordinates = []
    with open(path, "r") as f:
        for line in f:
            if "NODE_COORD_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "EOF" in line or not line:
                break
            fields = line.strip().split()
            coordinates.append((float(fields[1]), float(fields[2])))
    return coordinates

def read_tour(path):
    """Reads a TSPLIB-formatted TSP tour file. """
    tour = []
    with open(path, "r") as f:
        for line in f:
            if "TOUR_SECTION" in line:
                break
        for line in f:
            line = line.strip()
            if "-1" in line or "EOF" in line or not line:
                break
            fields = line.strip().split()
            tour.append((int(fields[0])))
    return tour

def distance(instance, i, j):
    """instance is a list of points. each point is a pair of coordinates x, y.
    i and j identify points in the list as indices.
    """
    ix = instance[i][0]
    iy = instance[i][1]
    jx = instance[j][0]
    jy = instance[j][1]
    dx = jx - ix
    dy = jy - iy
    return round((dx ** 2 + dy ** 2) ** 0.5)

def make_edge(instance, i, j):
    """instance is a list of points. each point is a pair of coordinates x, y.
    i and j identify points in the list as indices.
    returns tuple of cost + random integer (to get random ordering of same-cost edges) and i, j in normalized order.
    """
    return ((distance(instance, i, j), random.randint(0, len(instance))), min(i, j), max(i, j))

def make_sorted_edges(instance):
    """instance is a list of points. each point is a pair of coordinates x, y.
    returns all possible edges sorted by cost. complexity is at least O(n**2 * log(n**2))
    """
    edges = []
    for i in range(len(instance)):
        for j in range(i + 1, len(instance)):
            edges.append(make_edge(instance, i, j))
    edges.sort()
    return edges

def mst(instance):
    """Returns MST for given instance.
    """
    sorted_edges = make_sorted_edges(instance)
    sets = []
    edges = []
    for e in sorted_edges:
        # determine which edge sets this new edge belongs to.
        found = []
        cyclic = False
        for i in range(len(sets)):
            if e[1] in sets[i] and e[2] in sets[i]:
                cyclic = True
                break
            elif e[1] in sets[i] or e[2] in sets[i]:
                found.append(i)
        if cyclic:
            continue
        assert(len(found) <= 2)

        # create new set, add to existing, or merge 2 existing.
        if len(found) == 0:
            sets.append(set())
            sets[-1].add(e[1])
            sets[-1].add(e[2])
        elif len(found) == 1:
            sets[found[0]].add(e[1])
            sets[found[0]].add(e[2])
        elif len(found) == 2:
            sets[found[0]].update(sets[found[1]])
            sets.pop(found[1])
        edges.append(e)

        # end if all points included.
        if len(edges) == len(instance):
            break

    # check result.
    check = set()
    for e in edges:
        check.add(e[1])
        check.add(e[2])
    assert(len(check) == len(instance))

    return edges

from matplotlib import pyplot as plt

def plot_edges(instance, edges, color='b'):
    for e in edges:
        p1 = instance[e[1]]
        p2 = instance[e[2]]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], f"{color}x-")

def plot_tour(instance, tour):
    x = []
    y = []
    for i in tour:
        p = instance[i - 1]
        x.append(p[0])
        y.append(p[1])
    plt.plot(x, y, "rx:")

def plot_diff(instance, tour, mst_edges):
    tour_edges = set()
    prev = tour[-1]
    for i in tour:
        tour_edges.add((min(i - 1, prev - 1), max(i - 1, prev - 1)))
        prev = i
    mst_edges_ = set()
    for e in mst_edges:
        mst_edges_.add((e[1], e[2]))
    adds = set()
    for e in mst_edges_:
        if e not in tour_edges:
            adds.add(e)
    dels = set()
    for e in tour_edges:
        if e not in mst_edges_:
            dels.add(e)

    for e in adds:
        p1 = instance[e[0]]
        p2 = instance[e[1]]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], f"rx-")
    for e in dels:
        p1 = instance[e[0]]
        p2 = instance[e[1]]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], f"rx:")


import sys

if __name__ == "__main__":
    instance_file = sys.argv[1]
    tour_file = sys.argv[2]

    instance = read_instance(instance_file)
    tour = read_tour(tour_file)

    edges = mst(instance)
    total = sum([x[0][0] for x in edges])
    print(f'total cost: {total}')

    #plot_edges(instance, edges)
    #plot_tour(instance, tour)

    plot_diff(instance, tour, edges)

    plt.axis('square')
    plt.show()

