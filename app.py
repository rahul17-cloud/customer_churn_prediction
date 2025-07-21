from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from models import db, User
from utils.preprocessing import clean_data
from utils.modeling import load_model, predict_churn
import os


from flask import Flask, render_template, request, jsonify
from utils.chatbot import get_gemini_response
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



app = Flask(__name__)
app.config['SECRET_KEY'] = 'a7c08142d401ec8457b9b419a450e92f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='sha256')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.")
            return redirect('/signup')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/upload')
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['datafile']
        filepath = os.path.join('data/raw', file.filename)
        os.makedirs('data/raw', exist_ok=True)
        file.save(filepath)
        return redirect(url_for('dashboard', filename=file.filename))
    return render_template("upload.html")

@app.route('/dashboard/<filename>')
@login_required
def dashboard(filename):
    filepath = os.path.join('data/raw', filename)
    df = pd.read_csv(filepath)
    df_clean = clean_data(df)
    model = load_model()
    churn_preds = predict_churn(model, df_clean)
    df_result = df_clean.copy()
    df_result['Churn'] = churn_preds

    churn_customers = df_result[df_result['Churn'] == 1]
    not_churn_customers = df_result[df_result['Churn'] == 0]

    os.makedirs('data/outputs', exist_ok=True)
    churn_customers.to_csv('data/outputs/churn_customers.csv', index=False)
    not_churn_customers.to_csv('data/outputs/not_churn_customers.csv', index=False)

    return render_template("dashboard.html",
                           churned=churn_customers.to_dict(orient='records'),
                           not_churned=not_churn_customers.to_dict(orient='records'))

@app.route('/download/<category>')
@login_required
def download_csv(category):
    output_dir = 'data/outputs'
    if category == 'churn':
        path = os.path.join(output_dir, 'churn_customers.csv')
    elif category == 'not_churn':
        path = os.path.join(output_dir, 'not_churn_customers.csv')
    else:
        return "Invalid category"
    return send_file(path, as_attachment=True)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("message")
    response = get_gemini_response(user_input)
    return jsonify({"response": response})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)