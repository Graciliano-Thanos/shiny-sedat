import pandas as pd
from pathlib import Path

def find_db(path:str):
    infile = Path(__file__).parent / "database" / f"{path}.csv"
    return pd.read_csv(infile,low_memory=False)
    