from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_channel_info(channel_url):
    response = requests.get(channel_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print("Scraping successful!")  # Add a print statement for debugging
        channel_name = soup.find('h1', class_='channel-name').text
        profile_picture = soup.find('img', class_='profile-picture')['src']
        return channel_name, profile_picture
    else:
        print("Failed to fetch data!")  # Add a print statement for debugging
        return None, None

@app.route('/get-channel-info', methods=['POST'])
def get_channel_info():
    if request.method == 'POST':
        data = request.get_json()
        channel_url = data.get('channel_url')
        
        channel_name, profile_picture = scrape_channel_info(channel_url)
        
        if channel_name and profile_picture:
            response = {
                "channel_name": channel_name,
                "profile_picture": profile_picture
            }
            return jsonify(response)
        else:
            return jsonify({"error": "Unable to fetch channel information"}), 500

if __name__ == '__main__':
    print("Starting Flask app...")  # Add a print statement for Flask startup
    app.run(debug=True)
