import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import math
from random import random, randint, shuffle
from statistics import mean

# customers = pd.read_csv('./bikeshops.csv')
# bikes = pd.read_csv('./bikes.csv')
# orders = pd.read_csv('./orders.csv')

# orders = pd.merge(orders, customers, left_on='customer.id', right_on='bikeshop.id')
# orders = pd.merge(orders, bikes, left_on='product.id', right_on='bike.id')

# orders = orders.drop(['customer.id', 'product.id', 'bikeshop.id', 'order.date', 'bike.id', 'order.id', 'order.line', 'longitude', 'latitude'], axis=1)

# orders['price'] = pd.cut(orders['price'], bins=2)

# orders = orders.pivot_table(index=['model', 'category1', 'category2', 'frame', 'price'], columns='bikeshop.name', values='quantity', aggfunc='mean').fillna(0)

# orders.to_csv('pivoted.csv')
# print(orders.head())

def get_cluster_means(N=300, D=2, K=3, X=np.array([]), Y=np.array([])):
    """With Data X and cluster identities Y find the cluster means K"""

    M = np.zeros((K, D))

    if(len(X) == 0):
        # This line says: First generate 100 random two-dimensional data points, assign 0s to every element in every dimension
        # and assign the result to the first 100 data rows (e.g. if the first random two-dimensional data is [3,4545 4,545454]):
        # assign [0,0] to [3,4545 4,545454], which results into [3,4545 4,545454] and assign it to X[0]
        X = np.zeros((N, D))
        X[:100, :] = np.random.randn(100, D) + np.array([0, 0])
        X[100:200, :] = np.random.randn(100, D) + np.array([5, 5])
        X[200:300, :] = np.random.randn(100, D) + np.array([0, 5])

    if(len(Y) == 0):
    # Populate the cluster identities
        Y = np.array([0] * 100 + [1] * 100 + [2] * 100)

    # Assign to every index the mean of all the data points returned by the conditional array indexing
    for k in range(K):
        M[k,:] = X[Y == k].mean(axis=0)

    return M


def get_cluster_ids(*,N=300, D=2, X=[], M=[]):

    """With given data X , cluster means K, find the cluster identities Y"""
    Y=[]
    if(len(M) == 0):
        M = np.array([[0, 0], [5, 5], [0, 5]])
    if(len(X) == 0):
        X = np.zeros((N, D))
        X[:100, :] = np.random.randn(100, D) + M[0]
        X[100:200, :] = np.random.randn(100, D) + M[1]
        X[200:300, :] = np.random.randn(100, D) + M[2]

    for data_point in X:
        min_e_dist = float('inf')
        cluster = None
        for i, mean in enumerate(M):
            euclidean = np.linalg.norm(data_point - mean)
            euclidean_square_root = np.sqrt(((data_point - mean).dot(data_point - mean)))
            # print(f"With numpy.linalg.norm - {euclidean}")
            # print(f"----------With custom impl - {euclidean_square_root}")
            # print(euclidean == euclidean_square_root)
            if min_e_dist > euclidean_square_root:
                min_e_dist = euclidean_square_root
                cluster = i
        Y.append(cluster)
    return np.array(Y)


# Chicken and egg problem
# To find the cluster identities you need the cluster means
# To find the cluster means you have to find the cluster identities
# Which one should be found first?!
# Here helps the initialization phase!
# The initialization phase - assign the cluster centers to chosen data points in X -> THEN
# LOOP:
# --> Assign cluster identities based on current cluster centers (get_cluster_means()) -> THEN
# --> Calculate cluster centers based on cluster identities (get_cluster_ids()) -> THEN
# --> Check for convergence (cluster identities haven't changed)


def k_means_clustering(N=300, D=2, K=3):
    """ Implementation of K-Means clustering algorithm"""

    ## Initial Phase - initialize K random data_points from X to be the clusters centers
    X = np.zeros((N, D))
    X[:100, :] = np.random.randn(100, D) + np.array([0, 0])
    X[100:200, :] = np.random.randn(100, D) + np.array([5, 5])
    X[200:300, :] = np.random.randn(100, D) + np.array([0, 5])
    M = np.zeros((K, D))
    for k in range(K):
        M[k, :] = X[np.random.choice(N)]
    cluster_ids = get_cluster_ids(X=X, M=M)
    new_ids = np.zeros([])
    cluster_means = get_cluster_means(X=X, Y=cluster_ids)
    saved_cluster_ids = [cluster_ids]
    while(np.any(cluster_ids != new_ids)):
        cluster_ids = new_ids
        new_ids = get_cluster_ids(X=X, M=cluster_means)
        cluster_means = get_cluster_means(X=X, Y=new_ids)
        saved_cluster_ids.append([new_ids])
    print(len(saved_cluster_ids))
    fig, ax = plt.subplots(figsize=(5, 5 * len(saved_cluster_ids)))
    for s in range(len(saved_cluster_ids)):
        plt.subplot(len(saved_cluster_ids), 1, s + 1)
        cluster_id_set = saved_cluster_ids[s]
        plt.scatter(X[:, 0], X[:, 1], c=cluster_id_set)
    plt.scatter(X[:, 0], X[:, 1], c=cluster_ids)
    plt.scatter(cluster_means[:, 0], cluster_means[:, 1], s=500, c='red', marker='*')
    plt.show()
k_means_clustering()
