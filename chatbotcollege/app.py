from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask,render_template, request
import torch
import  random
import json
from model import  NeuralNet
from nltk_utils import tokenize,stem,bag_of_words

app = Flask(__name__)
app = Flask(__name__, static_url_path = "", static_folder = "static")

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'firstaidbuddy'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/fristaidbuddy/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg='')

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/firstaidbuddy/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/firstaidbuddy/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/firstaidbuddy/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/firstaidbuddy/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/firstaidbuddy/fdisform', methods=['GET','POST'])
def fdisform():
	if request.method == 'POST':
		ph=request.form['ph']
		mail=request.form['mail']
		name=request.form['name']
		disease=request.form['disease']
		age=request.form['age']
		cursor = mysql.connection.cursor()
		cursor.execute(
			'insert into chatbotentries values(%s,%s,%s,%s,%s)',(ph,mail,name,disease,age)
		)
		mysql.connection.commit()
		cursor.close()
	return render_template("fdisform.html")

@app.route('/firstaidbuddy/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/firstaidbuddy/amrita', methods=['GET','POST'])
def amrita():
	if request.method == 'POST':
		ph=request.form['ph']
		mail=request.form['mail']
		name=request.form['name']
		disease=request.form['disease']
		age=request.form['age']
		cursor = mysql.connection.cursor()
		cursor.execute(
			'insert into amritanursing values(%s,%s,%s,%s,%s)',(ph,mail,name,disease,age)
		)
		mysql.connection.commit()
		cursor.close()
	return render_template("amrita.html")

@app.route('/firstaidbuddy/jadhav', methods=['GET','POST'])
def jadhav():
	if request.method == 'POST':
		ph=request.form['ph']
		mail=request.form['mail']
		name=request.form['name']
		disease=request.form['disease']
		age=request.form['age']
		cursor = mysql.connection.cursor()
		cursor.execute(
			'insert into jadhavnursing values(%s,%s,%s,%s,%s)',(ph,mail,name,disease,age)
		)
		mysql.connection.commit()
		cursor.close()
	return render_template("jadhav.html")

@app.route('/firstaidbuddy/vairagi', methods=['GET','POST'])
def vairagi():
	if request.method == 'POST':
		ph=request.form['ph']
		mail=request.form['mail']
		name=request.form['name']
		disease=request.form['disease']
		age=request.form['age']
		cursor = mysql.connection.cursor()
		cursor.execute(
			'insert into vairaginursing values(%s,%s,%s,%s,%s)',(ph,mail,name,disease,age)
		)
		mysql.connection.commit()
		cursor.close()
	return render_template("vairagi.html")

@app.route('/firstaidbuddy/wagle', methods=['GET','POST'])
def wagle():
	if request.method == 'POST':
		ph=request.form['ph']
		mail=request.form['mail']
		name=request.form['name']
		disease=request.form['disease']
		age=request.form['age']
		cursor = mysql.connection.cursor()
		cursor.execute(
			'insert into waglenursing values(%s,%s,%s,%s,%s)',(ph,mail,name,disease,age)
		)
		mysql.connection.commit()
		cursor.close()
	return render_template("wagle.html")

@app.route('/firstaidbuddy/campregistration', methods=['GET','POST'])
def campregistration():
	if request.method == 'POST':
		ph=request.form['ph']
		mail=request.form['mail']
		name=request.form['name']
		campname=request.form['campname']
		age=request.form['age']
		cursor = mysql.connection.cursor()
		cursor.execute(
			'insert into camps values(%s,%s,%s,%s,%s)',(ph,mail,name,campname,age)
		)
		mysql.connection.commit()
		cursor.close()
	return render_template("campregistration.html")

@app.route("/get")
def  get_bot_response():
    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)
    userText = request.args.get('msg')
    data = torch.load("data.pth")

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]
    bot_name = "Sam"
    model = NeuralNet(input_size, hidden_size, output_size)
    model.load_state_dict(model_state)
    model.eval()


    sentence = tokenize(userText)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                res = random.choice(intent['responses'])
    else:
        res="I do not understand..."

    return str(res)






if __name__=="__main__":
    app.run(debug=True)