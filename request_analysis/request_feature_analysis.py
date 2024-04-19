import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

'''
Loads all the request from the 4 different types of request into its own dataframe and outputs it
'''
def load_dataframes():
    df = pd.read_csv("requests_mapped_to_keywords.csv")

    other = df[df["request_type"] == "Other"] 
    googler = df[df["request_type"] == "The lazy Googler"]
    creator = df[df["request_type"] == "The lazy creater"]
    editor = df[df["request_type"] == "The lazy Editor"]

    return other, googler, creator, editor

def average_request_length(df):
    number_of_requests = len(df["request"])
    total_length = 0
    for request in df["request"]:
        total_length += len(request)
    return total_length/number_of_requests
# Gaussian distribution
def request_distribution(df):
    request_lengths = []
    for request in df["request"]:
        request_lengths += [len(request)]
    request_lengths = np.array(request_lengths)
    avg = np.mean(request_lengths)
    var = np.var(request_lengths)
    return avg, var

def plot_standard_distribution(mean, variance):
    sigma = np.sqrt(variance)
    x = np.linspace(mean - 3*sigma, mean + 3*sigma, 100)
    plt.plot(x, norm.pdf(x, mean, sigma))

def request_histogram(df, request_type, plot_number=1):
    request_lengths = []
    for request in df["request"]:
        request_lengths += [len(request)]
    #limit length of the request to 200 characters for the histogram
    request_lengths = np.clip(np.array(request_lengths), 0, 200)
    plt.subplot(2,2,plot_number)
    plt.title(request_type)
    plt.hist(request_lengths,bins=200)

def outlier_histogram(df, request_type, plot_number=1):
    request_lengths = []
    for request in df["request"]:
        request_lengths += [len(request)]
    #limit length of the request to 200 characters for the histogram
    request_lengths = np.clip(np.array(request_lengths), 200, 2000)
    plt.subplot(2,2,plot_number)
    plt.title(request_type)
    plt.hist(request_lengths,bins=1000)

if __name__=="__main__":
    other, googler, creator, editor = load_dataframes()
    print(f'The average request of the other category is {average_request_length(other)}')
    print(f'The average request of the googler category is {average_request_length(googler)}')
    print(f'The average request of the creator category is {average_request_length(creator)}')
    print(f'The average request of the editor category is {average_request_length(editor)}')
    # other_mean, other_variance = request_distribution(other)
    # plot_standard_distribution(other_mean, other_variance)
    # googler_mean, googler_variance = request_distribution(googler)
    # plot_standard_distribution(googler_mean, googler_variance) 
    # creator_mean, creator_variance = request_distribution(creator)
    # plot_standard_distribution(creator_mean, creator_variance)
    # editor_mean, editor_variance = request_distribution(editor)
    # plot_standard_distribution(editor_mean, editor_variance)
    request_histogram(other, "other",1)
    request_histogram(googler, "googler",2)
    request_histogram(creator, "creator",3)
    request_histogram(editor, "editor",4)
    plt.show()
    outlier_histogram(other, "other",1)
    plt.show()