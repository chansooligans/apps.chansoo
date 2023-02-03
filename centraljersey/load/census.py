# %%
import censusdata
from functools import cached_property
from centraljersey import cache

VARIABLES = { 
    'B02001_001E':'total_pop', 
    'B02001_002E':'white_pop', 
    'B02001_003E':'black_pop', 
    'B02001_004E':'native_pop',
    'B02001_005E':'asian_pop',
    'B05002_001E':'pob_total',
    'B05002_003E':'pob_native_jeresy',
    'B05002_002E':'pob_native',
    'B05002_013E':'pob_foreign_born',
    'B06009_001E':'edu_total',
    'B06009_002E':'edu_less_than_hs',
    'B06009_003E':'edu_hs_degree',
    'B06009_004E':'edu_some_college',
    'B06009_005E':'edu_college',
    'B06009_006E':'edu_grad_degree',
    'C16001_002E':'lang_only_english',
    'B19001_001E':'income_total',
    'B19001_002E':'income_less_10k',
    'B19001_003E':'income_10k_to_$15k',
    'B19001_004E':'income_15k_to_$25k',
    'B19001_005E':'income_25k_to_$35k',
    'B19001_006E':'income_35k_to_$50k',
    'B19001_007E':'income_50k_to_$75k',
    'B19001_008E':'income_75k_to_$100k',
    'B19001_009E':'income_100k_to_$150k',
    'B19001_010E':'income_150k_to_$200k',
    'B19001_011E':'income_200k_to_more',
    'C24050_001E': 'occu_Estimate!!Total:',
    'C24050_002E': 'occu_Agriculture, forestry, fishing and hunting, and mining',
    'C24050_003E': 'occu_Construction',
    'C24050_004E': 'occu_Manufacturing',
    'C24050_005E': 'occu_Wholesale trade',
    'C24050_006E': 'occu_Retail trade',
    'C24050_007E': 'occu_Transportation and warehousing, and utilities',
    'C24050_008E': 'occu_Information',
    'C24050_009E': 'occu_Finance and insurance, and real estate, and rental and leasing',
    'C24050_010E': 'occu_Professional, scientific, and management, and administrative, and waste management services',
    'C24050_011E': 'occu_Educational services, and health care and social assistance',
    'C24050_012E': 'occu_Arts, entertainment, and recreation, and accommodation and food services',
    'C24050_013E': 'occu_Other services, except public administration',
    'C24050_014E': 'occu_Public administration',
    'C24050_015E': 'occu_Management, business, science, and arts occupations:',
    'C24050_029E': 'occu_Service occupations:',
    'C24050_043E': 'occu_Sales and office occupations:',
    'C24050_057E': 'occu_Natural resources, construction, and maintenance occupations:',
    'C24050_071E': 'occu_Production, transportation, and material moving occupations:'
}

class Census:

    def get_tract(self, s):
        return [x.params()[2][1] for x in s.values]

    def get_county(self, s):
        return [x.params()[1][1] for x in s.values]

    @cached_property
    @cache.localcache(dtype={"tract":str,"county":str})
    def nj_data(self):
        
        df = censusdata.download(
            'acs5', 2019, 
            censusdata.censusgeo([('state', '34'), ('county', '*'), ('tract', '*')]), 
            list(VARIABLES.keys())
        ).rename(VARIABLES, axis=1)

        df = (
            df
            .clip(lower=0)
            .reset_index()
            .rename({"index":"tract_name"}, axis=1)
        )

        df["tract"] = self.get_tract(df["tract_name"])
        df["county"] = self.get_county(df["tract_name"])
        return df

# nj_data.to_csv(f"../data/censustracts.csv", index=False)
