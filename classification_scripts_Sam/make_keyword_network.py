import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

'''
Loads all the request from the 4 different types of request into its own dataframe and outputs it
'''
def load_request_dataframes():
    df = pd.read_csv("requests_mapped_to_keywords.csv")

    googler = df[df["request_type"] == "The lazy Googler"]
    creator = df[df["request_type"] == "The lazy creater"]
    editor = df[df["request_type"] == "The lazy Editor"]
    other = df[df["request_type"] == "Other"] 

    return other, googler, creator, editor

def load_keywords():
    df_keywords = pd.read_csv("word_lists/Keywords.csv", sep=";")

    googler_keywords = df_keywords["The lazy Googler"].dropna()
    creator_keywords = df_keywords["The lazy creater"].dropna()
    editor_keywords = df_keywords["The lazy Editor"].dropna()
    other_keywords = df_keywords["Other"].dropna()

    return googler_keywords, creator_keywords, editor_keywords, other_keywords

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
        for keyword, request in zip(request_dataframe["keyword"], request_dataframe["request"]):
            if keyword == key:
                #splitting string into list of word strings
                bag_of_words = request.split()
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
    with open('keyword_network.json', 'w', encoding='utf-8') as f:
        json.dump(network_dict, f, indent=4)

if __name__=="__main__":
    other, googler, creator, editor = load_request_dataframes()
    googler_keywords, creator_keywords, editor_keywords, other_keywords = load_keywords()
    googler_network = initialize_network_dicts(googler_keywords)
    googler_network = fill_keyword_network(request_dataframe=googler, keyword_network_dict=googler_network)
    
    creator_network = initialize_network_dicts(creator_keywords)
    creator_network = fill_keyword_network(request_dataframe=creator, keyword_network_dict=creator_network)
    editor_network = initialize_network_dicts(editor_keywords)
    editor_network = fill_keyword_network(request_dataframe=editor, keyword_network_dict=editor_network)
    other_network = initialize_network_dicts(other_keywords)
    other_network = fill_keyword_network(request_dataframe=googler, keyword_network_dict=other_network)
    big_keyword_network = {"googler": googler_network, "creator": creator_network, "editor": editor_network, "other": other_network}
    save_to_json(big_keyword_network)