# %%
import yaml
from pathlib import Path

def setup():
    with open(
        Path(__file__).resolve().parent.parent.joinpath("secrets.yaml"), "r"
    ) as file:
        secrets = yaml.load(file, Loader=yaml.FullLoader)
    return secrets