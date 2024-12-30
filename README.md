# Debezium Demo Application

This is a simple demonstration of using Debezium for Change Data Capture (CDC) with PostgreSQL and Apache Kafka.

## Prerequisites

- Docker and Docker Compose
- Python 3.7+
- pip (Python package manager)

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the infrastructure using Docker Compose:
```bash
docker-compose up -d
```

3. Wait for all services to start (this might take a minute or two)

4. Run the demo application:
```bash
python demo.py
```

## What's happening?

1. The application creates a `customers` table in PostgreSQL
2. Configures a Debezium connector to monitor this table
3. Starts listening for changes via Kafka
4. Inserts some test data
5. You'll see the changes being captured and printed in real-time

Example output:
```bash
python3 demo.py

Creating table...
Configuring Debezium connector...
Inserting test data...
Listening for changes...
New customer created: {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'created_at': 1735562705267942}
New customer created: {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'created_at': 1735562707299172}
Customer updated: {'id': 1, 'name': 'John Doe', 'email': 'john.doe.updated@example.com', 'created_at': 1735562705267942}
New customer created: {'id': 3, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'created_at': 1735562747214277}
```

## Components

- PostgreSQL: Source database
- Apache Kafka: Message broker
- Zookeeper: Required for Kafka
- Kafka Connect with Debezium: Captures database changes
- Schema Registry: Manages Avro schemas (optional for this demo)

## Clean up

To stop all services:
```bash
docker-compose down -v
```

This will stop all containers and remove the volumes.
