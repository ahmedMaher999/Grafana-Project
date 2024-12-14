from flask import Flask, jsonify
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