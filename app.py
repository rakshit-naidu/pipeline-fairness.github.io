from flask import Flask, g, render_template, request, session, redirect, url_for, session, jsonify
import sqlite3
import csv, pandas as pd
import os
# from excelsheetpapers_to_htmltable import process_query


app = Flask(__name__)

# Global variable initialization
# @app.before_request
# def before_request():
#     g.logged_in = False

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index_b4_login.html')

@app.route('/home/<username>')
def index_after_login(username):
    # username = request.args.get('username')
    # mode = request.args.get('mode')
    return render_template('index_after_login.html', username=username) #mode=mode)
    

@app.route('/landing')
def landing():
    return render_template('landing_page.html')


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

    create_users_table()

    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':


        # Get the form data from the request object
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # print(username, email, password)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        # If the email and username are available, save the user details in the database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        cursor.close()
        
        # Check if the email is already taken
        # conn = sqlite3.connect('/Users/rakshitnaidu/Desktop/pipeline-fairness/users.db')
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM users WHERE email = ? OR username = ?", (email,username))
        # if cursor.fetchone():
        #     message = "Email or username already exists. Please enter a new email and username."
        #     return render_template('register.html', message=message)

        
        conn.close()
        # Redirect to the home page
        return redirect('/')

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
        # username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        # remember_me = request.form.get('rememberMe')
        
        # # check if the username and password are correct
        # if username == "admin" and password == "password":
        #     # if the credentials are correct, redirect to the profile page
        #     return redirect(url_for("profile", username=username))

        # if remember_me:
        #     session.permanent = True

        # Connect to the users.db database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        # Check if the user exists in the database
        cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
        user_id = cursor.fetchone()

        # cursor = conn.cursor()
        # # get username
        # query = "SELECT username FROM users WHERE email = ? AND password = ?"
        # cursor.execute(query, (email, password))
        # username = cursor.fetchone()

        

        mode = get_user_category(email)


        cursor.close()
        conn.close()

        if user_id:
            g.logged_in = True
            return redirect(url_for('profile', user_id=user_id[0], mode=mode))
        
        return render_template("login.html")
 
    else:
        return render_template("login.html")

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

    # print(mode)

   

    if mode == "moderator":
        return render_template('MODERATOR_profile.html', user=user, mode=mode)
    elif mode == "user":
        return render_template('USER_profile.html', user=user, mode=mode)
    
    # return redirect(url_for('landing'))
        

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

def process_query(query):
    # Read the original DataFrame from a CSV file or another source
    original_table = pd.read_csv('data/Pipeline Fairness Lit Review - updated_table.csv')
    # print(original_table)
    original_table["Tags/Comments"] = original_table["Tags/Comments"].fillna('')
    original_table["Year"] = original_table["Year"].astype(int)
    # original_table['Paper link'] = original_table['Paper link'].apply(lambda x: f'<a href="{x}">Link</a>')
    # Perform the query and filter the DataFrame based on the query
    filtered_table1 = original_table[(original_table['Tags/Comments'].str.contains(query) & original_table['Tags/Comments'].str.contains("Problem Identification"))]
    filtered_table2 = original_table[(original_table['Tags/Comments'].str.contains(query) & original_table['Tags/Comments'].str.contains("Measurement"))]
    filtered_table3 = original_table[(original_table['Tags/Comments'].str.contains(query) & original_table['Tags/Comments'].str.contains("Mitigation"))]
    # print(filtered_table)
    # Convert the filtered DataFrame to a list of dictionaries for JSON serialization
    sub_table1 = filtered_table1.to_dict(orient='records')
    sub_table2 = filtered_table2.to_dict(orient='records')
    sub_table3 = filtered_table3.to_dict(orient='records')


    # d = {"Paper Title": "N/A",
    #     "Authors": "N/A",
    #     "Description": "N/A",
    #     "Tags/Comments": "N/A",
    #     "Conference Venue": "N/A",
    #     "Year": "N/A",
    #     "Paper link": "N/A",
    #     "Additional resources": "N/A"}
    
    # if len(sub_table1)==0:
    #     sub_table1.append(d) 
    
    # elif len(sub_table2)==0:
    #     sub_table2.append(d) 
        
    # elif len(sub_table3)==0:
    #     sub_table3.append(d) 

    return sub_table1, sub_table2, sub_table3

# VIABILITY ASSESSMENTS

@app.route('/static/templates/viabilityassessments/cost.html', methods=['GET', 'POST'])
def viabilityassessments_cost():
    query = "Viability Assessments-Cost/Benefit"  # Get the query from the request
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('viabilityassessments/cost.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/viabilityassessments/general.html', methods=['GET', 'POST'])
def viabilityassessments_general():
    query = "Viability Assessments-General"  # Get the query from the request
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('viabilityassessments/general.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)

# PROBLEM FORMULATION

@app.route('/static/templates/problemformulation/predictiontarget.html', methods=['GET', 'POST'])
def problemformulation_predictiontarget():
    query = "Problem Formulation-Prediction Target"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('problemformulation/predictiontarget.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/problemformulation/predictiveattributes.html', methods=['GET', 'POST'])
def problemformulation_predictiveattributes():
    query = "Problem Formulation-Predictive Attributes" 
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('problemformulation/predictiveattributes.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/problemformulation/general.html', methods=['GET', 'POST'])
def problemformulation_general():
    query = "Problem Formulation-General" 
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('problemformulation/general.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


# DATA COLLECTION

@app.route('/static/templates/datacollection/sampling.html', methods=['GET', 'POST'])
def datacollection_sampling():
    query = "Data Collection-Sampling"  # Get the query from the request
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datacollection/sampling.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)



@app.route('/static/templates/datacollection/annotation.html', methods=['GET', 'POST'])
def datacollection_annotation():
    query = "Data Collection-Annotation"  # Get the query from the request
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datacollection/annotation.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/datacollection/featuremeasurement.html', methods=['GET', 'POST'])
def datacollection_featuremeasurement():
    query = "Data Collection-Feature Measurement"  # Get the query from the request
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datacollection/featuremeasurement.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/datacollection/recordlinkage.html', methods=['GET', 'POST'])
def datacollection_recordlinkage():
    query = "Data Collection-Record Linkage"  # Get the query from the request
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datacollection/recordlinkage.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/datacollection/general.html', methods=['GET', 'POST'])
def datacollection_general():
    query = "Data Collection-General"  # Get the query from the request
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datacollection/general.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


# DATA PREPROCESSING


@app.route('/static/templates/datapreprocessing/featurecreation.html', methods=['GET', 'POST'])
def datapreprocessing_featurecreation():
    query = "Data Preprocessing-Feature Creation"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datapreprocessing/featurecreation.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/datapreprocessing/featureselection.html', methods=['GET', 'POST'])
def datapreprocessing_featureselection():
    query = "Data Preprocessing-Feature Selection"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datapreprocessing/featureselection.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/datapreprocessing/omission.html', methods=['GET', 'POST'])
def datapreprocessing_omission():
    query = "Data Preprocessing-Data Cleaning"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datapreprocessing/omission.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/datapreprocessing/general.html', methods=['GET', 'POST'])
def datapreprocessing_general():
    query = "Data Preprocessing-General"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('datapreprocessing/general.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


# STATISTICAL MODELING

@app.route('/static/templates/statisticalmodeling/hypothesisclass.html', methods=['GET', 'POST'])
def statisticalmodeling_hypothesisclass():
    query = "Statistical Modeling-Hypothesis Class"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('statisticalmodeling/hypothesisclass.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/statisticalmodeling/optfunc.html', methods=['GET', 'POST'])
def statisticalmodeling_optfunc():
    query = "Statistical Modeling-Optimization Function"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('statisticalmodeling/optfunc.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/statisticalmodeling/hyperparameters.html', methods=['GET', 'POST'])
def statisticalmodeling_hyperparameters():
    query = "Statistical Modeling-Hyperparameters"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('statisticalmodeling/hyperparameters.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/statisticalmodeling/regularizers.html', methods=['GET', 'POST'])
def statisticalmodeling_regularizers():
    query = "Statistical Modeling-Regularizers"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('statisticalmodeling/regularizers.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/statisticalmodeling/general.html', methods=['GET', 'POST'])
def statisticalmodeling_general():
    query = "Statistical Modeling-General"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('statisticalmodeling/general.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)

# TESTING & VALIDATION

@app.route('/static/templates/testingnvalidation/traintestsplit.html', methods=['GET', 'POST'])
def testingnvalidation_traintestsplit():
    query = "Testing and Validation-Train/Test Split"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('testingnvalidation/traintestsplit.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/testingnvalidation/evaluationmetrics.html', methods=['GET', 'POST'])
def testingnvalidation_evaluationmetrics():
    query = "Testing and Validation-Evaluation Metrics"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('testingnvalidation/evaluationmetrics.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/testingnvalidation/general.html', methods=['GET', 'POST'])
def testingnvalidation_general():
    query = "Testing and Validation-General"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('testingnvalidation/general.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


# DEPLOYMENT & INTEGRATION

@app.route('/static/templates/deploymentnintegration/humancomputerhandoff.html', methods=['GET', 'POST'])
def deploymentnintegration_humancomputerhandoff():
    query = "Deployment and Integration-Human/Computer Handoff"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('deploymentnintegration/humancomputerhandoff.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/deploymentnintegration/maintenanceoversight.html', methods=['GET', 'POST'])
def deploymentnintegration_maintenanceoversight():
    query = "Deployment and Integration-Maintenance Oversight"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('deploymentnintegration/maintenanceoversight.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)


@app.route('/static/templates/deploymentnintegration/general.html', methods=['GET', 'POST'])
def deploymentnintegration_general():
    query = "Deployment and Integration-General"
    sub_table1, sub_table2, sub_table3 = process_query(query)
    return render_template('deploymentnintegration/general.html', sub_table1=sub_table1, sub_table2=sub_table2, sub_table3=sub_table3)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)