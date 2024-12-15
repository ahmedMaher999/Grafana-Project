from flask import Flask, jsonify
from faker import Faker
import mysql.connector
import os

app = Flask(__name__)

# Database configuration (using environment variables for security)
db_config = {
    'host': os.getenv('MYSQL_HOST', 'mysql-db'),
    'user': os.getenv('MYSQL_USER', 'irs_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'password123'),
    'database': os.getenv('MYSQL_DATABASE', 'irs_data')
}

faker = Faker()

# Function to seed data into the database
def seed_data():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into taxpayers table
        for _ in range(500):  # Create 500 taxpayers
            name = faker.name()
            age = faker.random_int(min=18, max=80)
            state = faker.state()
            cursor.execute("INSERT INTO taxpayers (name, age, state) VALUES (%s, %s, %s)", (name, age, state))

        conn.commit()

        # Retrieve all taxpayers
        cursor.execute("SELECT id FROM taxpayers")
        taxpayer_ids = [row[0] for row in cursor.fetchall()]

        # Insert data into returns table
        for taxpayer_id in taxpayer_ids:
            for _ in range(2):  # Add 2 returns per taxpayer
                year = faker.random_int(min=1940, max=2024)
                tax_paid = round(faker.random_number(digits=4) + faker.random.random(), 2)
                refund = round(faker.random.uniform(0, tax_paid), 2)
                filing_type = faker.random_element(elements=["Individual", "Joint"])
                cursor.execute(
                    "INSERT INTO returns (taxpayer_id, year, tax_paid, refund, filing_type) VALUES (%s, %s, %s, %s, %s)",
                    (taxpayer_id, year, tax_paid, refund, filing_type)
                )

        conn.commit()
        cursor.close()
        conn.close()

        return "Database seeded successfully!"

    except mysql.connector.Error as err:
        return f"Error: {err}"

# Route to trigger the seeding process
@app.route('/seed-database', methods=['GET'])
def seed_database():
    message = seed_data()
    return jsonify({'message': message})

# Routes
@app.route('/total-revenue', methods=['GET'])
def total_revenue():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(tax_paid) FROM returns;')
        total_revenue = cursor.fetchone()[0]
        conn.close()
        return jsonify({'total_revenue': total_revenue})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/refunds-by-state', methods=['GET'])
def refunds_by_state():
    conn = mysql.connector.connect(**db_config)  
    cursor = conn.cursor()
    cursor.execute('''
        SELECT state, SUM(refund)
        FROM taxpayers t
        JOIN returns r ON t.id = r.taxpayer_id
        GROUP BY state;
    ''')
    results = [{'state': row[0], 'total_refunds': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

@app.route('/filings-by-year', methods=['GET'])
def filings_by_year():
    conn = mysql.connector.connect(**db_config)  # Use ** to unpack the dictionary as arguments
    cursor = conn.cursor()

    cursor.execute('''
        SELECT year, COUNT(*) 
        FROM returns 
        GROUP BY year;
    ''')
    # Process query results into a list of dictionaries
    results = [{'year': row[0], 'filings': row[1]} for row in cursor.fetchall()]
    
    conn.close()  # Close the connection
    return jsonify(results)  # Return the results as a JSON response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')