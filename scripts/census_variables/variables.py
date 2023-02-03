# %%
import requests
import pandas as pd

# %% [markdown]
"""
# Occupation by Industry
"""

# %%
df = pd.read_html("https://api.census.gov/data/2019/acs/acs5/groups/C24050.html")[0]

df = df.loc[
    df["Label"].str.contains("Estimate!!Total") &
    ~df["Label"].str.contains("Annotation")
].copy()

df["Label"] = "occu_"+df["Label"].str.split("Estimate!!Total:!!").str[-1]
df = df.loc[~df["Label"].str.contains(":!!")].copy()

df["Label"]
{x:y for x,y in df[["Name","Label"]].values}


# %%
