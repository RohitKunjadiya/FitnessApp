from flask import Blueprint, render_template, request, jsonify
from PIL import Image
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the blueprint
app_calories = Blueprint("app_calories", __name__, template_folder="templates")

# Use the correct Gemini Vision model
model = genai.GenerativeModel("models/gemini-1.5-pro-vision")


@app_calories.route('/')
def index():
    return render_template("calories.html")


@app_calories.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')

    if file:
        image = Image.open(file)

        input_prompt = """
        You are an expert in nutrition. Analyze the food items from the image and estimate:
        1. Calories per item 🍽️
        2. Healthiness 🥦
        3. Nutritional breakdown (carbs, fats, fiber, sugar, etc.) 📊
        4. Suggested replacements for a healthier diet ✅
        Be detailed, and explain in an easy-to-understand way. Add emojis where appropriate to keep it friendly!
        """

        try:
            response = model.generate_content([input_prompt, image])
            return jsonify({'response': response.text})
        except Exception as e:
            return jsonify({'response': f"Error: {str(e)}"})

    return jsonify({'response': 'No image provided.'})