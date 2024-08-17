from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__, static_folder='graphs')  # Specify the custom static folder

# Load your final dataset
politicians_df = pd.read_csv('Databases/final_politicians_info.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip().lower()
    if query:
        results = politicians_df[politicians_df['Name'].str.lower().str.contains(query)]
        return jsonify(results.to_dict(orient='records'))
    return jsonify([])

@app.route('/graphs/<path:filename>')
def custom_static(filename):
    return send_from_directory('graphs', filename)

if __name__ == '__main__':
    app.run(debug=True)
