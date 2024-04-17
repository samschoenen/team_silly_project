import pandas as pd
import matplotlib.pyplot as plt

df_dataset = pd.read_csv("alpaca_data_cleaned.csv")
df_requests_only = pd.DataFrame(columns=["request", "conversation_id"])

for message, message_id, conversation_id in zip(df_dataset["message"], df_dataset["message_id"], df_dataset["conversation_id"]):
    if message_id == 0:
        df_requests_only.loc[len(df_requests_only)] = [message, conversation_id]

df_requests_only.to_csv("requests_only.csv")