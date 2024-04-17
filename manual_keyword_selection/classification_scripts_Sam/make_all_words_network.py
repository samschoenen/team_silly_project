import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
'''
Run this file from the top of the repo directory for the loading of the files to work correctly
'''


'''
Loads all the request from the 4 different types of request into its own dataframe and outputs it
'''
def load_words():
    df = pd.read_csv("word_count.csv")
    word_list = df["words"]
    return word_list

'''
Loads all the request from the 4 different types of request into its own dataframe and outputs it
'''
def load_request_dataframes():
    request_df = pd.read_csv("requests_only.csv")
    return request_df


def initialize_network_dicts(keywords):
    keys = list(keywords)
    network_dict = {}
    for key in keys:
        #for every keyword category we have a dict
        #for every keyword we have a  dict
        #these dicts are of the structure {"word": 1} counting the occurances of one word in relation to the keyword
        network_dict[key] = {}
    return network_dict


def fill_keyword_network(request_dataframe, keyword_network_dict):        
    for key in keyword_network_dict.keys():
        for request in request_dataframe["request"]:
            #splitting string into list of word strings
            bag_of_words = request.split()
            if key in bag_of_words:
                # preexising words is a string of the keys from the constructed dict of the keyword
                # the dict has the structure {"the": 2,"word": 1}
                preexisting_words = keyword_network_dict[key].keys()
                for word in bag_of_words:
                    if word in preexisting_words:
                        keyword_network_dict[key][word] =  keyword_network_dict[key][word] + 1
                    else:
                        keyword_network_dict[key][word] = 1
    return keyword_network_dict

def save_to_json(network_dict):
    with open('full_word_network.json', 'w', encoding='utf-8') as f:
        json.dump(network_dict, f, indent=4)

if __name__=="__main__":
    word_list = load_words()
    word_network = initialize_network_dicts(word_list)
    request_df = load_request_dataframes()
    word_network = fill_keyword_network(request_dataframe=request_df, keyword_network_dict=word_network)
    save_to_json(word_network)