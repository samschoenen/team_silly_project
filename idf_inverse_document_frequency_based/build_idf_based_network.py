import pandas as pd
import numpy as np

def get_idf_value(high_value_words, term):
    for word, idf in zip(high_value_words["words"], high_value_words["idf"]):
        if word == term:
            return idf
    return 0

def step1():
    high_value_words = pd.read_csv("high_value_words.csv")
    request_df = pd.read_csv("requests_only.csv")
    request_df = request_df.iloc[:]

    high_value_requests = []
    for request, conversation_id in zip(request_df["request"], request_df["conversation_id"]):
        bag_of_words = request.split()
        for term in list(high_value_words["words"]):
            if term in bag_of_words:
                high_value_requests.append([request, conversation_id,term, get_idf_value(high_value_words, term)])
    high_value_requests = np.array(high_value_requests)
    high_value_requests_df = pd.DataFrame(high_value_requests, columns=["request","conversation_id","high_idf_word","idf of word"])
    print(high_value_requests_df.shape)
    filename = "high_idf_request_df.csv"
    high_value_requests_df.to_csv(filename)
    return filename, high_value_requests_df, list(high_value_words["words"])

def create_empty_commonness_matrix(high_value_word_list):
    arr = np.zeros((len(high_value_word_list), len(high_value_word_list)))
    df = pd.DataFrame(arr, index=high_value_word_list, columns=high_value_word_list)
    df.to_csv("temp.csv")
    return df

def fill_out_commonness_matrix(commonness_matrix, high_idf_requests_df):
    for conv_id, high_idf_word in zip(high_idf_requests_df["conversation_id"], high_idf_requests_df["high_idf_word"]):
        sub_request_df = high_idf_requests_df.loc[high_idf_requests_df['conversation_id'] == conv_id,:]
        for sub_high_idf_word in sub_request_df["high_idf_word"]:
            commonness_matrix.loc[high_idf_word, sub_high_idf_word] = commonness_matrix.loc[high_idf_word, sub_high_idf_word] + 1
    return commonness_matrix

if __name__=="__main__":
    filename, high_idf_requests_df, high_value_word_list = step1()
    commonness_matrix = create_empty_commonness_matrix(high_value_word_list)
    commonness_matrix = fill_out_commonness_matrix(commonness_matrix, high_idf_requests_df)
    commonness_matrix.to_csv("commmonness_matrix.csv")