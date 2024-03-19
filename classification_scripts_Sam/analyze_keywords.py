import pandas as pd
import matplotlib.pyplot as plt

df_keywords = pd.read_csv("word_lists/Keywords.csv", sep=";")

googler = df_keywords["The lazy Googler"].dropna()
creator = df_keywords["The lazy creater"].dropna()
editor = df_keywords["The lazy Editor"].dropna()
other = df_keywords["Other"].dropna()

df_dataset = pd.read_csv("alpaca_data_cleaned.csv")
df_requests_only = pd.DataFrame(columns=["request", "conversation_id", "keyword", "request_type"])

for message, message_id, conversation_id in zip(df_dataset["message"], df_dataset["message_id"], df_dataset["conversation_id"]):
    if message_id == 0:
        for key in ["The lazy Googler", "The lazy creater", "The lazy Editor", "Other"]:
            keyword_sublist = df_keywords[key].dropna()
            for keyword in keyword_sublist:
                if keyword in message:
                    df_requests_only.loc[len(df_requests_only)] = [message, conversation_id, keyword, key]

df_requests_only.to_csv("requests_mapped_to_keywords.csv")