from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from zinga_bot import ZingaBot

app = Flask(__name__)
app.secret_key = 'zinga-secret'

# Upload setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bot = ZingaBot()

# 🏠 HOME ROUTE
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "accept":
            session['pending_dare'] = True
            return redirect("/submit-proof")

        elif action == "skip":
            session['pending_dare'] = False
            session.pop('current_dare', None)  # show new dare
            return redirect("/")

    # Load existing dare or generate a new one
    if 'current_dare' not in session:
        dare = bot.get_dare()
        session['current_dare'] = dare
    else:
        dare = session['current_dare']

    return render_template("index.html", dare=dare["text"], mood=bot.mood, streak=bot.streak)

# ✅ SUBMIT PROOF ROUTE
@app.route("/submit-proof", methods=["GET", "POST"])
def submit_proof():
    today = datetime.now().strftime("%Y-%m-%d")

    if session.get('last_proof_date') == today:
        return render_template("already_submitted.html")

    if request.method == "POST":
        file = request.files['proof']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            bot.update_mood(accepted=True)
            session['last_proof_date'] = today
            session['pending_dare'] = False
            session.pop('current_dare', None)  # get new dare on next visit

            return redirect("/")

    return render_template("submit.html")

# 🔁 RESET ROUTE (optional)
@app.route("/reset")
def reset():
    session.clear()
    bot.streak = 0
    bot.mood = "Happy"
    return redirect("/")

# 🚀 START FLASK
if __name__ == "__main__":
    app.run(debug=True)
