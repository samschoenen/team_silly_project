from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_log_matrix(d):
    for j in range(d.shape[1]):
        for i in range(d.shape[0]):
            if d.iloc[i,j] > 0:
                d.iloc[i,j] = np.log(d.iloc[i,j])
            else:
                d.iloc[i,j] = 0
    return d

def create_0_diagonal_matrix(d):
    for j in range(d.shape[1]):
        for i in range(d.shape[0]):
            if i == j:
                d.iloc[i,j] = 0
    return d

def plot_heatmap(d):
    sns.heatmap(data=d, cmap="Spectral", center=0)
    plt.show()

def plot_sector_full(d, x_start, x_end, y_start, y_end):
    d = d.iloc[x_start:x_end,y_start:y_end]
    plot_heatmap(d)
    dlog = create_log_matrix(d)
    plot_heatmap(dlog)
    d_zero_diagonal = create_0_diagonal_matrix(d)
    plot_heatmap(d_zero_diagonal)
    dlog_zero_diagonal = create_log_matrix(d_zero_diagonal)
    plot_heatmap(dlog_zero_diagonal)

def plot_sector_part(d, x_start, x_end, y_start, y_end):
    d = d.iloc[x_start:x_end,y_start:y_end]
    print(d)
    d_zero_diagonal = create_0_diagonal_matrix(d)
    dlog_zero_diagonal = create_log_matrix(d_zero_diagonal)
    plot_heatmap(dlog_zero_diagonal)

if __name__=="__main__":
    sns.set_theme(style="white")
    d = pd.read_csv("commmonness_matrix.csv",index_col=0)
    sector_borders = np.arange(0, 400, 40)
    for i in range(len(sector_borders)-1):
        for j in range(len(sector_borders)-1):
            print(sector_borders[i], sector_borders[j], sector_borders[i+1], sector_borders[j+1])
            plot_sector_part(d=d, x_start=sector_borders[i], x_end=sector_borders[i+1], y_start=sector_borders[j], y_end=sector_borders[i+1])