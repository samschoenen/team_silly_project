import pandas as pd

def create_0_diagonal_matrix(d):
    for j in range(d.shape[1]):
        for i in range(d.shape[0]):
            if i == j:
                d.iloc[i,j] = 0
    return d

def return_common_pair_df(d, threshold):
    df = pd.DataFrame(columns=["word1","word2"])
    columns = list(d.keys())
    rows = d.index.values.tolist()
    for j in range(d.shape[1]):
        for i in range(d.shape[0]):
            if i == j:
                break
            if d.iloc[i,j] > threshold:
                df.loc[len(df.index)] = [rows[i], columns[j]]
             
    return df

if __name__=="__main__":
    d = pd.read_csv("commmonness_matrix.csv",index_col=0)
    d = create_0_diagonal_matrix(d)
    threshold = 20
    common_pairs = return_common_pair_df(d, threshold)
    print(common_pairs.size)
    print(common_pairs)
    filename = "common_pairs_min_" + str(threshold) + "_common_appearances.csv"
    common_pairs.to_csv(filename)