import psycopg2
import json
import time
import requests
from kafka import KafkaConsumer

def create_table():
    conn = psycopg2.connect(
        dbname="inventory",
        user="postgres",
        password="mesika",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()
    
    # Create customers table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def insert_customer(name, email):
    conn = psycopg2.connect(
        dbname="inventory",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5433"
    )
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO customers (name, email) VALUES (%s, %s)",
        (name, email)
    )
    
    conn.commit()
    cur.close()
    conn.close()

def configure_debezium():
    # Configure Debezium connector
    connector_config = {
        "name": "inventory-connector",
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "tasks.max": "1",
            "database.hostname": "postgres",
            "database.port": "5432",
            "database.user": "postgres",
            "database.password": "mesika",
            "database.dbname": "inventory",
            "database.server.name": "dbserver1",
            "table.include.list": "public.customers",
            "plugin.name": "pgoutput",
            "topic.prefix": "dbserver1",
            "slot.name": "inventory_slot"
        }
    }
    
    # Send connector configuration to Kafka Connect
    response = requests.post(
        "http://localhost:8083/connectors",
        headers={"Content-Type": "application/json"},
        data=json.dumps(connector_config)
    )
    
    if response.status_code not in (201, 409):  # 409 means already exists
        print(f"Failed to configure connector: {response.text}")
        return False
    return True

def listen_to_changes():
    # Create Kafka consumer
    consumer = KafkaConsumer(
        'dbserver1.public.customers',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print("Listening for changes...")
    for message in consumer:
        change_event = message.value
        if 'payload' in change_event:
            operation = change_event['payload']['op']
            if operation == 'c':  # Create operation
                data = change_event['payload']['after']
                print(f"New customer created: {data}")
            elif operation == 'u':  # Update operation
                data = change_event['payload']['after']
                print(f"Customer updated: {data}")
            elif operation == 'd':  # Delete operation
                data = change_event['payload']['before']
                print(f"Customer deleted: {data}")

def main():
    print("Creating table...")
    create_table()
    
    print("Configuring Debezium connector...")
    if not configure_debezium():
        return
    
    # Wait for connector to be fully configured
    time.sleep(10)
    
    # Start listening to changes in a separate process
    from multiprocessing import Process
    consumer_process = Process(target=listen_to_changes)
    consumer_process.start()
    
    # Insert some test data
    print("Inserting test data...")
    insert_customer("John Doe", "john@example.com")
    time.sleep(2)
    insert_customer("Jane Smith", "jane@example.com")
    
    # Keep the main process running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        consumer_process.terminate()
        print("\nShutting down...")

if __name__ == "__main__":
    main()
