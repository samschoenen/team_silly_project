import os
import pandas as pd
from gensim.models import Word2Vec


# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))
# Specify the path to data.csv relative to the current directory
csv_path = os.path.join(current_dir, '..', 'request_analysis', 'requests_only.csv')
# Read the CSV file
df = pd.read_csv(csv_path)

if df.empty:
    print("Data is null")

model = Word2Vec(df[1], seed=1)
model.wv['Caesar']

