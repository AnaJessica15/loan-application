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
    
        # photo                   = request.values.get("photo") 
        public_hobbies          = request.values.get("p_hobbies")
        public_interests        = request.values.get("p_interests")
        hidden_interests        = request.values.get("interests")
        hidden_hobbies          = request.values.get("h_hobbies")
        challenges              = request.values.get("challenges")

        
        my_dict = {}

        my_dict ["Name"]                = name
    
        my_dict ["public_hobbies"]      = public_hobbies
        my_dict ["public_interests"]    = public_interests
        my_dict ["hidden_interests"]    = hidden_interests
        my_dict ["hidden_hobbies"]      = hidden_hobbies
        my_dict ["challenges"]          = challenges

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
        image_1 = client.upload(file= 'static/' + filename_1) 
        img_1 = image_1.url
        my_dict ["ac"]               = img_1

        filename_2 = secure_filename(uploaded_file_2.filename)
        if filename_2 != '':
            file_ext = os.path.splitext(filename_2)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_2))
        image_2 = client.upload(file= 'static/' + filename_2) 
        img_2 = image_2.url
        my_dict ["pc"]               = img_2

        filenames = secure_filename(uploaded_files.filename)
        if filenames != '':
            file_ext = os.path.splitext(filenames)[1]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filenames))
        images = client.upload(file= 'static/' + filenames) 
        imgs = images.url
        my_dict ["files"]               = imgs

        upload_details(my_dict)

        # names = get_details()

        return render_template('form.html')
    
    return render_template('form.html')

def upload_details(my_dict):

    x = col.insert_one(my_dict)

    return x

if __name__ == "__main__":
    
    app.run(debug=True,host="0.0.0.0",port="3012")