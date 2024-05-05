import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

word_counts = pd.read_csv("word_count.csv")
#word_counts = word_counts.sort_values("counts", ascending=True)
list1 = list(word_counts["counts"])[:3000]
list2 = list(word_counts["counts"])[:-50]
print(len(list1))
print(len(list2))
print(word_counts.iloc[14384])
#x = 10**np.random.uniform(size=1000)
plt.title("How often do words appear in this dataset?")
plt.ylabel("Number of words that occur n times (log scale)")
plt.xlabel("Number of occurances n (log scale)")
plt.xscale("log")
plt.yscale("log")
plt.hist(list1, bins=10**np.linspace(0, 1, 10), color="Fuchsia")
#plt.hist(list1, bins=300, color="Fuchsia")
plt.xlim((word_counts.iloc[3000]["counts"],word_counts.iloc[0]["counts"]))
#count_list = range(1001)
plt.axvline(x = 13, color = 'forestgreen', label = 'lower threshold for analysis')
plt.axvline(x = 605, color = 'forestgreen', label = 'upper threshold for analysis')
# count_counting = list(np.zeros(1001))
# for count in# word_counts["counts"]:
#     if count >= 1000:
#         break
#     count_counting[count] += 1
# xaxis = count_list = range(0,1001)
#plt.bar(xaxis, count_counting, color='Fuchsia')
plt.show()