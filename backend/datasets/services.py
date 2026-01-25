import pandas as pd
import hashlib

REQUIRED_COLUMNS=[
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature",
]

def analyze_csv(file_path):
    df=pd.read_csv(file_path)

    #Validating columns
    missing=set(REQUIRED_COLUMNS)-set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    
    for col in ["Flowrate","Pressure","Temperature"]:
        df[col]=pd.to_numeric(df[col],errors="coerce")

    valid_df=df.dropna(subset=["Flowrate","Pressure","Temperature"])

    if valid_df.empty:
        raise ValueError("No valid data row found")
    
    summary={
        "total_equipment":int(len(df)),
                "valid_rows": int(len(valid_df)),
        "average_flowrate": float(valid_df["Flowrate"].mean()),
        "average_pressure": float(valid_df["Pressure"].mean()),
        "average_temperature": float(valid_df["Temperature"].mean()),
        "equipment_type_distribution": (
            valid_df["Type"].value_counts().to_dict()
        ),
    }

    return summary

def compute_file_checksum(file_path):
    sha256=hashlib.sha256()
    with open (file_path,"rb") as f:
        for chunk in iter(lambda: f.read(8192),b""):
            sha256.update(chunk)
        return sha256.hexdigest()
    