import pandas as pd
import numpy as np
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from utils.plotly_tab_name import Title_Browser


def cluster(data: pd.DataFrame, num_clusters=8) -> (np.ndarray, float,
                                                    float, float):
    '''
    Cluster the data using KMeans clustering algorithm
    :return: (cluster labels, inertia, average distance between clusters,
    silhouette score)
    '''
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(data)
    # Get the cluster labels for each data point
    cluster_labels = kmeans.labels_
    # Get the cluster inertia (sum of squared distances of all points to
    # their nearest centroid)
    clusters_inertia = kmeans.inertia_
    # Get the distances of each sample to all cluster centers
    distances = kmeans.transform(data)
    # Calculate the average distance for each sample
    average_distances = np.mean(distances, axis=1)
    # Calculate the overall average distance between clusters
    avg_distance_between_clusters = float(np.mean(average_distances))
    # Silhouette score
    sil = silhouette_score(data.values, cluster_labels, metric='euclidean')
    return cluster_labels, clusters_inertia, avg_distance_between_clusters, sil


def show_heat_map(df, title="Correlation Heatmap"):
    row_labels = df.index.values
    col_labels = df.columns.values
    heatmap = go.Figure(
        data=go.Heatmap(z=df, x=col_labels,
                        y=row_labels))
    heatmap.update_layout(
        title=title,  # Set the title of the heatmap
        xaxis_title="Feature Index",  # Set the label for the x-axis
        yaxis_title="Feature Index",  # Set the label for the y-axis
    )
    heatmap.show(renderer=Title_Browser, browser_tab_title=title)


def sort_data_by_labels(df: pd.DataFrame, labels) -> pd.DataFrame:
    df.index = [f"{df.index[i]}-{label}"
                for i, label in enumerate(labels)]
    df.columns = [
        f"{df.columns[i]}-{label}" for i, label in
        enumerate(labels)]
    sorted_axis = np.argsort(labels)
    res_df = df.iloc[sorted_axis, sorted_axis]
    return res_df


def cluster_sort_plot(correlation_matrix: pd.DataFrame, k: int):
    labels, inertia, dist, sil = cluster(correlation_matrix, k)
    clustered_corr_matrix = correlation_matrix.copy()
    sorted_df = sort_data_by_labels(clustered_corr_matrix, labels)
    show_heat_map(sorted_df, title=f"Correlation Heatmap K={k} I="
                                   f"{round(inertia, 3)} dist="
                                   f"{round(dist, 3)} sil={round(sil, 3)}")


if __name__ == '__main__':
    # Load data
    data_path = r'IPIP-FFM-data-8Nov2018/data-final.csv'
    df = pd.read_csv(data_path, delimiter='\t')
    # Filter data only
    df = df.iloc[:, :50]
    data = df.values
    # Calculate the correlation matrix
    correlation_matrix = df.corr().abs()
    # Cluster the correlation vectors and show plots
    for k in range(2, 15):
        cluster_sort_plot(correlation_matrix, k)
