from flask import Flask, render_template, redirect, url_for, request
from Calories.calories import app_calories
from Workout.workout import app_workout
from Diet.diet import app_diet
from Tracker.tracker import app_tracker

app = Flask(__name__)
app.config["SECRET_KEY"] = "FITNESS_SECRET_KEY"

# Register blueprints
app.register_blueprint(app_calories, url_prefix="/calories")
app.register_blueprint(app_workout, url_prefix="/workout")
app.register_blueprint(app_diet, url_prefix="/diet")
app.register_blueprint(app_tracker, url_prefix="/tracker")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/select_option", methods=["GET", "POST"])
def select_option():
    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option == "calories":
            return redirect(url_for("app_calories.index"))
        elif selected_option == "workout":
            return redirect(url_for("app_workout.index"))
        elif selected_option == "diet":
            return redirect(url_for("app_diet.index"))
        elif selected_option == "tracker":
            return redirect(url_for("app_tracker.index"))

    return render_template("select_option.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)