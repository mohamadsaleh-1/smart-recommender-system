import pandas as pd
import sqlite3

conn = sqlite3.connect("database/store.db")

users = pd.read_excel("data_new/users.xlsx")
products = pd.read_excel("data_new/products.xlsx")
ratings = pd.read_excel("data_new/ratings.xlsx")
behavior = pd.read_excel("data_new/behavior_15500.xlsx")
ؤ
users.to_sql("users", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
ratings.to_sql("ratings", conn, if_exists="replace", index=False)
behavior.to_sql("behavior", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully")