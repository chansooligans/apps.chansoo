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
        self.census = census.Census().nj_data.drop_duplicates(subset="tract_name")
        self.dunkin = foursquare.Foursquare(company="dunkin").df_dunkins
        self.wawa = foursquare.Foursquare(company="wawa").df_wawas
        self.nfl = njdotcom.Njdotcom().nfl
        self.pork = njdotcom.Njdotcom().pork
        self.tracts = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
        self.counties = gpd.read_file("../data/county_boundaries/County_Boundaries_of_NJ.shp")
        self.counties = self.counties.to_crs("EPSG:4269")

    @cached_property
    def tracts(self):
        # Perform the spatial merge
        merged = gpd.sjoin(
            self.tracts, 
            self.counties, 
            how="inner", 
            op="intersects"
        )
        df = merged.drop_duplicates(subset="TRACTCE")
        df = df.merge(self.nfl).merge(self.pork)
        df = df.merge(self.census, how='left', left_on = "TRACTCE", right_on="tract")
        # df.fillna(0).to_file("../data/merged_tracts.geojson", driver='GeoJSON')

        return df

    @cached_property
    def counties(self):

        merged = gpd.sjoin(self.counties, self.tracts, how="inner", op="intersects")
        df = merged.drop_duplicates(subset="TRACTCE")
        df = df[["COUNTY","COUNTYFP","geometry"]].drop_duplicates()
        df = df.merge(self.nfl).merge(self.pork)
        for col in self.census.columns:
            if col not in ["tract_name","tract","county"]:
                self.census[col] = self.census[col].astype(float)
        census_county = (
            self.census
            .groupby("county")
            .agg({
                x:sum for x in census.columns 
                if x not in ["tract_name","tract","county"]
                })
            .reset_index()
        )
        df = df.merge(
            census_county, how='left', left_on = "COUNTYFP", right_on="county")

        df = df.merge(
            self.df_dunkins, 
            how="left", 
            left_on="COUNTYFP",
            right_on="dunkin_county"
        )

        df = df.merge(
            self.df_wawas, 
            how="left", 
            left_on="COUNTYFP",
            right_on="wawa_county"
        )

        return df