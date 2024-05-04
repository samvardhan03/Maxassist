import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password"
)

# Create a cursor
cur = conn.cursor()

# Execute SQL queries
cur.execute("INSERT INTO qa_pairs (question, answer) VALUES (%s, %s)", (question, answer))
conn.commit()

