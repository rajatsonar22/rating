from flask import Flask, request, jsonify, send_file, render_template
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate TEXT,
                    rating INTEGER
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    data = request.json
    candidate = data['candidate']
    rating = data['rating']
    
    conn = sqlite3.connect('ratings.db')
    c = conn.cursor()
    c.execute("INSERT INTO ratings (candidate, rating) VALUES (?, ?)", (candidate, rating))
    conn.commit()
    conn.close()
    return jsonify({"message": "Rating submitted successfully!"})

@app.route('/download_ratings', methods=['GET'])
def download_ratings():
    # Admin authentication can be added here
    conn = sqlite3.connect('ratings.db')
    df = pd.read_sql_query("SELECT * FROM ratings", conn)
    conn.close()

    output_file = 'ratings.xlsx'
    df.to_excel(output_file, index=False)

    return send_file(output_file, as_attachment=True)

@app.route('/rate/<team_name>')
def rate_team(team_name):
    return render_template('rate.html', team_name=team_name)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
