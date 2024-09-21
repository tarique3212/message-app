from flask import Flask, jsonify, request, render_template
import psycopg2
import uuid
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )

@app.route('/get/messages', methods=['GET'])
def get_messages_form():
    return render_template('get_messages_form.html')

@app.route('/get/messages/<account_id>', methods=['GET'])
def get_messages(account_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM messages WHERE account_id = %s', (account_id,))
        messages = cur.fetchall()
        
        if messages:
            return render_template('get_messages_results.html', messages=messages)
        else:
            return render_template('get_messages_results.html', messages=[])

    finally:
        cur.close()
        conn.close()

@app.route('/create', methods=['GET', 'POST'])
def create_message():
    if request.method == 'POST':
        # Get data from form
        account_id = request.form['account_id']
        sender_number = request.form['sender_number']
        receiver_number = request.form['receiver_number']
        
        message_id = str(uuid.uuid4())
        message = (
            account_id,
            message_id,
            sender_number,
            receiver_number
        )

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO messages (account_id, message_id, sender_number, receiver_number) VALUES (%s, %s, %s, %s)',
                message
            )
            conn.commit()
            return render_template('create_results.html', message_id=message_id), 201
        finally:
            cur.close()
            conn.close()
    else:
        # Serve the HTML form
        return render_template('create_form.html')

@app.route('/search', methods=['GET'])
def search():
    if request.args:
        # Extract the field and its corresponding value
        field = next(iter(request.args))  # Get the first query parameter key
        value = request.args.get(field)  # Get the value for that field

        if field not in ['message_id', 'sender_number', 'receiver_number']:
            return jsonify({"error": "Invalid field selected"}), 400

        query = f"SELECT * FROM messages WHERE {field} IN %s"
        filters = [tuple(value.split(','))] if value else []

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            if filters:
                cur.execute(query, filters)
                messages = cur.fetchall()
                return render_template('search_results.html', messages=messages)
            else:
                return render_template('search_results.html', messages=[])

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()
            conn.close()

    return render_template('search_form.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
