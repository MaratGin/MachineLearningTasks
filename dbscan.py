import sys

import numpy as np
import numpy.linalg.linalg
import pygame
import random
from itertools import cycle
from math import hypot
from numpy import random
import matplotlib.pyplot as plt

eps = 100
def dbscan_naive(P, eps, m):
    NOISE = 0
    cur_cluster = 0

    visited_points = set()
    clustered_points = set()
    clusters = {NOISE: []}

    def find_neighbours(q):
        neighbourss = []
        for p in P:
            if distance(p, q) < eps:
                neighbourss.append(p)
        return neighbourss
    def distance(p1, p2):
        return numpy.linalg.linalg.norm(np.array(p1) - np.array(p2))

    def expand_cluster(p, neighbours):
        if cur_cluster not in clusters:
            clusters[cur_cluster] = []
        clusters[cur_cluster].append(p)
        clustered_points.add(p)
        while neighbours:
            q = neighbours.pop()
            if q not in visited_points:
                visited_points.add(q)
                neighbours1 = find_neighbours(q)
                print(neighbours1)
                if len(neighbours1) > m:
                    neighbours.extend(neighbours1)
            if q not in clustered_points:
                clustered_points.add(q)
                clusters[cur_cluster].append(q)
                if q in clusters[0]:
                    clusters[0].remove(q)

    for p in P:
        if p in visited_points:
            continue
        visited_points.add(p)
        neighbours = find_neighbours(p)
        if len(neighbours) < m:
            clusters[0].append(p)
        else:
            cur_cluster += 1
            expand_cluster(p, neighbours)

    return clusters

def assign_flags(points):
    visited_points = set()
    clustered_points = set()
    green_flagged = set()
    yellow_flagged = set()
    red_flagged = set()
    def distance(p1, p2):
        return numpy.linalg.linalg.norm(np.array(p1) - np.array(p2))
    def region_query(p):
        count = 0
        for q in points:
            if 0 < distance(p,q) < eps:
                count += 1
        return count
        # return [q for q in points if distance(p, q) < eps]
    NOISE = 0
    C = 0
    m = 3
    clusters = {NOISE: []}

    for point in points:
        if point in visited_points:
            continue
        visited_points.add(point)
        neighbours = region_query(point)
        print(neighbours)
        if m > neighbours > 0:
            clusters[0].append(point)
            yellow_flagged.add(point)
        elif neighbours == 0:
            red_flagged.add(point)
        else:
            green_flagged.add(point)
    return green_flagged, yellow_flagged, red_flagged


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
    screen.fill(color='#FFFFFF')
    pygame.display.update()
    points = []
    flag = True
    drawing = False
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(event)
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                print("pressed mousebutton")
            pygame.display.update()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == 13:
                    # screen.fill(color='#000000')
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False
                print("pressed mousebutton")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # screen.fill(color='#123456')
                    green, yellow, red = assign_flags(points)
                    for p in red:
                        pygame.draw.circle(screen, color='red', center= p, radius=10)
                    for p in yellow:
                        pygame.draw.circle(screen, color='yellow', center=p, radius=10)
                    for p in green:
                        pygame.draw.circle(screen, color='green', center= p, radius=10)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    clusters = dbscan_naive(points, eps, 3)
                    print('----------')
                    print(clusters)
                    cluster = 0
                    print(clusters[0])
                    for i in range(len(clusters)):
                        print(i)
                        color = [(random.random() * 100) * (cluster + 1) % 256,
                                 (random.random() * 200) * (cluster + 1) % 256,
                                 (random.random() * 300) * (cluster + 1) % 256]
                        for y in clusters[i]:
                            print(y)
                            if cluster == 0:
                                pygame.draw.circle(screen, color='red', center=y, radius=10)
                            else:
                                pygame.draw.circle(screen, color=color, center=y, radius=10)
                        cluster += 1
            pygame.display.update()
        if drawing:
            pygame.time.delay(100)
            coord = pygame.mouse.get_pos()
            pygame.draw.circle(screen, color='black', center=pygame.mouse.get_pos(), radius=10)
            points.append(coord)
            # print("points - ", points)
    pygame.quit()
    sys.exit()