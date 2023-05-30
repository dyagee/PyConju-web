from flask import Flask,render_template,request
from tkinter import filedialog as dialog
import tkinter
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows as drows
import os



app = Flask(__name__)
success =""

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('base.html')

@app.route('/merge',methods=['POST','GET'])
def excel():
    print("Hello, am in the loop...")
    if request.method  == "POST":
        print("confirmed, method is POST")
        if request.form['submit']=="Select":
            print("Select received")
            root = tkinter.Tk()
            root.withdraw()
            root.wm_attributes('-topmost',1)
            #root.attributes('-topmost',True)
            path = dialog.askdirectory()
            
        
            if path !='':
                files = os.listdir(path)
                #print(files)
            
                if files:
                    excel_files =[]
                    for f in files:
                        if f[-4:] == 'xlsx':
                            excel_files.append(f)
                    #print(excel_files)
                    data =[]
                    for file in excel_files:
                        dt = pd.read_excel(os.path.join(path,file),header=0,index_col=None)
                        data.append(dt)
                    if len(data) != 0:
                        df = pd.concat(data)
                        #print(df)

                        #create a dataFrame
                        dframe =pd.DataFrame(df)
                        print("Merging.....")

                        # Create an Excel file and write the data
                        wb = openpyxl.Workbook()
                        ws = wb.active
                        for row in drows(dframe,header=True,index=False):
                            ws.append(row)

                        wb.save('merged_files.xlsx')
                        print("merged all the files successfully...")
                        msg = "Merged all files successfully...."
                    else:
                        print("No xlsx files in the directory")
                        msg = "No xlsx files in the directory"
                else: 
                    print("No files available")
                    msg = "No files available"

                return render_template('base.html', msg=msg,success= "success")
        return render_template('base.html',msg="Something Wrong",success="error")
    return render_template('base.html',msg="request not allowed",success = "error")
        
#app.run(port=8000,host="localhost",debug=True,threaded=True)
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 0, app,threaded=True)
