import pandas as pd

# dtype=str means "read everything as text, don't guess".
# We want to see the file exactly as it is before we trust it.
raw = pd.read_csv("data/id_list.csv", dtype=str)

print("shape:", raw.shape)               # (rows, columns)
print("columns:", raw.columns.tolist())  # what is the column called?
print(raw.head(10))
print("blank cells:", raw.isna().sum().sum())