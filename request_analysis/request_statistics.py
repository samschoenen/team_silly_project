import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

common_pairs = pd.read_csv("common_pairs_modified.csv")
catagories = list(set(list(common_pairs["category"])))
category_counts = list(np.zeros(len(catagories)))

category_df = pd.DataFrame({'category': catagories, 'counts': category_counts})
requests_df = pd.read_csv("request_analysis/requests_with_features_simplified.csv")

for r_word1, r_word2 in zip(requests_df["word1"], requests_df["word2"]):
    for word1, word2, cat in zip(common_pairs["word1"], common_pairs["word2"], common_pairs["category"]):
        if word1 in [r_word1, r_word2] or word2 in [r_word1, r_word2]:
            for i, (categ, count) in enumerate(zip(category_df["category"], category_df["counts"])):
                if categ == cat:
                    category_df.iloc[i,1] = count + 1

category_df = category_df.sort_values(by="counts", ascending=True)
print(category_df)

x = category_df["category"].to_list()
y = category_df["counts"].to_list()
# y_pos = np.arange(len(x))
# plt.yticks(y_pos, x)
# sns.barplot(category_df, y="category", x="counts")
plt.figure(figsize=(12, 5))
plt.barh(range(len(x)), y, color='magenta')
y_pos = np.arange(len(x))
plt.yticks(y_pos, x)
plt.title('Use Case Count', size=16)
plt.ylabel('Use Cases')
plt.xlabel('Count')
plt.tight_layout()
plt.savefig("use_cases.png")