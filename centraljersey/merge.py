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
        self.dunkin = foursquare.Foursquare(company="dunkin")
        self.wawa = foursquare.Foursquare(company="wawa")
        self.nfl = njdotcom.Njdotcom().nfl
        self.pork = njdotcom.Njdotcom().pork
        self.tracts = gpd.read_file("../data/tl_2018_34_tract/tl_2018_34_tract.shp")
        self.counties = gpd.read_file("../data/county_boundaries/County_Boundaries_of_NJ.shp")
        self.counties = self.counties.to_crs("EPSG:4269")

    @cached_property
    def df_tracts(self):
        # Perform the spatial merge
        
        df = self.tracts.merge(
            self.census, 
            how='left', 
            left_on = ["COUNTYFP","TRACTCE"], 
            right_on=["county","tract"]
        )

        df = df.merge(
            self.dunkin.df_dunkins_tract, 
            how="left", 
            left_on=["COUNTYFP","TRACTCE"],
            right_on=["dunkin_county", "dunkin_tract"]
        )

        df = df.merge(
            self.wawa.df_wawa_tract, 
            how="left", 
            left_on=["COUNTYFP","TRACTCE"],
            right_on=["wawa_county", "wawa_tract"]
        )

        return df

    @cached_property
    def df_counties(self):

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
                x:sum for x in self.census.columns 
                if x not in ["tract_name","tract","county"]
                })
            .reset_index()
        )
        df = df.merge(
            census_county, how='left', left_on = "COUNTYFP", right_on="county")

        df = df.merge(
            self.dunkin.df_dunkins_county, 
            how="left", 
            left_on="COUNTYFP",
            right_on="dunkin_county"
        )

        df = df.merge(
            self.wawa.df_wawa_county, 
            how="left", 
            left_on="COUNTYFP",
            right_on="wawa_county"
        )

        return df