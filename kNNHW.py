import networkx as nx
from itertools import cycle
from math import hypot
from numpy import random
import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
import random
from sklearn.linear_model import LogisticRegression



def normalize(test_sample, main_sample, test_vector, main_vector):
    iris = load_iris()

    best_k = 0
    best_accuracy = 0

    for k in range(1, 20):
        knn_model = KNeighborsClassifier(n_neighbors=k)
        knn_model.fit(main_sample, main_vector)

        y_pred = knn_model.predict(test_sample)

        accuracy = accuracy_score(test_vector, y_pred)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_k = k

    knn_model = KNeighborsClassifier(n_neighbors=best_k)
    knn_model.fit(main_sample, main_vector)
    sepalLengthCm = input()
    sepalWidthCm = input()
    petalLengthCm = input()
    petalWidthCm = input()
    arr = [[float(sepalLengthCm), float(sepalWidthCm), float(petalLengthCm), float(petalWidthCm)]]
    prediction = knn_model.predict(arr)
    answer = ""
    if prediction[0] == 0:
        answer = "setosa"
    if prediction[0] == 1:
        answer = "versicolor"
    if prediction[0] == 2:
        answer = "virginica"

    print(f"Оптимальное количество соседей (k): {best_k}")
    print('Ожидаемый класс: ' + answer)
    return best_k

def normalize_data(data):

    means = data.mean(axis=0)
    stds = data.std(axis=0)

    normalized_data = (data - means) / stds


    return normalized_data

def draw_plot_normalized(dataset, target):

    setosa_indices = target == 0
    versicolor_indices = target == 1
    virginica_indices = target == 2


    setosa_features = dataset[setosa_indices]
    versicolor_features = dataset[versicolor_indices]
    virginica_features = dataset[virginica_indices]

    fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(15, 10))

    feature_names = iris.feature_names
    newArr = []
    for i in range(3):
        j = i + 1

        while j <= 3:
            axes[i][j - 1].scatter(setosa_features[:, i], setosa_features[:, j], label='Setosa')
            axes[i][j - 1].scatter(versicolor_features[:, i], versicolor_features[:, j], label='Versicolor')
            axes[i][j - 1].scatter(virginica_features[:, i], virginica_features[:, j], label='Virginica')

            axes[i][j - 1].set_xlabel(feature_names[i])
            axes[i][j - 1].set_ylabel(feature_names[j])
            axes[i][j - 1].legend()
            j += 1
            newArr.append(axes[i][j-1])
    axes[1][0].scatter(setosa_features[:, 2], setosa_features[:, 3], label='Setosa')
    axes[1][0].scatter(versicolor_features[:, 2], versicolor_features[:, 3], label='Versicolor')
    axes[1][0].scatter(virginica_features[:, 2], virginica_features[:, 3], label='Virginica')

    axes[1][0].set_xlabel(feature_names[2])
    axes[1][0].set_ylabel(feature_names[2])
    axes[1][0].legend()
    fig.delaxes(axes[0][3])
    fig.delaxes(axes[2][2])
    fig.delaxes(axes[1][3])
    fig.delaxes(axes[2][0])
    fig.delaxes(axes[2][1])
    fig.delaxes(axes[2][3])
    fig.delaxes(axes[3][0])
    fig.delaxes(axes[3][1])
    fig.delaxes(axes[3][2])
    fig.delaxes(axes[3][3])
    # plt.tight_layout()
    plt.show()


def draw_plot5(dataset):
    iris = dataset
    X = iris.data
    y = iris.target

    setosa_indices = y == 0
    versicolor_indices = y == 1
    virginica_indices = y == 2

    setosa_features = X[setosa_indices]
    versicolor_features = X[versicolor_indices]
    virginica_features = X[virginica_indices]


    fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(15, 10))

    feature_names = iris.feature_names
    newArr = []
    for i in range(3):
        j = i + 1

        while j <= 3:
            axes[i][j - 1].scatter(setosa_features[:, i], setosa_features[:, j], label='Setosa')
            axes[i][j - 1].scatter(versicolor_features[:, i], versicolor_features[:, j], label='Versicolor')
            axes[i][j - 1].scatter(virginica_features[:, i], virginica_features[:, j], label='Virginica')

            axes[i][j - 1].set_xlabel(feature_names[i])
            axes[i][j - 1].set_ylabel(feature_names[j])
            axes[i][j - 1].legend()
            j += 1
            newArr.append(axes[i][j-1])
    axes[1][0].scatter(setosa_features[:, 2], setosa_features[:, 3], label='Setosa')
    axes[1][0].scatter(versicolor_features[:, 2], versicolor_features[:, 3], label='Versicolor')
    axes[1][0].scatter(virginica_features[:, 2], virginica_features[:, 3], label='Virginica')

    axes[1][0].set_xlabel(feature_names[2])
    axes[1][0].set_ylabel(feature_names[2])
    axes[1][0].legend()
    fig.delaxes(axes[0][3])
    fig.delaxes(axes[2][2])
    fig.delaxes(axes[1][3])
    fig.delaxes(axes[2][0])
    fig.delaxes(axes[2][1])
    fig.delaxes(axes[2][3])
    fig.delaxes(axes[3][0])
    fig.delaxes(axes[3][1])
    fig.delaxes(axes[3][2])
    fig.delaxes(axes[3][3])
    # plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    iris = load_iris()
    n = 100
    x = []
    y = []
    for i in range(n):
        x.append([random.randint(10,100),random.randint(10,100)])
        y.append(random.randint(0,1))
    model = LogisticRegression()
    model.fit(x,y)
    x0 = [25,89]
    model.predict([x0])


    # print(iris['data'])
    train_sample = []
    test_sample = []
    test_sample_vector = []
    train_sample_vector = []
    for i in range(len(iris['data'])):
        if i in (45,46,47,48,49,95,96,97,98,99,145,146,147,148,149):
            test_sample.append(iris['data'][i])
            test_sample_vector.append(iris.target[i])
        else:
            train_sample.append(iris['data'][i])
            train_sample_vector.append(iris.target[i])
    print('Hello')
    draw_plot5(iris)
    normalized = normalize_data(iris.data)
    draw_plot_normalized(normalized, iris.target)
    best_k = normalize(test_sample, train_sample, test_sample_vector, train_sample_vector)
    sepalLengthCm = input()
    sepalWidthCm = input()
    petalLengthCm = input()
    petalWidthCm = input()