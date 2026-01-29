import pandas as pd

REQUIRED_COLUMNS = [
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature",
]

def analyze_csv(file_path):
    df = pd.read_csv(file_path)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    for col in ["Flowrate", "Pressure", "Temperature"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    valid_df = df.dropna(subset=["Flowrate", "Pressure", "Temperature"])
    if valid_df.empty:
        raise ValueError("No valid rows found")

    summary = {
        "total": len(df),
        "avg_flowrate": valid_df["Flowrate"].mean(),
        "avg_pressure": valid_df["Pressure"].mean(),
        "avg_temperature": valid_df["Temperature"].mean(),
        "distribution": valid_df["Type"].value_counts().to_dict(),
    }

    return summary
