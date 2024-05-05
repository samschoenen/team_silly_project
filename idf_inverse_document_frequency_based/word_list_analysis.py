import numpy as np
import pandas as pd

idf_threshold = 3
number_of_words = 3000
#filename = "idf_inverse_document_frequency_based/word_list_df_expanded.csv" #+ str(number_of_words) + "_words.csv"
filename = "significance/word_list_df_sub4.csv"
word_list_df = pd.read_csv(filename)

high_value_words = []
for word, idf in zip(word_list_df["words"], word_list_df["idf"]):
    if idf > idf_threshold:
        high_value_words.append([word, idf])

high_value_words = np.array(high_value_words)
df = pd.DataFrame(high_value_words, columns=["words","idf"])
df.idf = pd.to_numeric(df.idf, errors='coerce')
df = df.sort_values('idf', ascending = False)
print(df)
out_file = "high_value_words_sub4.csv"
df.to_csv(out_file)