import bcrypt
from flask import Flask, render_template, request ,url_for, redirect, session
import pymongo
from flask.helpers import flash
import imgbbpy
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

load_dotenv()

cluster = MongoClient(os.environ.get('MONGO_URI'))
cluster = MongoClient("mongodb+srv://aj_15:anajessica@cluster0.pdcrn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db1 = cluster["Loan_Customers_Info"]
# db2 = cluster["Loan_Requests_Info"]
col  = db1["Details"]
col1 = db1["Requests"]


app = Flask(__name__)

UPLOAD_PATH = "static/"
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

#encryption relies on secret keys so they could be run
app.secret_key = "testing"
#connoct to your Mongo DB database

client = pymongo.MongoClient("mongodb+srv://aj_15:anajessica@cluster0.pdcrn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
client = pymongo.MongoClient(os.environ.get('MONGO_URI'))

#get the database name
db = client.get_database('total_records')
#get the particular collection that contains the data
records = db.register

#assign URLs to have a particular route 
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')



@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'LOGIN IN '
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('form.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')

@app.route('/submit', methods = ["GET","POST"])
def get_details():
    if request.method == 'POST':
        name                    = request.values.get("name")
        past_debt               = request.values.get("debt")
        loan_type               = request.values.get("loan")
        monthly_income          = request.values.get("income")
        source_income           = request.values.get("source")
     
        
        my_dict = {}

        my_dict ["Name"]                = name
        my_dict ["past_debt"]           = past_debt 
        my_dict ["loan_type"]           = loan_type
        my_dict ["monthly_income"]      = monthly_income
        my_dict ["source_income"]      = source_income 
      

        uploaded_file           = request.files['photo']
        uploaded_file_1         = request.files['ac']
        uploaded_file_2         = request.files['pc']
        uploaded_files          = request.files['files']


        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # else :
        #     filename = 'avatar.png'

        client = imgbbpy.SyncClient('3e5affdb90cfdbc171774c0f1a9d23dc')

        image = client.upload(file= 'static/' + filename) 
        img = image.url
        my_dict ["photo"]               = img

        filename_1 = secure_filename(uploaded_file_1.filename)
        if filename_1 != '':
            file_ext = os.path.splitext(filename_1)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_1))
   

        filename_2 = secure_filename(uploaded_file_2.filename)
        if filename_2 != '':
            file_ext = os.path.splitext(filename_2)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_2))
     

        filenames = secure_filename(uploaded_files.filename)
        if filenames != '':
            file_ext = os.path.splitext(filenames)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filenames))


        upload_details(my_dict)

        x = cibil_score(my_dict)

        # names = get_details()

        return render_template('loan.html', c_score = x)
    
    return render_template('form.html')



@app.route('/apply', methods = ["GET","POST"])
def apply_form():
    if request.method == 'POST':
        name                    = request.values.get("name")
        loan_amount             = request.values.get("amount")
        tenure                  = request.values.get("tenure")
        rate                    = request.values.get("rate")
        
        my_req = {}

        my_req ["Name"]                  = name
        my_req ["Loan_amount"]           = loan_amount
        my_req ["Tenure"]                = tenure 
        my_req ["Rate"]                  = rate
 

        apply_requests(my_req)

        return redirect("/view")
      
    
    return render_template('apply.html')

@app.route("/view", methods=["GET","POST"])
def view():
    
    data =[]
    x =col1.find({})
    for y in x:
        data.append(y)

    return render_template('view.html', result = data)

@app.route('/single', methods=["GET","POST"])
def display():

    name = str(request.args['com_nam'])

    x = col1.find_one({"Name":name},{'_id':0,'Name':1,'Loan_amount':1,'Tenure':1,'Rate':1})
    print(x)

    return render_template('single.html', result = x)

@app.route('/delete', methods=["GET","POST"])
def delete():
    name = str(request.args['com_nam'])

    myquery = {"Name":name}

    col1.delete_one(myquery)
    return render_template('delete.html')

def upload_details(my_dict):

    x = col.insert_one(my_dict)

    return x

def apply_requests(my_req):

    x = col1.insert_one(my_req)

    return x

def cibil_score(my_dict):
    if  my_dict ["past_debt"] == "No" and my_dict ["monthly_income"] == "Less than 15,000 INR":
        x = 600

    elif my_dict ["past_debt"] == "No" and my_dict ["loan_type"] == "Unsecured":
        x= 650
    
    else:
        x=700
    
    return x


if __name__ == "__main__":
  app.run(debug=True)
