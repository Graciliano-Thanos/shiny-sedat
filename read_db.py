import pandas as pd
from pathlib import Path

def find_db(path:str):
    infile = Path(__file__).parent / "database" / f"{path}.csv"
    
    db = pd.read_csv(infile,low_memory=False)
    filters = ["Country","Location","Capacity","Technology","Plant type" if path == "global_desal" else "Plant_type"]

    return db, filters
