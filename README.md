# Hackathon Leaderboard Website

Welcome to the **Hackathon Leaderboard Website**! This project is designed to streamline the evaluation process for machine learning hackathons by automatically calculating team scores based on model performance, feature engineering, presentation, and time. The leaderboard updates in real-time, ensuring a smooth and transparent ranking process.

## Project Overview
This website handles:
- **Model Evaluation**: Submissions are scored based on R-squared (R²) values.
- **Time Efficiency**: Teams are rewarded for early submission.
- **Feature Engineering**: Evaluates how well the data was preprocessed and engineered.
- **Presentation**: Judges score the quality of the team’s final presentation.

The leaderboard displays real-time results and updates automatically when new submissions are made or existing ones are improved.

##  Key Features
- **Real-Time Leaderboard**: Ranks teams as soon as new scores are submitted.
- **Dynamic Scoring System**:
   - **R-squared** - 40%
   - **Presentation** - 30%
   - **Feature Engineering** - 30%
- **Submission Flexibility**: Teams can submit prediction CSV files and update them anytime.
- **CSV Validation**: Ensures that submissions match expected formats.
- **Admin Control**: Allows hackathon organizers to update team scores manually if needed.


## How It Works
1. **Teams submit** their prediction CSV files through the website.
2. The system calculates the **R-squared value** by comparing predictions to a target CSV.
3. Judges evaluate and score **feature engineering** and **presentation**.
4. The final score is computed using the weighted formula:
   ```
   Final Score = (0.4 * R-squared) + (0.3 * Presentation Score) + (0.3 * Feature Engineering Score)
   ```
5. The leaderboard is updated to reflect the new standings.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: MySQL (via XAMPP & PHPMyAdmin)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Hackathon-website.git
   ```
2. Navigate to the project folder:
   ```bash
   cd Hackathon-website
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. Access the website at:
   ```
   http://localhost:5000

## 🎯 Future Improvements
- **Automated Feedback** on submissions
- **Detailed Analytics** for model performance
- **User Authentication** for teams



