# %%
if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from centraljersey.load import (
    census,
    foursquare,
    dialects
)
from centraljersey import merge
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import seaborn as sns

# %%
merger = merge.Merge()
df_county = merger.df_counties
df_tracts = merger.df_tracts

# %%

# %% [markdown]
"""
# Export Geojson
"""

# %%
df_county.fillna(0).to_file("../jerseyproj/static/geojson/merged_counties.geojson", driver='GeoJSON')

# %% [markdown]
"""
# Predictions
"""

# %%
df_tracts = df_tracts.merge(
    df_county[[
        "COUNTYFP",'dunkin_id','wawa_id','giants_or_jets','pork_roll','calm-no-l', 
        'almond-no-l', 'forward-no-r', 'drawer', 'gone-don'
    ]],
    how="left",
)

df_tracts.columns
INCLUDE = [
    'dunkin_id','wawa_id','giants_or_jets','pork_roll','calm-no-l', 
    'almond-no-l', 'forward-no-r', 'drawer', 'gone-don',
    'white_pop', 'black_pop', 'asian_pop',

    'occu_Agricul/fish/mining/forest',
    'occu_Construction', 'occu_Manufacturing', 'occu_Wholesale trade',
    'occu_Retail trade', 'occu_transport/warehouse/utils',
    'occu_Information', 'occu_finance/insurance/realestate',
    'occu_administrative', 'occu_educational/healthcare/social',
    'occu_arts/entertainment/foodservices', 'occu_public administration',
    'occu_management, business', 'occu_Service occupations:',
    'occu_Sales and office occupations:',
    'occu_Natural resources, construction',
    'occu_production/transport/materials',

    'income_150k+', "pob_foreign_born", "edu_college"
]

X = df_tracts.loc[
    df_tracts["loc"].notnull(),
    INCLUDE
].fillna(0)
features = X.columns
y = df_tracts.loc[df_tracts["loc"].notnull(),"loc"]
X_test = df_tracts[INCLUDE].fillna(0)

# %%
sc = StandardScaler()
X = sc.fit_transform(X)
X_test = sc.transform(X_test)

m = LogisticRegression(random_state=0)
clf = m.fit(X, y)

# Use cross_val_predict to perform cross-validation
y_pred = cross_val_predict(clf, X, y, cv=5)

# Use cross_val_score to calculate cross-validated performance scores
scores = cross_val_score(clf, X, y, cv=5)
print("Cross-validated scores:", scores)

df_features = pd.DataFrame({
    "feature":features,
    "blue=north":m.coef_[0]
})

y_test = clf.predict_proba(X_test)

# %%
df_features.sort_values("blue=north").to_csv("../jerseyproj/static/csv/summary.csv", index=False)

# %%
df_tracts["loc"] = y_test[:,1]

# %% [markdown]
"""
# Export
"""
# %%
df_tracts.fillna(0).to_file("../jerseyproj/static/geojson/merged_tracts.geojson", driver='GeoJSON')



# %%
