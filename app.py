from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to add a new card
@app.route('/add_card', methods=['POST'])
def add_card():
    data = request.json
    name = data.get('name')
    card_number = data.get('card_number')
    expiry_date = data.get('expiry_date')
    credit_limit = data.get('credit_limit')

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO cards (name, card_number, expiry_date, credit_limit) VALUES (?, ?, ?, ?)',
        (name, card_number, expiry_date, credit_limit)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Card added successfully!'}), 201

# Route to delete a card
@app.route('/delete_card/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cards WHERE id = ?', (card_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Card deleted successfully!'})

# Route to update card details
@app.route('/update_card/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    data = request.json
    name = data.get('name')
    card_number = data.get('card_number')
    expiry_date = data.get('expiry_date')
    credit_limit = data.get('credit_limit')

    conn = get_db_connection()
    conn.execute(
        'UPDATE cards SET name = ?, card_number = ?, expiry_date = ?, credit_limit = ? WHERE id = ?',
        (name, card_number, expiry_date, credit_limit, card_id)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Card updated successfully!'})

# Route to add a transaction
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    card_id = data.get('card_id')
    month = data.get('month')
    year = data.get('year')
    amount = data.get('amount')
    paid = data.get('paid', 0)  # 0 for unpaid, 1 for paid
    paid_date = data.get('paid_date', None)

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO transactions (card_id, month, year, amount, paid, paid_date) VALUES (?, ?, ?, ?, ?, ?)',
        (card_id, month, year, amount, paid, paid_date)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Transaction added successfully!'})

# Route to get the balance for a card
@app.route('/get_balance/<int:card_id>', methods=['GET'])
def get_balance(card_id):
    conn = get_db_connection()
    transactions = conn.execute(
        'SELECT SUM(amount) AS total FROM transactions WHERE card_id = ? AND paid = 0',
        (card_id,)
    ).fetchone()
    conn.close()

    total_balance = transactions['total'] if transactions['total'] else 0
    return jsonify({'balance': total_balance})

# Home route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Credit Card Manager API!'})

if __name__ == '__main__':
    app.run(debug=True)
