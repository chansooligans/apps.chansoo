# %%
if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from centraljersey.load import census
from centraljersey.load import foursquare
from centraljersey import merge

# %%
merger = merge.Merge()

# %%
df = merger.df_tracts
df.fillna(0).to_file("../data/merged_tracts.geojson", driver='GeoJSON')

# %%
df_county = merger.df_counties
df.fillna(0).to_file("../data/merged_tracts.geojson", driver='GeoJSON')

# %%
merger.df_tracts["edu_college"].isnull().sum()

# %%
merger.tracts
# %%
