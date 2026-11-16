from pathlib import Path 
import pandas as pd 


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

print("looking into - " , DATA)
print("File Found - " , [p.name for p in DATA.iterdir()])

files = sorted(DATA.glob("accepted*"))
file_path = files[0]
print("Using : " ,  file_path.name)


df = pd.read_csv(file_path , usecols=["loan_status" , "issue_d" , "loan_amnt"] , nrows=200000)

df = df.dropna(subset=["loan_status"])
df["issue_d"] = pd.to_datetime(df["issue_d"] , format="%b-%Y" , errors="coerce")

print(df.shape)
print(df["loan_status"].value_counts())
print(df["issue_d"].min() , df["issue_d"].max())