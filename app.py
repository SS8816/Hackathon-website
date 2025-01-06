from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/hackathon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

# Database Modelṇ
class Results4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    mse = db.Column(db.Float, nullable=False)
    r_squared = db.Column(db.Float, nullable=False)
    presentation_score = db.Column(db.Float, nullable=False)
    feature_engineering_score = db.Column(db.Float, nullable=False)
    timing_score = db.Column(db.Float, nullable=False)  # New field for timing score
    final_score = db.Column(db.Float, nullable=False)

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Route for Prediction Submission Page
@app.route('/submit_predictions', methods=['GET', 'POST'])
def submit_predictions():
    if request.method == 'POST':
        if 'prediction_file' not in request.files or 'target_file' not in request.files:
            flash("Both prediction and target files are required", "danger")
            return redirect(url_for('submit_predictions'))

        team_name = request.form['team_name']
        prediction_file = request.files['prediction_file']
        target_file = request.files['target_file']

        try:
            predictions = pd.read_csv(prediction_file, header=None, dtype=float).squeeze()
            target = pd.read_csv(target_file, header=None, dtype=float).squeeze()

            if predictions.shape != target.shape:
                flash("Prediction and target files must have the same number of entries", "danger")
                return redirect(url_for('submit_predictions'))

            # Calculate MSE and R-squared
            mse = np.sqrt(np.mean((predictions - target) ** 2))
            ss_total = np.sum((target - np.mean(target)) ** 2)
            ss_residual = np.sum((target - predictions) ** 2)
            r_squared = float(1 - (ss_residual / ss_total))

            if r_squared < 0: 
                r_squared = 0

            existing_result = Results4.query.filter_by(team_name=team_name).first()
            if existing_result:
                existing_result.mse = mse
                existing_result.r_squared = r_squared
            else:
                new_result = Results4(
                    team_name=team_name,
                    mse=mse,
                    r_squared=r_squared,
                    presentation_score=0.0,
                    feature_engineering_score=0.0,
                    timing_score=0.0,
                    final_score=0.0
                )
                db.session.add(new_result)

            db.session.commit()
            flash("Results submitted successfully!", "success")
            return render_template("evaluation_result.html", mse=mse, r_squared=r_squared)
        except Exception as e:
            flash(f"Error processing files: {str(e)}", "danger")
            return redirect(url_for('submit_predictions'))
    return render_template('submit_predictions.html')

# Route for Judge Scores Submission Page
@app.route('/submit_judge_scores', methods=['GET', 'POST'])
def submit_judge_scores():
    if request.method == 'POST':
        team_name = request.form['team_name']
        presentation_score = float(request.form['presentation_score'])
        feature_engineering_score = float(request.form['feature_engineering_score'])
        timing_score = float(request.form['timing_score'])  # Get the timing score from the form

        # Fetch the result using the team name
        result = Results4.query.filter_by(team_name=team_name).first()
        if result:
            # Calculate final score using the new weight distribution
            final_score = (result.r_squared * 40) + (presentation_score * 0.25) + (timing_score * 0.1) + (feature_engineering_score * 0.25)
            result.presentation_score = presentation_score
            result.feature_engineering_score = feature_engineering_score
            result.timing_score = timing_score  # Store the timing score
            result.final_score = final_score
            
            db.session.commit()
            flash("Judge scores submitted successfully!", "success")
            return redirect(url_for('leaderboard'))
        else:
            flash("Team not found", "danger")
            return redirect(url_for('submit_judge_scores'))
    return render_template('submit_judge_scores.html')
# Route for Leaderboard
@app.route('/leaderboard')
def leaderboard():
    results = Results4.query.order_by(Results4.final_score.desc()).all()
    return render_template('leaderboard.html', results=results)

    # Route for Instructions Page
@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)