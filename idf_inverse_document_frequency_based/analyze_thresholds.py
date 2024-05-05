import pandas as pd
import matplotlib.pyplot as plt

def count_above_and_below_threshold(threshold, df, column_name):
    above = 0
    below = 0
    equal = 0
    for number in df[column_name]:
        if number > threshold:
            above += 1
        elif number < threshold:
            below += 1
        else:
            equal += 1
    return above, below, equal

def create_0_diagonal_matrix(d):
    for j in range(d.shape[1]):
        for i in range(d.shape[0]):
            if i == j:
                d.iloc[i,j] = 0
    return d

def return_threshold_data_commonness_matrix(d, threshold):
    above = 0
    below = 0
    df = pd.DataFrame(columns=["word1","word2"])
    columns = list(d.keys())
    rows = d.index.values.tolist()
    for j in range(d.shape[1]):
        for i in range(d.shape[0]):
            if i == j:
                break
            if d.iloc[i,j] > threshold:
                df.loc[len(df.index)] = [rows[i], columns[j]]
                above += 1
            else:
                below += 1
             
    return above, below

def return_equal_threshold_data_commonness_matrix(d, threshold):
    equal = 0
    for j in range(d.shape[1]):
        for i in range(d.shape[0]):
            if i == j:
                break
            if d.iloc[i,j] == threshold:
                equal += 1 
    return equal

def find_word_pair(d, word1, word2):
    columns = list(d.keys())
    rows = d.index.values.tolist()
    for j, col in enumerate(columns):
        if word1 == col:
            for i, row in enumerate(rows):
                if word2 == row:
                    return d.iloc[i,j]
    return 0

#idf list
if __name__=="__main__":
    print("----------idf threshold---------")
    threshold_idf = 9
    #df1 = pd.read_csv("idf_inverse_document_frequency_based/word_list_df_expanded.csv")
    #above, below, equal = count_above_and_below_threshold(threshold_idf, df1, "idf_2999")
    #print("%d words have a higher idf" % above)
    #print("%d words have a lower idf" % below)
    #plt.title("idf distribution")
    #plt.hist(list(df1["idf_2999"]), bins=100)
    #plt.show()
    print("----------commonness matrix---------")
    d = pd.read_csv("commmonness_matrix2.csv",index_col=0)
    d = create_0_diagonal_matrix(d)
    #print("start counting for graph")
    xaxis = range(0,31)
    yasix = [0, 69516, 11699, 5206, 1962, 1117, 588, 372, 286, 204, 139, 100, 85, 86, 62, 50, 29, 29, 15, 26, 13, 8, 10, 9, 11, 10, 9, 5, 4, 7, 4] 
    xvalues = range(1,31)
    #for threshold in range(20,31):
    #    equal = return_equal_threshold_data_commonness_matrix(d, threshold)
    #    yasix.append(equal)
    #print(yasix)
    plt.title("Number of connections between pairs of words")
    plt.yscale("log")
    plt.ylabel("Number of Words")
    plt.xlabel("Number of connections")
    plt.xticks(xvalues)
    plt.bar(xaxis, yasix, color='Fuchsia')
    plt.show()
    threshold = 10
    #above, below = return_threshold_data_commonness_matrix(d, threshold)
    #print("%d word pairs are a common pair with threshold %d" % (above, threshold))
    #print("%d word pairs not a common pair with threshold %d" % (below, threshold))
    #print(find_word_pair(d, "zoo", "zoo"))