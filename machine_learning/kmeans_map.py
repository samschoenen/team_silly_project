import os
import pandas as pd
from transformers import BertTokenizer
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from ml_BERT import df

# Load pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Sample a subset of the data for processing
sample_df = df.sample(n=500, random_state=42)

# Tokenize the requests
tokenized_inputs = tokenizer(sample_df['request'].tolist(), padding=True, truncation=True, return_tensors='pt')
#tokenized_requests = [tokenizer.tokenize(request.lower()) for request in sample_df['request'].tolist()]


# Perform MiniBatchKMeans clustering on tokenized inputs
kmeans = MiniBatchKMeans(n_clusters=5, random_state=0, batch_size=100).fit(tokenized_inputs['input_ids'])

# Dimensionality reduction using PCA
pca = PCA(n_components=2)
embeddings_2d = pca.fit_transform(tokenized_inputs['input_ids'])

# Get cluster assignments
cluster_labels = kmeans.labels_

# Plot clusters
plt.figure(figsize=(8, 6))
for cluster_id in range(len(np.unique(cluster_labels))):
    cluster_points = embeddings_2d[cluster_labels == cluster_id]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {cluster_id}')

plt.title('Clustered Requests Visualization (500)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.show()

