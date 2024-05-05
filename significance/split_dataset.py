import pandas as pd
request_df = pd.read_csv("request_analysis/requests_only.csv")
out_file = "significance/requests_sub4.csv"
df = request_df.sample(n=4000)
df.to_csv(out_file, index=False)