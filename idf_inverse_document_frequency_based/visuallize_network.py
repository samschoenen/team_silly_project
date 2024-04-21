from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

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

def plot_heatmap(d,filename="oops.png"):
    plt.clf()
    sns.heatmap(data=d, cmap="Spectral", center=0)
    plt.title(filename[:-4])
    plt.savefig(filename)
    plt.close()

def plot_sector_full(d, x_start, x_end, y_start, y_end):
    d = d.iloc[x_start:x_end,y_start:y_end]
    plot_heatmap(d)
    dlog = create_log_matrix(d)
    plot_heatmap(dlog)
    d_zero_diagonal = create_0_diagonal_matrix(d)
    plot_heatmap(d_zero_diagonal)
    dlog_zero_diagonal = create_log_matrix(d_zero_diagonal)
    plot_heatmap(dlog_zero_diagonal)

def plot_sector_part(d, x_start, x_end, y_start, y_end,filename):
    d = d.iloc[x_start:x_end,y_start:y_end]
    d_zero_diagonal = create_0_diagonal_matrix(d)
    dlog_zero_diagonal = create_log_matrix(d_zero_diagonal)
    plot_heatmap(dlog_zero_diagonal,filename=filename)

def get_correlated_word_list():
    df = pd.read_csv("highly_correlated_words.csv")
    word_list_1 = list(df["word1"])
    word_list_2 = list(df["word2"])
    
    combined_word_list = []
    for word in word_list_1:
        if word not in combined_word_list:
            combined_word_list.append(word)
    for word in word_list_2:
        if word not in combined_word_list:
            combined_word_list.append(word)
    return word_list_1, word_list_2, combined_word_list

def make_graph(word_list1, word_list2, combined_word_list):
    nxG = nx.Graph()
    #pos = nx.spring_layout(nxG, k=0.15, iterations=20)
    for word in combined_word_list:
        nxG.add_node(word)
    for word1, word2 in zip(word_list1, word_list2):
        nxG.add_edge(word1, word2)
    nx.draw(nxG, with_labels=True, font_size=10, width=0.4,node_color='lightblue', node_size=400)
    plt.show()

if __name__=="__main__":
    # sns.set_theme(style="white")
    # d = pd.read_csv("commmonness_matrix.csv",index_col=0)
    # sector_borders = np.arange(0, 400, 20)
    # for i in range(len(sector_borders)-1):
    #     for j in range(len(sector_borders)-1):
    #         filename = "visualisations/commonness_matrix_" + "x_from_" + str(sector_borders[i]) + "_to_" + str(sector_borders[i+1])+ "_y_from_" + str(sector_borders[j]) +"_to_" +  str(sector_borders[j+1]) + ".png"
    #         plot_sector_part(d=d, x_start=sector_borders[i], x_end=sector_borders[i+1], y_start=sector_borders[j], y_end=sector_borders[j+1],filename=filename)
    word_list_1, word_list_2, combined_word_list = get_correlated_word_list()
    make_graph(word_list_1, word_list_2, combined_word_list)