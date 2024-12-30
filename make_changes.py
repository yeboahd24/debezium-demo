import psycopg2

def make_changes():
    conn = psycopg2.connect(
        dbname="inventory",
        user="postgres",
        password="mesika",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()
    
    # Update an existing customer
    cur.execute(
        "UPDATE customers SET email = %s WHERE name = %s",
        ('john.doe.updated@example.com', 'John Doe')
    )
    
    # Insert a new customer
    cur.execute(
        "INSERT INTO customers (name, email) VALUES (%s, %s)",
        ('Alice Johnson', 'alice@example.com')
    )
    
    # Commit the changes
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    make_changes()
