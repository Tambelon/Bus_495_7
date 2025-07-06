# application.py
from flask import Flask, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

NASA_API_KEY = 'DEMO_KEY'  # Replace with your actual NASA API key

@app.route('/api/nasa/images', methods=['GET'])
def get_nasa_images():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'error': 'Both start_date and end_date are required'}), 400
    
    try:
        # Convert dates to ensure they're valid
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # NASA APOD API endpoint
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&start_date={start_date}&end_date={end_date}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
