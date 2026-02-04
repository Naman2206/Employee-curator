import pandas as pd

in_path = "output/employees_clean.csv"
out_path = "output/employees_sample.csv"

# Read cleaned CSV
df = pd.read_csv(in_path)

# Select requested columns and take top 10
cols = ["employee_id", "full_name", "email", "salary", "salary_band", "age", "tenure_years", "department"]
pdf = df[cols].head(10)

print(pdf)

# Write only this subset to output
pdf.to_csv(out_path, index=False)

print(f"Wrote sample to {out_path}")
