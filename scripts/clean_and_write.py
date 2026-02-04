import pandas as pd
from datetime import datetime


in_path = "data/input/employees_raw.csv"
out_path = "output/employees_clean.csv"

# Read
df = pd.read_csv(in_path, dtype=str)

# Drop duplicate employee_id, keep first
df = df.drop_duplicates(subset=["employee_id"], keep="first")

# Fill missing values for address fields and status
df["address"] = df["address"].fillna("")
df["city"] = df["city"].fillna("")
df["state"] = df["state"].fillna("")
df["zip_code"] = df["zip_code"].fillna("")
df["status"] = df["status"].fillna("Active")

# Normalize names
df["first_name"] = df["first_name"].str.title()
df["last_name"] = df["last_name"].str.title()

# Full name
df["full_name"] = df["first_name"].fillna("") + " " + df["last_name"].fillna("")

# Normalize email to lowercase
df["email"] = df["email"].astype(str).str.strip().str.lower()
df["email_domain"] = df["email"].str.extract(r"@(.+)$", expand=False).fillna("")

# Clean salary: remove $ and commas, convert to float
df["salary"] = df["salary"].astype(str).str.replace(r"[\$,]", "", regex=True)
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

# Parse dates
df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce").dt.date
df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce").dt.date

# Remove future hire dates
today = datetime.utcnow().date()
df = df[df["hire_date"].isna() | (df["hire_date"] <= today)]

# Age calculation
def calc_age(birth):
    if pd.isna(birth):
        return None
    delta = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        delta -= 1
    return delta

df["age"] = df["birth_date"].apply(calc_age)

# Tenure in years
df["tenure_years"] = ((pd.to_datetime(today) - pd.to_datetime(df["hire_date"])) / pd.Timedelta(days=365.25))
df["tenure_years"] = df["tenure_years"].round(1)

# Salary bands
def salary_band(sal):
    if pd.isna(sal):
        return "Unknown"
    if sal < 50000:
        return "Junior"
    if sal < 80000:
        return "Mid"
    return "Senior"

df["salary_band"] = df["salary"].apply(salary_band)

# Timestamps
ts = datetime.now().isoformat()
df["created_at"] = ts
df["updated_at"] = ts

# Select and reorder columns similar to notebook
final_cols = [
    "employee_id", "first_name", "last_name", "full_name", "email", "email_domain",
    "hire_date", "job_title", "department", "salary", "salary_band", "manager_id",
    "address", "city", "state", "zip_code", "birth_date", "age", "tenure_years",
    "status", "created_at", "updated_at"
]

out = df.reindex(columns=final_cols)

# Write CSV
out.to_csv(out_path, index=False)

print(f"Wrote cleaned data to {out_path} with {len(out)} rows")
