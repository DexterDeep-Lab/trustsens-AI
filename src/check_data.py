from pathlib import Path 
import pandas as pd 


ROOT = Path(__file__).resolve().parent.parent   # Path converts the path into obj / .reslove() - return the exact location / .parent - moves one directory up again .parent moves 2 direcotry up
DATA = ROOT / "data"                            # 

print("looking into - " , DATA)
print("File Found - " , [p.name for p in DATA.iterdir()])   # DATA.iterdir() Returns all files and folders inside the data directory.

files = sorted(DATA.glob("accepted*"))          # .glob searches inside the directory who's name atarts with accepted
file_path = files[0]                            # Sorts the matching file paths alphabetically and soring the name in variable
print("Using : " ,  file_path.name)


df = pd.read_csv(file_path , usecols=["loan_status" , "issue_d" , "loan_amnt"])

df = df.dropna(subset=["loan_status"])          # dropna() removes rows containing missing values.
df["issue_d"] = pd.to_datetime(df["issue_d"] , format="%b-%Y" , errors="coerce")

print(df.shape)
print(df["loan_status"].value_counts())
print(df["issue_d"].min() , df["issue_d"].max())