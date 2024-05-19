from flask import Flask, render_template, jsonify, send_file, request
import requests
import random
import os

app = Flask(__name__)

# The Cat API endpoint
CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
# The Dog API endpoint
DOG_API_URL = 'https://dog.ceo/api/breeds/image/random'

@app.route('/')
def home():
    cat_response = requests.get(CAT_API_URL)
    dog_response = requests.get(DOG_API_URL)
    
    if cat_response.status_code == 200 and dog_response.status_code == 200:
        cat_data = cat_response.json()
        dog_data = dog_response.json()
        cat_image_url = cat_data[0]['url']
        dog_image_url = dog_data['message']
        return render_template('index.html', 
                               cat_image_url=cat_image_url, 
                               dog_image_url=dog_image_url)
    else:
        return 'Failed to get cat or dog image', 500

@app.route('/get-cat')
def get_cat():
    cat_response = requests.get(CAT_API_URL)
    if cat_response.status_code == 200:
        cat_data = cat_response.json()
        cat_image_url = cat_data[0]['url']
        return jsonify(cat_image_url=cat_image_url)
    else:
        return jsonify(error='Failed to get cat image'), 500

@app.route('/get-dog')
def get_dog():
    dog_response = requests.get(DOG_API_URL)
    if dog_response.status_code == 200:
        dog_data = dog_response.json()
        dog_image_url = dog_data['message']
        return jsonify(dog_image_url=dog_image_url)
    else:
        return jsonify(error='Failed to get dog image'), 500

@app.route('/download-image')
def download_image():
    url = request.args.get('url')
    filename = url.split('/')[-1]
    image_response = requests.get(url)
    if image_response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(image_response.content)
        return send_file(filename, as_attachment=True)
    else:
        return 'Failed to download image', 500

if __name__ == '__main__':
    app.run(debug=True)
