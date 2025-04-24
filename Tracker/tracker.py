from flask import Blueprint, render_template, request
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up Gemini model
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    model = None
    print("Error loading Gemini model:", e)

# Tracker Blueprint
app_tracker = Blueprint("app_tracker", __name__, template_folder="templates")


# Homepage Route
@app_tracker.route("/")
def index():
    return render_template("tracker.html")


# Track and Generate Insights Route
@app_tracker.route("/track", methods=["POST"])
def track():
    # Get user input from form
    weight = request.form.get("weight")
    steps = request.form.get("steps")
    calories = request.form.get("calories")

    # Message to display on the page
    msg = f"Today's Stats - Weight: {weight} kg, Steps: {steps}, Calories Burned: {calories}"

    # Prepare input prompt for AI model
    input_prompt = f"""
    A user has submitted their fitness tracking data:
    - Weight: {weight} kg
    - Steps: {steps}
    - Calories burned: {calories}

    You are a fitness expert and motivational coach. Based on the data:
    1. Give a short analysis of the user's daily performance.
    2. Motivate them with an inspiring message or quote 💪🔥.
    3. Suggest one simple action or improvement for tomorrow.
    Be supportive, concise, and use emojis to make it fun.
    """

    try:
        # Generate AI feedback
        response = model.generate_content(input_prompt)
        ai_feedback = response.text

    except Exception as e:
        # Handle errors
        ai_feedback = "Couldn't fetch AI feedback right now. Please try again later."

    # Render the template with user stats and AI feedback
    return render_template("tracker.html", msg=msg, ai_feedback=ai_feedback)