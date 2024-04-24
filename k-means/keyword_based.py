import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load your data into a pandas DataFrame
data = pd.read_csv('your_data.csv')

# Preprocess the text data


# Extract features using TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['text'])

# Apply k-means clustering
k = 3  # Number of clusters
kmeans = KMeans(n_clusters=k)
kmeans.fit(X)

# Get the cluster labels for each data point
labels = kmeans.labels_

# Print the cluster labels
for i, label in enumerate(labels):
    print(f"Data point {i+1} belongs to cluster {label+1}")