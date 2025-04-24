from flask import Blueprint, render_template, request, jsonify, send_file
import os
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO

# Load environment variable
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app_diet = Blueprint("app_diet", __name__, template_folder="templates")

# Set up Gemini model
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    model = None
    print("Error loading Gemini model:", e)

@app_diet.route('/')
def index():
    return render_template("diet.html")

@app_diet.route('/', methods=['POST'])
def generate_diet():
    name = request.form['name']
    goal = request.form['goal']
    weight = request.form['weight']
    height = request.form['height']
    age = request.form['age']
    gender = request.form['gender']
    food = request.form['food']

    prompt = f"""
    Act like an AI-based fitness advisor. Create a detailed daily personalized diet plan based on:
    Name: {name}
    Goal: {goal}
    Weight: {weight} kg
    Height: {height} cm
    Age: {age}
    Gender: {gender}
    Food Preference: {food}

    Ensure the diet includes a meal-by-meal breakdown (breakfast, lunch, dinner, snacks), along with calorie estimates and macronutrients. Make it healthy and achievable. Be friendly in tone.
    """

    response = model.generate_content(prompt)
    return render_template("diet.html", response=response.text, name=name)

@app_diet.route('/download/<name>')
def download(name):
    # Fetch or regenerate the diet plan (you may store it temporarily if needed)
    # For simplicity, regenerating here
    prompt = f"""
    Act like an AI-based fitness advisor. Generate a daily personalized diet plan for {name}.
    Keep it concise and formatted in plain text for download.
    """
    response = model.generate_content(prompt)
    plan = response.text

    buffer = BytesIO()
    buffer.write(plan.encode('utf-8'))
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{name}_diet_plan.txt", mimetype='text/plain')