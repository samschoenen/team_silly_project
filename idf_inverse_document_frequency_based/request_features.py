import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

'''
Loads all the request from the 4 different types of request into its own dataframe and outputs it
'''
def load_words(number_of_words):
    df = pd.read_csv("word_count.csv")
    word_list = df["words"]
    return word_list[:number_of_words]

'''
Loads all the request from the 4 different types of request into its own dataframe and outputs it
'''
def load_request_dataframes(in_file):
    request_df = pd.read_csv(in_file)
    return request_df.iloc[:50000]

'''
n_i_j is the number of occurances of word with index i in request j
tf_i_j is the term frequency of the word with index i in request j
tf_idf_i_j is the term importance weighed by 
'''
def expand_empty_df(df, word_list_length):
    column_names = []
    for i in range(word_list_length):
        column_name_1 = "n_" + str(i) + "_j"
        column_names.append(column_name_1)
        column_name_2 = "tf_" + str(i) + "_j"
        column_names.append(column_name_2)
        column_name_4 = "tf_idf_" + str(i) + "_j"
        column_names.append(column_name_4)
    df2 = pd.DataFrame(columns=column_names)
    df = pd.concat([df, df2], axis=1)
    return df

'''
counts the number of occurances of a term in a request
'''
def count_number_of_occurance_of_term_in_request(term, request):
    bag_of_words = request.split()
    count = 0
    for word in bag_of_words:
        if word == term:
            count += 1
    return count

'''
caluculates the term frequency
'''
def calculate_term_fequency(n_i_j, all_other_n_k_j):
    if np.sum(all_other_n_k_j) > 0:
        tf_i_j = n_i_j/np.sum(all_other_n_k_j)
        return tf_i_j
    else:
        return 0
'''
adds n_i_j and tf_i_j for every word and every column
'''
def fill_out_request_dataframe(df, word_list):
    columns = []
    matrix = np.empty([len(df["request"]), 3*len(word_list)])
    for i in range(len(word_list)):
        column_name_1 = "n_" + str(i) + "_j"
        column_name_2 = "tf_" + str(i) + "_j" 
        column_name_4 = "tf_idf_" + str(i) + "_j"
        columns.append(column_name_1)
        columns.append(column_name_2)
        columns.append(column_name_4)
    for j, request in enumerate(df["request"]):
        all_other_n_k_j = []
        for i, word in enumerate(word_list):
            n_i_j = count_number_of_occurance_of_term_in_request(word, request)
            all_other_n_k_j.append(n_i_j)
            matrix[j,i*3] = n_i_j
        for i, word in enumerate(word_list):
            tf_i_j = calculate_term_fequency(all_other_n_k_j[i], all_other_n_k_j) 
            matrix[j,i*3+1] = tf_i_j
    return columns, matrix

'''
loads dataframe for words, and adds inverse document frequency (idf) for every word
'''
def add_idf_to_word_dataframe(request_matrix, number_of_words):
    df1 = pd.read_csv("word_count.csv")
    df1 = df1.iloc[:number_of_words]
    number_of_requests = request_matrix.shape[0]
    idf_i_list = []
    for i in range(number_of_words):
        number_of_requests_containing_word = 0
        for j in range(request_matrix.shape[0]):
            n_i_j = request_matrix[j, i]
            if n_i_j > 0:
                number_of_requests_containing_word += 1
        if number_of_requests_containing_word > 0:
            idf_i = np.log(number_of_requests/number_of_requests_containing_word)
        else:
            idf_i = 0    
        idf_i_list.append(idf_i)
    column_name_3 = "idf" 
    df2 = pd.DataFrame(idf_i_list, columns=[column_name_3])  
    df = pd.concat([df1, df2],axis=1)  
    return df, idf_i_list

def add_tf_idf_to_request_dataframe(request_matrix, idf_i_list):
    for j in range(request_matrix.shape[0]):
        for i in range(len(idf_i_list)):
            tf_i_j = request_matrix[j,i*2] 
            idf_i = idf_i_list[i]
            tf_idf_i_j = tf_i_j * idf_i
            request_matrix[j, 3*i+2] = tf_idf_i_j
    return request_matrix

def fuse_request_matrix_into_df(request_df, matrix, columns):
    df2 = pd.DataFrame(matrix, columns=columns)
    request_df = pd.concat([request_df, df2],axis=1)
    return request_df

if __name__=="__main__":
    number_of_words = 3000
    #in_file = "requests_only.csv"
    sub = 1
    in_file = "significance/requests_sub4.csv"
    request_df = load_request_dataframes(in_file)
    word_list = load_words(number_of_words)
    print("step 1")
    columns, matrix = fill_out_request_dataframe(request_df, word_list)
    print("step 3")
    word_list_df, idf_i_list = add_idf_to_word_dataframe(request_matrix=matrix, number_of_words=number_of_words)
    print("step 4")
    #matrix = add_tf_idf_to_request_dataframe(matrix, idf_i_list)
    #print("step 5")
    #request_df = fuse_request_matrix_into_df(request_df, matrix, columns)
    #print("step 6")
    #request_file_string = "request_df_"+ str(number_of_words) + "_words.csv"
    #word_list_string = "significance/word_list_df_" + str(number_of_words) +"_words.csv"
    #request_df.to_csv(request_file_string)
    word_list_string = "significance/word_list_df_sub4.csv"
    word_list_df.to_csv(word_list_string)