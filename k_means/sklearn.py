import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import seaborn as sns
from sklearn import preprocessing, cluster
import json


# Implementation of K-means clustering using RFM profile of a customer
def RFM(data :list, cache_data):
    invoices = pd.DataFrame(data)
    cache = pd.DataFrame(cache_data)

    pd.set_option('display.expand_frame_repr', False)
    # print(invoices)
    # customer_count = len(orders.groupby('customer.id'))
    #
    # orders = orders.drop(columns='order.line', axis=0)
    # print(orders)
    invoices['date'] = invoices['date'].apply(pd.to_datetime)
    invoices['date'] = invoices['date'].dt.date


    rec_end = max(invoices['date']) + timedelta(days=1)
    # print(rec_end)
    rfm_df = invoices.groupby('customer_id').agg({
        # Get the days between the last and forlast purchase
        'date': lambda x: (rec_end - max(x)).days,
        'id': 'count',
        'value': 'sum',
    })
    #
    rfm_df.columns = ['Recency', 'Frequency', 'Monetary']

    # fig, axes = plt.subplots(1, 3, figsize=(20, 5))
    # for i, feature in enumerate(list(rfm_df.columns)):
    #     sns.histplot(rfm_df[feature], ax=axes[i])
    # plt.show()

    scaler = preprocessing.MinMaxScaler()
    rfm_normalized = pd.DataFrame(scaler.fit_transform(rfm_df))
    rfm_normalized.columns = ['n_Recency', 'n_Frequency', 'n_Monetary']

    # Sum of squared distances between centroids and each member of cluster
    # SSE = []
    # for k in range(10):
    #     kmeans = cluster.KMeans(n_clusters=k + 1, init='k-means++').fit(rfm_normalized)
    #     # print(kmeans)
    #     SSE.append(kmeans.inertia_)
    # sns.pointplot(x=list(range(1, 11)), y=SSE)
    # plt.show()

    model = cluster.KMeans(n_clusters=4, init='k-means++').fit(rfm_normalized)

    # ## 3D scatter plot
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(rfm_normalized['n_Recency'], rfm_normalized['n_Frequency'], rfm_normalized['n_Monetary'], cmap="brg", c = model.predict(rfm_normalized))
    # centers = model.cluster_centers_
    # ax.scatter(centers[:, 0], centers[:, 1], marker="*", s=500, c='red')
    # plt.show()

    rfm_ = pd.DataFrame(scaler.inverse_transform(rfm_normalized))
    rfm_.columns = rfm_df.columns
    rfm_['Customer ID'] = rfm_df.index
    rfm_['Cluster'] = model.labels_
    # #
    # rfm_.sort_values(by='Recency', inplace=True)
    # rfm_.sort_values(by=['Frequency', 'Monetary'], inplace=True, ascending=False)
    #

    t_cache = pd.DataFrame()
    t_cache['Customer ID'] = rfm_['Customer ID']
    t_cache['Cluster ID'] = rfm_['Cluster']

    clusters = rfm_.groupby(['Cluster']).agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Customer ID': 'count'
    })

    analyzed_data = {}

    analyzed_data['cluster_data'] = clusters.rename(columns={"Customer ID": "Volume"}).T
    analyzed_data['customer_data'] = t_cache
    return analyzed_data


    # rfm = np.zeros((customer_count, 3))
    # customer_monitory = list(orders.groupby(['customer.id']).agg({
    #     "quantity": 'sum',
    # })['quantity'])
    # customer_recency = np.zeros(customer_count)
    # customer_frequency = np.zeros(customer_count)
    #
    # customer_orders = orders.groupby(['customer.id'])['order.id'].apply(set)
    # print(customer_monitory)
    #
    # for idx, o in enumerate(customer_orders):
    #     customer_frequency[idx] = len(o)
    #
    # customer_purchase_dates = orders.groupby(['customer.id'])['order.date'].apply(set)
    #
    # for idx, dates in enumerate(customer_purchase_dates):
    #     if len(dates) <= 1:
    #         customer_recency[idx] = 0
    #     dates_list = pd.to_datetime(list(dates)).sort_values()
    #     last_p, before_last_p = dates_list[0], dates_list[1]
    #     days_diff = abs((last_p - before_last_p).days)
    #     customer_recency[idx] = days_diff
    #
    # for k in range(customer_count):
    #     rfm[k, 0] = customer_recency[k]
    #     rfm[k, 1] = customer_frequency[k]
    #     rfm[k, 2] = customer_monitory[k]
    # print(rfm[0])


# Customer implementation of K-means clustering
def plot_k_means(X, K, max_iter=20):
    N, D = X.shape
    M = np.zeros((K, D))
    R = np.zeros((N, K))

    for k in range(K):
        M[k] = X[np.random.choice(N)]

    costs = np.zeros(max_iter)
    cluster_ids = np.zeros(N)
    for i in range(max_iter):
        print("Iteration---", i)
        old_cluster_ids = cluster_ids.copy()
        min_dists = np.zeros(N)
        for x in range(N):
            min_distance = float('inf')
            cluster_id = -1

            for k in range(K):
                # Calculate euclidean distance
                d = np.sqrt(((X[x] - M[k]).dot(X[x] - M[k])))
                if (d < min_distance):
                    min_distance = d
                    cluster_id = k
            min_dists[x] = min_distance
            cluster_ids[x] = cluster_id

        costs[i] = min_dists.sum()

        for k in range(K):
            M[k] = X[cluster_ids == k].mean(axis=0)

        if np.all(old_cluster_ids == cluster_ids):
            break
    plt.subplots(2, 1)
    plt.subplot(2, 1, 2)
    plt.plot(costs)
    plt.title('Cost per iteration')
    plt.ylabel('Costs')
    plt.xlabel('Iterations')

    plt.subplot(2, 1, 1)
    plt.scatter(X[:, 0], X[:, 1], c=cluster_ids)
    plt.scatter(M[:, 0], M[:, 1], s=500, c='red', marker='*')
    plt.show()
    ## Retrieve


def main():
    D = 2
    s = 4
    mu1 = np.array([0, 0])
    mu2 = np.array([s, s])
    mu3 = np.array([0, s])

    N = 900
    X = np.zeros((N, D))
    X[:300, :] = np.random.randn(300, D) + mu1
    X[300:600, :] = np.random.randn(300, D) + mu2
    X[600:900, :] = np.random.randn(300, D) + mu3

    plt.scatter(X[:, 0], X[:, 1])
    plt.show()

    K = 3
    plot_k_means(X, K)
    K = 5
    plot_k_means(X, K, max_iter=30)
    K = 5
    plot_k_means(X, K, max_iter=30)
