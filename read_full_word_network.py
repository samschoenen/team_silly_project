import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

'''you can laod any json file of your choice with this'''
def get_json_file(filename):
    with open(filename, 'r') as openfile:
        full_network_dict = json.load(openfile)
    return full_network_dict



'''use this to extract the dictionary of one keyword of choice.'''
def get_keyword_dict(keyword, word_network):
    return word_network[keyword]

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

'''loading a csv file that you already created'''
def load_csv_file(filename):
    filename = "keyword_breakdown/" + filename
    df = pd.read_csv(filename)
    return df

'''saves a dictionary in a readable format into a json file'''
def save_to_json(dict, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict, f, indent=4)

def make_horizontal_barplot(filename):
    sns.set_theme()
    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    # Load the example car crash dataset
    df = load_csv_file(filename).sort_values("count", ascending=False)
    df = df.loc[1:16]

    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="count", y="word", data=df,
                label="Number of uses", color="b")

    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 100), ylabel="",
        xlabel="Number of times used")
    sns.despine(left=True, bottom=True)
    plt.title(filename[:-4])
    plt.show()

if __name__=="__main__":
    full_dict = get_json_file('full_word_network.json')
    word_list = list(full_dict.keys())
    listofzeros = [0] * len(word_list)
    #word_network_matrix = pd.DataFrame({"words": word_list})
    #for word in word_list:
    #    word_network_matrix[word] = listofzeros
    #    for i, word_suggestion in enumerate(word_network_matrix["words"]):
    #        if word_suggestion in full_dict[word].keys():
    #            word_network_matrix[word].loc[i] = full_dict[word][word_suggestion]
    #word_network_matrix.to_csv("word_occurance_matrix.csv")
    word_occurance_matrix = pd.read_csv("word_occurance_matrix.csv")
    word_occurance_matrix["words"] = word_list
    word_occurance_matrix.to_csv("word_occurance_matrix.csv")
    #save_to_csv("what", full_dict, "what.csv")
    #make_horizontal_barplot("what.csv")