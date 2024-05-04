from collections import Counter
#import kmeans_map
from kmeans_map import sample_df, tokenizer, cluster_labels
import numpy as np

# Define a list of words to skip
skip_words = ['the', 'of', 'and', 'following', 'to', 'in', 'a', 'for', 'on', 'or', 'an', 'that', 'with', 'is', '.', ':', "'", '-', ',', '[PAD]', '[CLS]', '[SEP]', '"']

# Get the tokenized requests
tokenized_requests = tokenizer(sample_df['request'].tolist(), padding=True, truncation=True, return_tensors='pt')['input_ids']

# Create a dictionary to store word frequencies for each cluster
cluster_word_freq = {cluster_id: Counter() for cluster_id in np.unique(cluster_labels)}

# Update word frequencies for each cluster
for i, (tokens, cluster_id) in enumerate(zip(tokenized_requests, cluster_labels)):
    token_list = tokenizer.convert_ids_to_tokens(tokens.numpy().tolist())
    # Filter out the words in the skip_words list
    filtered_tokens = [token for token in token_list if token not in skip_words]
    cluster_word_freq[cluster_id].update(filtered_tokens)

# Print the 15 most used words per cluster
for cluster_id, word_freq in cluster_word_freq.items():
    print(f"Cluster {cluster_id} Most Used Words (Excluding Skip Words):")
    print(word_freq.most_common(15))  # Print top 15 most common words