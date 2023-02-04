# %%
if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from centraljersey.load import census
from centraljersey.load import foursquare
from centraljersey import merge
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# %%
merger = merge.Merge()

# %% [markdown]
"""
# Export Geojson
"""

# %%
df_county = merger.df_counties
for col in ["wawa_id", "dunkin_id"]:
    df_county[col] = (df_county[col] / df_county["total_pop"])* 100_000

df_county["giants_or_jets"] = df_county[["nfl_giants","nfl_jets"]].sum(axis=1) / df_county[["nfl_giants","nfl_jets","nfl_eagles"]].sum(axis=1)
df_county["pork_roll"] = df_county["pork_pork_roll"] / df_county[["pork_pork_roll","pork_taylor_ham"]].sum(axis=1)
df_county.fillna(0).to_file("../jerseyproj/static/geojson/merged_counties.geojson", driver='GeoJSON')

# %% [markdown]
"""
# Predictions
"""

# %%
df_tracts_percents = merger.df_tracts_percents
df_tracts = merger.df_tracts

NORTHJERSEY = [
    "Bergen",
    "Union",
    "Essex",
    "Hudson",
    "Morris",
    "Passaic",
    "Sussex",
    "Warren",
]

SOUTHJERSEY = [
    "Atlantic",
    "Burlington",
    "Camden",
    "Cape May",
    "Cumberland",
    "Gloucester",
    "Salem",
]

df_tracts["loc"] = None
df_tracts.loc[df_tracts["county_name"].isin(NORTHJERSEY),"loc"] = "1"
df_tracts.loc[df_tracts["county_name"].isin(SOUTHJERSEY),"loc"] = "0"


# %%
exclude = [
    'STATEFP', 'COUNTYFP', 'TRACTCE', 'GEOID', 'NAME', 'NAMELSAD', 'MTFCC',
    'FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry',
    'county_name','tract_name', 'tract', 'county', 'dunkin_county', 'dunkin_tract',
    'wawa_county','wawa_tract', 'loc',

    'total_pop',"white_pop","pob_total",'native_pop','pob_native','pob_native_jeresy',

    'income_total','income_less_10k', 'income_10k_to_$15k', 'income_15k_to_$25k',
       'income_25k_to_$35k', 'income_35k_to_$50k', 'income_50k_to_$75k',
       'income_75k_to_$100k',  'edu_some_college',
    
    'occu_Arts, entertainment, and recreation, and accommodation and food services',


    'occu_Estimate!!Total:',

]
X = df_tracts.loc[
    df_tracts["loc"].notnull(),
    [x for x in df_tracts.columns if x not in exclude]
].fillna(0)
features = X.columns
y = df_tracts.loc[df_tracts["loc"].notnull(),"loc"]


X_test = df_tracts[[x for x in df_tracts.columns if x not in exclude]].fillna(0)

sc = StandardScaler()
X = sc.fit_transform(X)
X_test = sc.fit_transform(X_test)

# %%
from sklearn.linear_model import LogisticRegression
m = LogisticRegression(random_state=0)
clf = m.fit(X, y)

y_test = clf.predict_proba(X_test)

df_features = pd.DataFrame({
    "feature":features,
    "red=north":np.std(X_test, 0)*m.coef_[0]
})

# %%
df_features.sort_values("red=north").to_csv("../jerseyproj/static/csv/summary.csv", index=False)

# %%
df_tracts_percents["loc"] = y_test[:,1]

# %% [markdown]
"""
# Export
"""
# %%
df_tracts_percents.fillna(0).to_file("../jerseyproj/static/geojson/merged_tracts.geojson", driver='GeoJSON')

# %%
