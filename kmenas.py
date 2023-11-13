import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation



def first_centroids(points, n):
    pointCntr = [0, 0]

    for elem in points:
        pointCntr[0] += elem[0]
        pointCntr[1] += elem[1]
    pointCntr[0] /= len(points)
    pointCntr[1] /= len(points)
    R = 0
    for elem in points:
        distCurr = dist(elem, pointCntr)
        if (distCurr > R):
            R = distCurr
    centroids = []
    for i in range(n):
        centroids.append([R * np.cos(2 * np.pi * i / n) + pointCntr[0],
                          R * np.sin(2 * np.pi * i / n) + pointCntr[1]])
    return centroids


def compute_distances(data_point, centroids):
    return np.sqrt(np.sum((centroids - data_point) ** 2, axis=1))


def fit_final(k, X, max_iterations, centroids):
    flag = True
    y = []
    plt.ion()
    images = []
    while flag:
        y = []
        o = 0
        for data_point in X:
            distances = compute_distances(data_point, centroids)
            cluster_num = np.argmin(distances)
            y.append(cluster_num)
        y = np.array(y)
        clusters_indexes = []
        for i in range(k):
            clusters_indexes.append(np.argwhere(y == i))
        cluster_centers = []
        for i, indexes in enumerate(clusters_indexes):
            if len(indexes) == 0:
                cluster_centers.append(centroids[i])
            else:
                cluster_centers.append(np.mean(X[indexes], axis=0)[0])
        if np.max(centroids - np.array(cluster_centers)) < 0.001:
            flag = False
        else:
            centroids = np.array(cluster_centers)
        plt.scatter(X[:, 0], X[:, 1], c=y)
        plt.scatter(centroids[:, 0], centroids[:, 1], c=range(len(centroids)), marker="*", s=200)
        plt.show()
    return y, centroids, clusters_indexes


def fit(k, X, max_iterations, centroids):
    flag = True
    while flag:
        y = []
        for data_point in X:
            distances = compute_distances(data_point, centroids)
            cluster_num = np.argmin(distances)
            y.append(cluster_num)
        y = np.array(y)
        clusters_indexes = []
        for i in range(k):
            clusters_indexes.append(np.argwhere(y == i))
        cluster_centers = []
        for i, indexes in enumerate(clusters_indexes):
            if len(indexes) == 0:
                cluster_centers.append(centroids[i])
            else:
                cluster_centers.append(np.mean(X[indexes], axis=0)[0])
        if np.max(centroids - np.array(cluster_centers)) < 0.001:
            flag = False
        else:
            centroids = np.array(cluster_centers)
    return y, centroids, clusters_indexes


def test_alg(k, points):
    centroids = first_centroids(points, k)
    labels, centroids, indexes = fit_final(k, points, 200, centroids)


def compute_distSumm(cluster_points, centroid):
    distortion = 0
    for x, y in cluster_points:
        distances = [math.sqrt((x - centroid[0]) ** 2 + (y - centroid[1]) ** 2)]
        distortion += sum(distances) ** 2
    return distortion


def get_cluster_points(data, clusters, cluster_number):
    cluster_points = [data[i] for i in range(len(data)) if clusters[i] == cluster_number]
    return cluster_points


def find_optimal_clusters():
    dist = 0
    total_dist = 0
    result = []
    K_range = range(2, 10)
    random_points = np.random.randint(0, 200, (100, 2))
    for k in K_range:
        centroids = first_centroids(random_points, k)
        labels, centroids, indexes = fit(k, random_points, 200, centroids)
        for f in range(0, k - 1):
            cluster_points = get_cluster_points(random_points, labels, f)
            a = compute_distSumm(cluster_points, centroids[f])
            total_dist += a
        print(total_dist)
        result.append(total_dist)
        total_dist = 0
    diff = []
    for i in range(1, len(result)):
        minChange = float('inf')
        val = result[i - 1] / result[i]
        if result[i] < minChange:
            if (result[i - 1] / result[i] > 1.0 and result[i - 1] / result[i] < 1.3):
                minChange = i
    print(minChange + 1)

    plt.plot(K_range, result, 'bx-')
    plt.xlabel('Clusters (k)')
    plt.ylabel('Cумма квадратов расстояний')
    plt.title('Different k')
    plt.show()
    test_alg(k, random_points)


if __name__ == "__main__":
    find_optimal_clusters()
