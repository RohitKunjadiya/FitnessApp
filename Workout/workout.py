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

# Create Blueprint
app_workout = Blueprint("app_workout", __name__, template_folder="templates")

@app_workout.route("/")
def index():
    return render_template("workout.html")

@app_workout.route("/recommend", methods=["POST"])
def recommend():
    goal = request.form.get("goal")
    time = request.form.get("time")

    prompt = f"""
    You are a professional fitness coach. A user has the goal: "{goal}" and has {time} minutes available for workout today.

    Generate a personalized workout plan based on this. Make sure:
    - The plan fits within {time} minutes
    - Exercises align with the goal: "{goal}"
    - Mention the name, reps/duration, and any rest breaks
    - Use emojis and motivational tone 🎯💥

    Give tips if needed, and make it beginner-friendly unless it's an advanced goal.
    """

    if not model:
        recommendation = "Gemini model is not available at the moment. Please try again later."
    else:
        try:
            response = model.generate_content(prompt)
            recommendation = response.text
        except Exception as e:
            print("Gemini API error:", e)
            recommendation = "Couldn’t generate a workout plan right now. Please try again later!"

    return render_template("workout.html", recommendation=recommendation)