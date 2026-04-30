import random
import sqlite3

NUM_PRODUCTS = 5
POPULATION = 10
GENERATIONS = 15

# Get all available product IDs from the database

def get_products():
    conn = sqlite3.connect("database/store.db")
    cur = conn.cursor()

    cur.execute("SELECT product_id FROM products")
    data = [x[0] for x in cur.fetchall()]

    conn.close()
    return data

# Create a random individual (solution) from available products

def create_solution(products):
    return random.sample(products, NUM_PRODUCTS)

# Calculate fitness score of a solution based on user behavior

def fitness(solution, user_id):

    conn = sqlite3.connect("database/store.db")
    cur = conn.cursor()

    score = 0

    for p in solution:

        cur.execute("""
        SELECT viewed, clicked, purchased
        FROM behavior
        WHERE product_id=? AND user_id=?
        """, (p, user_id))

        rows = cur.fetchall()

        for r in rows:
            score += r[0]*1 + r[1]*2 + r[2]*5

    conn.close()

    return score

# Combine two parents to create a child solution

def crossover(a, b):

    cut = random.randint(1, NUM_PRODUCTS-1)

    child = a[:cut] + b[cut:]

    # إزالة التكرار
    child = list(set(child))

    return child

# Randomly modify one product in the solution

def mutate(sol, products):

    if random.random() < 0.3:

        sol[random.randint(0, len(sol)-1)] = random.choice(products)

    return sol

# Run the genetic algorithm to find the best recommendation set

def run_ga(user_id):

    products = get_products()

    population = [create_solution(products)
                  for _ in range(POPULATION)]

    for _ in range(GENERATIONS):

        population = sorted(
            population,
            key=lambda x: fitness(x, user_id),
            reverse=True
        )

        new_pop = population[:4]

        while len(new_pop) < POPULATION:

            p1 = random.choice(population[:5])
            p2 = random.choice(population[:5])

            child = crossover(p1, p2)

            child = mutate(child, products)

            new_pop.append(child)

        population = new_pop

    return population[0]