import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def find_db(path:str):
    infile = Path(__file__).parent / f"{path}.csv"
    
    db = pd.read_csv(infile,low_memory=False)
    filters = ["Size","Technology","Plant type" if path == "Global" else "Plant_type"]

    return db, filters

def info_from_db(*args):
    return "text teste."


def give_loc(db:pd.DataFrame,db_type:str):
    return db["Location"].value_counts()



def plot_capacity(db:pd.DataFrame,db_type:str):
    
    cap = db["Capacity"if db_type=="Global" else "Capacity__"]

    return plt.hist(db.value_counts("Capacity" if db_type=="Global" else "Capacity__"),label="Capacity")