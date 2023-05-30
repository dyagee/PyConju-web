from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI,Request, Form
from tkinter import filedialog as dialog
import tkinter
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows as drows
import os



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get('/',response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse('base.html',{"request":request})

@app.post('/merge',response_class=HTMLResponse)
async def excel(request:Request, submit:str=Form(...)):
    
    if submit  == "Select":
        if submit:
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

                return templates.TemplateResponse('base.html',{"request":request, "msg":msg,"class":"success"})
        return templates.TemplateResponse('base.html',{"request":request, "msg":"Something Wrong","class":"error"})
    return templates.TemplateResponse('base.html',{"request":request, "msg":"Only get request allowed","class":"error"})
        

