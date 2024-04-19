import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("word_count.csv")
thresholds = [1000, 500, 100, 50, 10, 1]
threshold_counts = [0,0,0,0,0,0]


for i, threshold in enumerate(thresholds):
    threshold_count = 0
    for word, count in zip(df['words'], df['counts']):
        if count >= threshold:
            if i == 0 or count < thresholds[i-1]:
                threshold_count += 1
    threshold_counts[i] = threshold_count

print(threshold_counts)
df_used_1000_plus_times = df.loc[:threshold_counts[0]-1,:] #words used more than 1000 times
df_used_1000_plus_times.to_csv("word_lists/used_1000_plus_times.csv", index=False)
df_used_500_to_1000_times = df.loc[threshold_counts[0]:threshold_counts[1]-1,:] #words used more than 500 times
df_used_500_to_1000_times.to_csv("word_lists/used_500_to_1000_times.csv", index=False)
df_used_100_to_500_times = df.loc[threshold_counts[1]:threshold_counts[2]-1,:] #words used more than 100 times
df_used_100_to_500_times.to_csv("word_lists/used_100_to_500_times.csv", index=False)
df_used_50_to_100_times = df.loc[threshold_counts[2]:threshold_counts[3]-1,:] #words used more than 50 times
df_used_50_to_100_times.to_csv("word_lists/used_50_to_100_times.csv", index=False)
df_used_10_to_50_times = df.loc[threshold_counts[3]:threshold_counts[4]-1,:] #words used more than 10 times
df_used_10_to_50_times.to_csv("word_lists/used_10_to_50_times.csv", index=False)
df_used_1_to_10_times = df.loc[threshold_counts[4]:,:] #words used less than 10 times
df_used_1_to_10_times.to_csv("word_lists/used_1_to_10_times.csv", index=False)