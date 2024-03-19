import json
import pandas as pd

'''you can laod any json file of your choice with this'''
def get_json_file(filename):
    with open(filename, 'r') as openfile:
        full_network_dict = json.load(openfile)
    return full_network_dict

'''saves a dictionary in a readable format into a json file'''
def save_to_json(dict, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict, f, indent=4)

'''create a dataframe for a keyword'''
def create_keyword_dataframe(keyword, network_dict):
    keyword_dict = get_keyword_dict(keyword,network_dict)
    df = pd.DataFrame(columns=["word", "count"])
    for key in keyword_dict.keys():
        df.loc[len(df.index)] = [key, keyword_dict[key]]  
    return df

'''create a dataframe for a keyword breakdown and saves it as a file'''
def save_to_csv(keyword, network_dict, filename):
    df = create_keyword_dataframe(keyword=keyword, network_dict=network_dict)
    filename = "keyword_breakdown/" + filename
    df.to_csv(filename)

'''use this to extract the dictionary of one keyword of choice.'''
def get_keyword_dict(keyword, keyword_type_network):
    return keyword_type_network[keyword]

'''loading a csv file that you already created'''
def load_csv_file(filename):
    df = pd.read_csv(filename)
    return df

if __name__=="__main__":
    full_dict = get_json_file('keyword_network.json')
    googler_network = full_dict["googler"]
    creator_network = full_dict["creator"]
    editor_network = full_dict["editor"]
    other_network = full_dict["other"]

    #print(json.dumps(get_keyword_dict("write",creator_network), indent=4))
    save_to_csv("what", googler_network, "what.csv")