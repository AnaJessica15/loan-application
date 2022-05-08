# Import necessary modules
from flask import Flask, render_template, request , jsonify
from flask.helpers import flash
import imgbbpy
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient

load_dotenv()

# cluster = MongoClient(os.environ.get('MONGO_URI'))
cluster = MongoClient("mongodb+srv://aj_15:6385715202@cluster0.pdcrn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Loan_Customers_Info"]
col = db["Details"]


app = Flask(__name__)

UPLOAD_PATH = "static/"
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

# @app.route('/')
# def index():
#     return render_template('login.html')

@app.route('/form')
def form():
    # files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('form.html')


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
        my_dict ["source_income "]      = source_income 
      

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

        # names = get_details()

        return render_template('form.html')
    
    return render_template('form.html')

def upload_details(my_dict):

    x = col.insert_one(my_dict)

    return x

if __name__ == "__main__":
    
    app.run(debug=True,host="0.0.0.0",port="3012")