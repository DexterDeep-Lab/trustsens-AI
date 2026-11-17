
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# print("File Found - " , [p.name for p in DATA.iterdir()])

src = sorted(DATA.glob("accepted*"))[0]
print("Reading : " , src.name)

# only colums know at the time of loan is issued (no leakeage)
# colums like "total_pymt" , recoveries last_pymnt_d are deliberately not loaded 

COLS = [
    "loan_status", "issue_d", "loan_amnt", "term", "int_rate", "installment",
    "grade", "sub_grade", "emp_length", "home_ownership", "annual_inc",
    "verification_status", "purpose", "addr_state", "dti", "delinq_2yrs",
    "earliest_cr_line", "fico_range_low", "fico_range_high",
    "inq_last_6mths", "open_acc", "pub_rec", "revol_bal", "revol_util",
    "total_acc",
]

# Read the cunks and keep only finished loans , To save memory 

keep = ["Fully Paid" , "Charged Off"]
parts = []

for chunk in pd.read_csv(src , usecols = COLS , chunksize = 500_000 , low_memory = False) :
    parts.append(chunk[chunk["loan_status"].isin(keep)])

df = pd.concat(parts, ignore_index = True)
print("Finished Loan :- " , df.shape)

# Target 1 = Charged Off (Defalut) , 0 = Fully Paid

df["default"] = (df["loan_status"] == "Charged Off").astype(int)
print(df["default"].value_counts())
print(df["loan_status"].unique())
df = df.drop(columns = ["loan_status"])

# Dates and Simple Feature cleaning

df["issue_d"] = pd.to_datetime(df["issue_d"], format="%b-%Y", errors="coerce")
df["issue_year"] = df["issue_d"].dt.year
df["term"] = df["term"].str.extract(r"(\d+)").astype(float)
df["emp_length"] = df["emp_length"].str.extract(r"(\d+)").astype(float)
df.loc[df["emp_length"].isna() , "emp_length" ] = pd.NA
earliest = pd.to_datetime(df["earliest_cr_line"], format="%b-%Y", errors="coerce")
df["credit_age_years"] = (df["issue_d"] - earliest).dt.days / 365.25
df["fico_avg"] = (df["fico_range_low"] + df["fico_range_high"]) / 2
df = df.drop(columns=["earliest_cr_line", "fico_range_low", "fico_range_high"])

# Time-based split
df = df[df["issue_year"] >= 2012].copy()
df["split"] = "train"
df.loc[df["issue_year"] == 2016, "split"] = "calib"
df.loc[df["issue_year"] >= 2017, "split"] = "test"

print("\nLoans and default rate per year:")
print(df.groupby("issue_year")["default"].agg(["count", "mean"]).round(3))
print("\nLoans and default rate per split:")
print(df.groupby("split")["default"].agg(["count", "mean"]).round(3))

out = DATA / "loans_clean.parquet"
df.to_parquet(out, index=False)
print("\nSaved:", out)
