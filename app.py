from flask import Flask, send_file, request, jsonify
from flask_cors import CORS # CORS allow karne ke liye
import os

# Server setup
app = Flask(__name__)
CORS(app) # Local testing ke liye CORS enabled kiya
IMAGE_FOLDER = 'images'

@app.route('/get_image', methods=['POST'])
def get_image():
    # User se JSON data (query) lein
    try:
        data = request.get_json()
        image_name_raw = data.get('query')
    except:
        # Agar JSON nahi mila toh form data check karein
        image_name_raw = request.form.get('query')

    if not image_name_raw:
        return jsonify({"message": "Boss, Kripya image ka naam bataiye."}), 400

    # Query ko simple file name mein badlein (lowercase, no spaces, etc.)
    image_name = image_name_raw.lower().strip().replace(' ', '_')
    
    # Possible extensions check karein
    possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    
    found_file = None
    
    for ext in possible_extensions:
        file_path = os.path.join(IMAGE_FOLDER, f'{image_name}{ext}')
        if os.path.exists(file_path):
            found_file = file_path
            break # Pehli mili hui file ko use karein
    
    if found_file:
        # Image mili, toh uska MIME type guess karke send kar do
        # send_file automatically MIME type guess kar leta hai
        return send_file(found_file)
    else:
        # Image nahi mili
        # Aap chahein toh yahan ek default "Image Not Found" image bhi bhej sakte hain
        return jsonify({"message": f"Sorry Maharaj, '{image_name_raw}' naam ki image nahi mili."}), 404

@app.route('/', methods=['GET'])
def home():
    # Home page ke liye simple message ya index.html serve kar sakte hain
    return "Image Fetching API is Running. Use /get_image endpoint."

if __name__ == '__main__':
    # Server ko run karein
    # Yeh development server hai. Production ke liye aapko gunicorn ya isse kuch aur use karna padega.
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True)