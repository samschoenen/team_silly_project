import numpy as np
import pandas as pd

def load_dataframe(filename):
    df = pd.read_csv(filename)
    return df

def reduce_to_interesting_requests(common_pairs, requests_df):
    df = pd.DataFrame(columns=["request","conversation_id","word1","word2"])
    for request, conv_id in zip(requests_df["request"], requests_df["conversation_id"]):
        bag_of_words = request.split()
        for word1, word2 in zip(common_pairs["word1"], common_pairs["word2"]):
            if word1 in bag_of_words and word2 in bag_of_words:
                df.loc[len(df.index)] = [request, conv_id, word1, word2]
    return df

def calculate_term_fequency(n_i_j, all_other_n_k_j):
    if np.sum(all_other_n_k_j) > 0:
        tf_i_j = n_i_j/np.sum(all_other_n_k_j)
        return tf_i_j
    else:
        return 0

def extract_new_features(request_df, word_list_df):
    df = pd.DataFrame(columns=["request","conversation_id","word1","word2","word1_idf","word2_idf", "number_of_characters", "number_of_words", 
        "avg_word_length", "number_of_unique_words","avg_tf", "average_idf", "average_tf_idf"])
    for i, request in enumerate(request_df["request"]):
        conv_id, word1, word2 =  request_df["conversation_id"][i], request_df["word1"][i], request_df["word2"][i]
        number_of_characters = len(request)
        bag_of_words = request.split()
        number_of_words = len(bag_of_words)
        avg_word_length = number_of_characters/number_of_words
        unique_words = []
        unique_word_count = []
        for word in bag_of_words:
            if word not in unique_words:
                unique_words.append(word)
                unique_word_count.append(1)
            else:
                for i, (un_word, count) in enumerate(zip(unique_words, unique_word_count)):
                    if un_word == word:
                        unique_word_count[i] = count + 1
        number_of_unique_words = len(unique_words)
        unique_words_tf = []
        for i, word in enumerate(unique_words):
            unique_words_tf.append(calculate_term_fequency(unique_word_count[i], unique_word_count))
        average_tf = np.sum(np.array(unique_words_tf))/number_of_unique_words
        all_idf_values = []
        all_tf_idf = []
        word1_idf = 0
        word2_idf = 0
        for word, idf in zip(word_list_df["words"], word_list_df["idf_2999"]):
            if word == word1:
                word1_idf = idf
            elif word == word2:
                word2_idf = idf
            for i, un_word in enumerate(unique_words):
                if word == un_word:
                    all_idf_values.append(idf)
                    all_tf_idf.append(unique_words_tf[i] * idf)
        average_idf = np.mean(np.array(all_idf_values))
        average_tf_idf = np.mean(np.array(all_tf_idf))
        
        df.loc[len(df.index)] = [request, conv_id,word1, word2, word1_idf, word2_idf, number_of_characters, number_of_words, avg_word_length, 
                    number_of_unique_words, average_tf, average_idf, average_tf_idf]
    return df


if __name__=="__main__":
    threshold = 20
    common_pairs_filename = "idf_inverse_document_frequency_based/common_pairs_min_" + str(threshold) + "_common_appearances2.csv"
    common_pairs = load_dataframe(common_pairs_filename)
    requests_filename = "request_analysis/requests_only.csv"
    requests_df = load_dataframe(requests_filename)
    reduced_request_df = reduce_to_interesting_requests(common_pairs=common_pairs, requests_df=requests_df)
    word_list_filename = "idf_inverse_document_frequency_based/word_list_df_expanded.csv"
    word_list_df = load_dataframe(word_list_filename)
    #reduced_request_df = extract_new_features(reduced_request_df, word_list_df)
    #print(reduced_request_df.size)
    reduced_request_df = reduced_request_df.sort_values("word1", axis=0)
    reduced_request_df.to_csv("request_analysis/requests_with_features_simplified.csv")