from flask import Flask,render_template,request,send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
import os
import random as r
import time


app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, "temp")

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
success =""

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('base.html')

@app.route('/xlsx_files',methods=['GET','POST'])
def cta_xlsx():
    return render_template('xlsx.html')

@app.route('/xls_files',methods=['GET','POST'])
def cta_xls():
    return render_template('xls.html')

@app.route('/csv_files',methods=['GET','POST'])
def cta_csv():
    return render_template('csv.html')

@app.route('/merge_xlsx',methods=['POST','GET'])
def excel_xlsx():
    print("Hello, am in the loop...")
    if request.method  == "POST":
        print("confirmed, method is POST")
        if request.form['sub']=="Select":
            print("Select received")
            selected = request.files.getlist("xlsx")
            if len(selected) != 0:
                if selected:
                    excel_files =[]
                    f = ''
                    for fil in selected:
                        #print(fil)
                        f = secure_filename(fil.filename) 
                        if f[-4:] == 'xlsx':
                            excel_files.append(f)
                            fil.save(os.path.join(app.config['UPLOAD_FOLDER'], f))
                        else:
                            print("No xlsx files in the directory")
                            msg = "No xlsx files in the directory"
                            return render_template('xlsx.html', msg=msg,success= "error")

                    #print(excel_files)
                    data =[]
                    for file in excel_files:
                        dt = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],file),header=0,index_col=None)
                        data.append(dt)
                    if len(data) != 0:
                        df = pd.concat(data)
                        #print(df)

                        #create a dataFrame
                        dframe =pd.DataFrame(df)
                        print("Merging.....")
                
                        hashed = r.randint(1000,9999)
                        hashed = str(hashed)
                        merged_file = f"merged_{hashed}.xlsx"
                        dframe.to_excel(os.path.join(app.config['UPLOAD_FOLDER'],merged_file ),index=False)
                        
                        msg = "Merged all files successfully...."
                        print("merged all the files successfully...")

                        #delete the temporary files uploaded
                        for item in excel_files:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],item))
                        
                        return render_template('xlsx.html', msg=msg,success= "success",download = merged_file)
                    else: 
                        print("No files available")
                        msg = "No files available"
                        return render_template('xlsx.html',msg=msg,success="error")
 
            return render_template('xlsx.html',msg="Something Wrong",success="error")
        return render_template('xlsx.html',msg="Something Wrong",success="error")
    return render_template('xlsx.html',msg="request not allowed",success = "error")

@app.route('/merge_xls',methods=['POST','GET'])
def excel_xls():
    print("Hello, am in the loop...")
    if request.method  == "POST":
        print("confirmed, method is POST")
        if request.form['sub']=="Select":
            print("Select received")
            selected = request.files.getlist("xls")
            if len(selected) != 0:
                if selected:
                    excel_files =[]
                    f = ''
                    for fil in selected:
                        #print(fil)
                        f = secure_filename(fil.filename) 
                        if f[-3:] == 'xls':
                            excel_files.append(f)
                            fil.save(os.path.join(app.config['UPLOAD_FOLDER'], f))
                        else:
                            print("No xls files in the directory")
                            msg = "No xls files in the directory"
                            return render_template('xls.html', msg=msg,success= "error")

                    #print(excel_files)
                    data =[]
                    for file in excel_files:
                        dt = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'],file),engine='xlrd',header=0,index_col=None)
                        data.append(dt)
                    if len(data) != 0:
                        df = pd.concat(data)
                        #print(df)

                        #create a dataFrame
                        dframe =pd.DataFrame(df)
                        dframe = dframe.iloc[:,1:]
                        print("Merging.....")
                
                        hashed = r.randint(1000,9999)
                        hashed = str(hashed)
                        merged_file = f"merged_{hashed}.xls"
                        dframe.to_excel(os.path.join(app.config['UPLOAD_FOLDER'],merged_file ),engine="openpyxl",index=False)
                        
                        msg = "Merged all files successfully...."
                        print("merged all the files successfully...")

                        #delete the temporary files uploaded
                        for item in excel_files:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],item))
                        
                        return render_template('xls.html', msg=msg,success= "success",download = merged_file)
                    else: 
                        print("No files available")
                        msg = "No files available"
                        return render_template('xls.html',msg=msg,success="error")
 
            return render_template('xls.html',msg="Something Wrong",success="error")
        return render_template('xls.html',msg="Something Wrong",success="error")
    return render_template('xls.html',msg="request not allowed",success = "error")

@app.route('/merge_csv',methods=['POST','GET'])
def csv():
    print("Hello, am in the loop...")
    if request.method  == "POST":
        print("confirmed, method is POST")
        if request.form['sub']=="Select":
            print("Select received")
            selected = request.files.getlist("csv")
            if len(selected) != 0:
                if selected:
                    csv_files =[]
                    f = ''
                    for fil in selected:
                        #print(fil)
                        f = secure_filename(fil.filename) 
                        if f[-3:] == 'csv':
                            csv_files.append(f)
                            fil.save(os.path.join(app.config['UPLOAD_FOLDER'], f))
                        else:
                            print("No csv files in the directory")
                            msg = "No csv files in the directory"
                            return render_template('csv.html', msg=msg,success= "error")

                    #print(csv_files)
                    data =[]
                    for file in csv_files:
                        dt = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'],file),header=0,index_col=None)
                        data.append(dt)
                    if len(data) != 0:
                        df = pd.concat(data)
                        #print(df)

                        #create a dataFrame
                        dframe =pd.DataFrame(df)
                        dframe = dframe.iloc[:,2:]
                        print("Merging.....")
                
                        hashed = r.randint(1000,9999)
                        hashed = str(hashed)
                        merged_file = f"merged_{hashed}.csv"
                        dframe.to_csv(os.path.join(app.config['UPLOAD_FOLDER'],merged_file ),index=False)
                        
                        msg = "Merged all files successfully...."
                        print("merged all the files successfully...")

                        #delete the temporary files uploaded
                        for item in csv_files:
                            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],item))
                        
                        return render_template('csv.html', msg=msg,success= "success",download = merged_file)
                    else: 
                        print("No files available")
                        msg = "No files available"
                        return render_template('csv.html',msg=msg,success="error")
 
            return render_template('csv.html',msg="Something Wrong",success="error")
        return render_template('csv.html',msg="Something Wrong",success="error")
    return render_template('csv.html',msg="request not allowed",success = "error")

@app.route('/uploads/<path:fileName>', methods =['GET','POST'])
def  download(fileName):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'],path=fileName)     

@app.route('/success', methods=['GET','POST'])
def download_success():
    if request.method == "POST":
        if request.form['downloaded'] == 'success':
            item_delete = request.form['download']
            msg ="file downloaded successfully, check your download folder..."
            success = "success"
            time.sleep(3)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],item_delete))
            return render_template('base.html',msg=msg,success=success)
    return render_template('base.html')
#app.run(port=8000,host="localhost",debug=True,threaded=True)
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app,use_reloader=True)
