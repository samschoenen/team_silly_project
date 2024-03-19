import pandas as pd
import matplotlib.pyplot as plt

df_common_words = pd.read_csv("word_lists/used_1000_plus_times.csv")
df_keywords = pd.DataFrame(columns=df_common_words.keys())
not_keywords = []
exception_list = ['that', 'with', 'about','this','from','between','into']
i = 0
for j, (word, count) in  enumerate(zip(df_common_words['words'], df_common_words['counts'])):
    if len(word) < 4:
        not_keywords.append(word)
    elif word in exception_list:
        not_keywords.append(word)
    else:
        df_keywords.loc[i] = df_common_words.loc[j]
        i += 1
not_keywords += exception_list
print(df_keywords)
print(not_keywords)
df_keywords.to_csv("keywords.csv",index=False)