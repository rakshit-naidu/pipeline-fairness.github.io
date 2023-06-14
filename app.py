from flask import Flask, render_template, request, session, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
def landing():

    return render_template('landing_page.html')

# @app.route('/home', methods=["GET", "POST"])
# def home():
#     if 'username' in session:
#         username = session['username']
#         # Add your logic to fetch user details based on the username
#         user_details = get_user_details(username)
#         return render_template('index.html', username=username, user_details=user_details)
        


@app.route('/home/<mode>/<username>', methods=['GET', 'POST'])
def index(username, mode):
    return render_template('index.html', username=username, mode=mode)

def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the users table (if it does not exist)
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    '''
    cursor.execute(create_table_query)

    conn.commit()
    conn.close()

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        # Get the form data from the request object
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        create_users_table()

        # Check if the email is already taken
        conn = sqlite3.connect('/Users/rakshitnaidu/Desktop/pipeline-fairness/users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? OR username = ?", (email,username))
        if cursor.fetchone():
            message = "Email or username already exists. Please enter a new email and username."
            return render_template('register.html', message=message)

        # If the email and username are available, save the user details in the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()

        # Redirect to the home page
        return redirect('/')

# @app.route('/login', methods=['GET', 'POST'])
# def authenticate():
#     if request.method == "POST":
#     # Get the username and password from the submitted form
#         username = request.form['username']
#         password = request.form['password']

#         # Connect to the users.db database
#         conn = sqlite3.connect('users.db')
#         cursor = conn.cursor()

#         # Query the database to check if the username and password match
#         query = "SELECT * FROM users WHERE username = ? AND password = ?"
#         cursor.execute(query, (username, password))
#         user = cursor.fetchone()

#         # Close the database connection
#         conn.close()

#         if user:
#             # If the user exists, redirect them to the profile page
#             return redirect('/profile')
#         else:
#             # If the user doesn't exist or the credentials are incorrect,
#             # you can display an error message or redirect them to a login failure page
#             return redirect('/login-failure')

def get_user_category(email):
    emailid = email.split('@')[1]
    if emailid.lower().endswith('.edu'):
        return "moderator"
    else:
        return "user"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get the form data
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        remember_me = request.form.get('rememberMe')
        
        # # check if the username and password are correct
        # if username == "admin" and password == "password":
        #     # if the credentials are correct, redirect to the profile page
        #     return redirect(url_for("profile", username=username))

        if remember_me:
            session.permanent = True

        # Connect to the users.db database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        
        # query = "SELECT * FROM users WHERE username = ? AND password = ?"
        # cursor.execute(query, (username, password))
        # user = cursor.fetchone()

        # Check if the user exists in the database
        cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
        user_id = cursor.fetchone()

        mode = get_user_category(email)


        cursor.close()
        conn.close()

        if user_id:
            return redirect(url_for('profile', user_id=user_id[0], mode=mode))
        
        return render_template("login.html")
 
        # if user_id:
        #     # If the user exists, redirect them to the profile page
        #     return redirect(url_for('profile', user_id=user_id[0]))
        # else:
        #     # if the credentials are incorrect, show an error message
        #     error = "Invalid credentials. Please try again."
        #     return render_template("login.html", error=error)
    else:
        return render_template("login.html")

# @app.route("/profile/<username>")
# def profile(username):
#     return render_template("profile.html", username=username)

# @app.route('/profile')
# def profile():
#     # Connect to the SQLite database
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()

#     # Assuming you have a table called "users" with columns "name" and "email"
#     cursor.execute("SELECT name, email FROM users WHERE id = ?", (user_id,))
#     user = cursor.fetchone()

#     # Close the database connection
#     cursor.close()
#     conn.close()

#     # Return user data as JSON response
#     return jsonify({
#         'name': user[0],
#         'email': user[1]
#     })

# @app.route('/<mode>/<user_id>')
# def USER(user_id, mode):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()

#     # Assuming you have a table called "users" with columns "name" and "email"
#     cursor.execute("SELECT username, email FROM users WHERE id = ?", (user_id,))
#     user = cursor.fetchone()

#     # Close the database connection
#     cursor.close()
#     conn.close()

#     return render_template('USER_profile.html', user=user, mode=mode)

@app.route('/<mode>/<user_id>')
def profile(user_id, mode):
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT username, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    # Close the database connection
    cursor.close()
    conn.close()

    if mode == "moderator":
        return render_template('MODERATOR_profile.html', user=user, mode=mode)
    elif mode == "user":
        return render_template('USER_profile.html', user=user, mode=mode)
        

@app.route('/logout')
def logout():
    # session.pop('username', None)
    # Clear session and delete session cookie
    session.clear()
    return render_template("landing_page.html")

@app.route('/search')
def search():
    # handle search query here
    return 'Search results'




# DATA COLLECTION

@app.route('/home/datacollection/sampling.html')
def datacollection_sampling():
    mode = request.args.get('mode', default=None)
    return render_template('datacollection/sampling.html', mode=mode)


@app.route('/home/datacollection/annotation.html')
def datacollection_annotation():
    mode = request.args.get('mode', default=None)
    return render_template('datacollection/annotation.html', mode=mode)


@app.route('/home/datacollection/featuremeasurement.html')
def datacollection_featuremeasurement():
    mode = request.args.get('mode', default=None)
    return render_template('datacollection/featuremeasurement.html', mode=mode)


@app.route('/home/datacollection/recordlinkage.html')
def datacollection_recordlinkage():
    mode = request.args.get('mode', default=None)
    return render_template('datacollection/recordlinkage.html', mode=mode)


@app.route('/home/datacollection/general.html')
def datacollection_general():
    mode = request.args.get('mode', default=None)
    return render_template('datacollection/general.html', mode=mode)


# @app.route('/home/datapreprocessing/featureselection.html', methods=['POST'])
# def datapreprocessing_featureselection(query):
#     # query = request.form.get('query')  # Get the query from the request
    
#     # # Process the query and fetch the appropriate sub-table based on the query
#     sub_table1, sub_table2, sub_table3 = process_query(query)
    
#     return render_template('featureselection.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3))


# def process_query(query):
#     q1, q2 = query.split(",")[0].strip().lower(), query.split(",")[1].strip().lower()
#     if "datapreprocessing" in q1:

#         if q2 == "problemidentification":

#         elif q2 == "measurement":

#         elif q2 == "mitigation":






if __name__ == '__main__':
    app.run(debug=True)