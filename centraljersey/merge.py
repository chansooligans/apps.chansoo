# %%
if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from centraljersey.load import (
    census, 
    foursquare,
    njdotcom
)
from centraljersey.load import foursquare
import pandas as pd
import glob
import json
from functools import cached_property
import geopandas as gpd

class Merge:

    def __init__(self):
        self.dfcensus = census.Census().nj_data.drop_duplicates(subset="tract_name")
        self.dunkin = foursquare.Foursquare(company="dunkin").df_dunkins
        self.wawa = foursquare.Foursquare(company="wawa").df_wawas
        self.nfl = njdotcom.Njdotcom().nfl
        self.pork = njdotcom.Njdotcom().pork
        self.tracts = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
        self.counties = gpd.read_file("../data/county_boundaries/County_Boundaries_of_NJ.shp")
        self.counties = self.counties.to_crs("EPSG:4269")

    @cached_property
    def df(self):
        # Perform the spatial merge
        merged = gpd.sjoin(
            self.tracts, 
            self.counties, 
            how="inner", 
            op="intersects"
        )
        df = merged.drop_duplicates(subset="TRACTCE")
        return df
