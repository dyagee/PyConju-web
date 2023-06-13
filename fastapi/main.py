from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI,Request, Form,UploadFile,File
from typing import Annotated,List
from pydantic import BaseSettings
import aiofiles
import pandas as pd
import os
import random as r
import time 
import uvicorn



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

#create a temporary upload dir
UPLOAD_FOLDER = os.path.join(app.root_path, "temp")

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

#create settings using pydantic model
class Setting(BaseSettings):
    app_name:str = "Pyconju"
    author = "Agee Aondo"
    year = 2023
    upload_folder:str = UPLOAD_FOLDER

#call instance of the setting class
setting = Setting()
success =""
msg =""

@app.get('/',response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse('base.html',{"request":request})

@app.post('/merge',response_class=HTMLResponse)
async def excel(request:Request, sub:Annotated[str,Form()], xls:List[UploadFile]=File(...)):
    
    if sub  == "Select":
        excel_files =[]
        name = ''
        if len(xls) != 0:
            for file in xls:
                name =file.filename
                #print(name)
                if name[-4:] == 'xlsx':
                    excel_files.append(name)
                    #output path
                    file_path = os.path.join(setting.upload_folder,name)
                    #save the file in chunks using aiofiles
                    async with aiofiles.open(file_path,'wb') as outfile:
                        while content:= await file.read(1024):
                            await outfile.write(content)
                else:
                    print("No xlsx files in the directory")
                    msg = "No xlsx files in the directory"
                    return templates.TemplateResponse('base.html', {'request':request,'msg':msg,'success': "error"})
            
            #convert excel files to dataframe
            data =[]
            for file in excel_files:
                dt = pd.read_excel(os.path.join(setting.upload_folder,file),header=0,index_col=None)
                data.append(dt)

            if len(data) != 0:
                df = pd.concat(data)
                #print(df)
                #create a dataFrame
                dframe =pd.DataFrame(df)
                #print("Merging.....")
                #create a random hash number
                hashed = r.randint(1000,9999)
                hashed = str(hashed)
                merged_file = f"merged_{hashed}.xlsx"
                dframe.to_excel(os.path.join(setting.upload_folder,merged_file ))
                        
                msg = "Merged all files successfully...."
                print("merged all the files successfully...")
                #print(request.client.host,request.url,app.url_path_for("download",fileName = f"{merged_file}"))

                #delete the temporary files uploaded
                for item in excel_files:
                    os.remove(os.path.join(setting.upload_folder,item))
                return templates.TemplateResponse('base.html',{'request':request,'msg':msg,'success': "success",'download':merged_file} )
        else: 
            print("No files available")
            msg = "No files available"
            return templates.TemplateResponse('base.html',{'request':request,'msg':"Something Wrong",'success':"error"})
    return templates.TemplateResponse('base.html',{'request':request,'msg':"request not allowed",'success': "error"})
            

            
@app.get('/uploads/{fileName}',response_class=FileResponse)
async def  download(fileName:str):
    path=fileName
    return os.path.join(setting.upload_folder,path) 


@app.post('/success', response_class=HTMLResponse)
async def download_success(request:Request, downloaded:Annotated[str,Form()],download:Annotated[str,Form()]):
    if downloaded == "success":
        item_delete = download
        msg ="file downloaded successfully, check your download folder..."
        success = "success"
        time.sleep(3)
        os.remove(os.path.join(setting.upload_folder,item_delete))
        return templates.TemplateResponse('base.html',{'request':request,'msg':msg,'success':success})
    return templates.TemplateResponse('base.html',{'request':request})

#uncomment this block if you don't want to run uvicorn in CLI                   
#if __name__ ==  "__main__":
#    uvicorn.run("app:app",port=8000,host="localhost",reload=True)
