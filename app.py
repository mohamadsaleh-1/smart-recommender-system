from flask import Flask, render_template
import sqlite3
from algorithm.genetic_algorithm import run_ga

app = Flask(__name__)

def get_products_by_ids(ids):

    conn = sqlite3.connect("database/store.db")
    cur = conn.cursor()

    placeholders = ",".join("?" * len(ids))

    query = f"""
    SELECT *
    FROM products
    WHERE product_id IN ({placeholders})
    """

    cur.execute(query, ids)

    products = cur.fetchall()

    conn.close()

    return products


@app.route("/")
def home():

    conn = sqlite3.connect("database/store.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM products")

    products = cur.fetchall()

    conn.close()

    return render_template("index.html",
                           products=products)


@app.route("/Recommendations/<int:user_id>")
def recommend(user_id):

    recommended_ids = run_ga(user_id)

    products = get_products_by_ids(
        recommended_ids
    )

    return render_template(
        "Recommendations.html",
        products=products,
        user_id=user_id
    )


if __name__ == "__main__":
    app.run(debug=True)