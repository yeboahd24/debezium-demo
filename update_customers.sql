-- Update an existing customer
UPDATE customers SET email = 'john.doe.updated@example.com' WHERE name = 'John Doe';

-- Insert a new customer
INSERT INTO customers (name, email) VALUES ('Alice Johnson', 'alice@example.com');

-- Delete a customer (uncomment if you want to test deletion)
-- DELETE FROM customers WHERE name = 'Jane Smith';
