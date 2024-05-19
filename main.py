from flask import Flask, render_template, jsonify, send_file, request, Response
import requests

app = Flask(__name__)

# The Cat API endpoint
CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
# The Dog API endpoint
DOG_API_URL = 'https://dog.ceo/api/breeds/image/random'
# The Rabbit API endpoint
RABBIT_API_URL = 'https://rabbit-api-two.vercel.app/api/random'

@app.route('/')
def home():
    cat_response = requests.get(CAT_API_URL)
    dog_response = requests.get(DOG_API_URL)
    rabbit_response = requests.get(RABBIT_API_URL)
    
    if cat_response.status_code == 200 and dog_response.status_code == 200 and rabbit_response.status_code == 200:
        cat_data = cat_response.json()
        dog_data = dog_response.json()
        rabbit_data = rabbit_response.json()
        cat_image_url = cat_data[0]['url']
        dog_image_url = dog_data['message']
        rabbit_image_url = rabbit_data['url']
        return render_template('index.html', 
                               cat_image_url=cat_image_url, 
                               dog_image_url=dog_image_url,
                               rabbit_image_url=rabbit_image_url)
    else:
        return 'Failed to get cat, dog or rabbit image', 500

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

@app.route('/get-rabbit')
def get_rabbit():
    rabbit_response = requests.get(RABBIT_API_URL)
    if rabbit_response.status_code == 200:
        rabbit_data = rabbit_response.json()
        rabbit_image_url = rabbit_data['url']
        return jsonify(rabbit_image_url=rabbit_image_url)
    else:
        return jsonify(error='Failed to get rabbit image'), 500

@app.route('/download-image')
def download_image():
    url = request.args.get('url')
    image_response = requests.get(url, stream=True)
    if image_response.status_code == 200:
        return Response(
            image_response.content,
            mimetype=image_response.headers['Content-Type'],
            headers={
                "Content-Disposition": f"attachment; filename={url.split('/')[-1]}"
            }
        )
    else:
        return 'Failed to download image', 500

if __name__ == '__main__':
    app.run(debug=True)
