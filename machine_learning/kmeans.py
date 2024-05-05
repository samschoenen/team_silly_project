import os
import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from sklearn.cluster import KMeans

# Load pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Example requests (replace this with your dataset)
current_dir = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(current_dir, '..', 'manual_keyword_selection', 'requests_mapped_to_keywords.csv')
df = pd.read_csv(csv_path)
requests = df['request'].head(100).tolist()  # Convert pandas Series to list of strings

# Tokenize and encode the requests
tokenized_inputs = tokenizer(requests, padding=True, truncation=True, return_tensors='pt')

# Forward pass through BERT model
with torch.no_grad():
    outputs = model(**tokenized_inputs)

# Pooling strategy: Mean pooling
pooled_embeddings = torch.mean(outputs.last_hidden_state, dim=1)

# Convert to numpy array for k-means clustering
pooled_embeddings_np = pooled_embeddings.numpy()

# Perform k-means clustering
kmeans = KMeans(n_clusters=10, random_state=0).fit(pooled_embeddings_np)

# Get cluster assignments
cluster_labels = kmeans.labels_

# Print clusters
for cluster_label, request in zip(cluster_labels, requests):
    print(f"Cluster {cluster_label}: {request}")
