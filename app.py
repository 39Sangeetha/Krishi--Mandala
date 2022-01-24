from fastapi import FastAPI, Request
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from starlette.datastructures import URL, URLPath
import starlette.status as status
from starlette.responses import RedirectResponse  

app = FastAPI()  

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request : Request):
      return templates.TemplateResponse("index.html",{"request" : request})
URLPath(path="/")    

@app.get("/Products", response_class=HTMLResponse)
def Products(request : Request):
    return templates.TemplateResponse("Products.html",{"request" : request})
URLPath(path="/Products")

@app.get("/newsfeed", response_class=HTMLResponse)
def newsfeed(request : Request):
    return templates.TemplateResponse("newsfeed.html",{"request" : request})
URLPath(path="/newsfeed")  

@app.get("/login", response_class=HTMLResponse)
def login(request : Request):
    return templates.TemplateResponse("login.html",{"request" : request})
URLPath(path="/login")  

@app.get("/register", response_class=HTMLResponse)
def register(request : Request):
    return templates.TemplateResponse("register.html",{"request" : request})
URLPath(path="/register")  

@app.get("/crops", response_class=HTMLResponse)
def crops(request : Request):
    return templates.TemplateResponse("crops.html",{"request" : request})
URLPath(path="/crops")

@app.get("/fruits", response_class=HTMLResponse)
def fruits(request : Request):
    return templates.TemplateResponse("fruits.html",{"request" : request})
URLPath(path="/fruits")    

@app.get("/vegetables", response_class=HTMLResponse)
def vegetables(request : Request):
    return templates.TemplateResponse("vegetables.html",{"request" : request})
URLPath(path="/vegetables") 

@app.get("/seeds", response_class=HTMLResponse)
def seeds(request : Request):
    return templates.TemplateResponse("seeds.html",{"request" : request})
URLPath(path="/seeds")  

@app.get("/fertilizer", response_class=HTMLResponse)
def seeds(request : Request):
        return templates.TemplateResponse("fertilizer.html",{"request" : request})
URLPath(path="/fertilizer")  



@app.get("/farmerregister", response_class=HTMLResponse)
def farmerregister(request : Request):
    con = sqlite3.connect("register.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from register")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("farmerregister.html",{"request" : request, "items" : items})

@app.post("/farmerregister",response_class=HTMLResponse)
def addregister(request : Request, Name : str =  Form(...), Age : int = Form(...), Gender : str = Form(...), PhoneNumber : str = Form(...), AadharNumber:str =Form(...), Address : str = Form(...), District:str = Form(...),State : str = Form(...),FarmCategory : str = Form(...),id : str = Form(...),nameb : str = Form(...), accno : int = Form(...), bankName : str = Form(...),ifsccode : str = Form(...)  ):
    with sqlite3.connect("register.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into register(Name,Age,Gender,PhoneNumber,AadharNumber ,Address,District,State,FarmCategory,id,nameb,accno,bankName,ifsccode) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Name,Age,Gender,PhoneNumber,AadharNumber,Address,District,State,FarmCategory,id,nameb,accno,bankName,ifsccode))
        con.commit()
    return RedirectResponse("/",status_code=status.HTTP_302_FOUND)

@app.get("/userregister", response_class=HTMLResponse)
def index(request : Request):
    con = sqlite3.connect("uregister.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from uregister")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("userregister.html",{"request" : request, "items" : items})

@app.post("/userregister",response_class=HTMLResponse)
def adduregister(request : Request, Name : str =  Form(...), PhoneNumber : str = Form(...), Address : str = Form(...), District:str = Form(...),State : str = Form(...),Pincode : str = Form(...),id  : str = Form(...) ):
    with sqlite3.connect("uregister.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into uregister(Name,PhoneNumber,Address,District,State,pincode,id,role) values(?,?,?,?,?,?,?,?)",(Name,PhoneNumber,Address,District,State,Pincode,id))
        con.commit()
    return RedirectResponse("/userregister",status_code=status.HTTP_302_FOUND)
URLPath(path="/userregister")
        
@app.get("/authorregister", response_class=HTMLResponse)
def index(request : Request):
    con = sqlite3.connect("aregister.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from aregister")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("authorregister.html",{"request" : request, "items" : items})

@app.post("/authorregister",response_class=HTMLResponse)
def addaregister(request : Request, Name : str =  Form(...), dob : str = Form(...), gender : str = Form(...), phno: str = Form(...),address  : str = Form(...),district   : str = Form(...),state : str = Form(...)):
    with sqlite3.connect("aregister.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into aregister(Name,dob,gender,phno,address,district,state,role) values(?,?,?,?,?,?,?,?)",(Name,dob,gender,phno,address,district,state,"Blogger"))
        con.commit()
    return RedirectResponse("/authorregister",status_code=status.HTTP_302_FOUND)
URLPath(path="/authorregister")

        #return templates.TemplateResponse("index.html",{"request" : request, "message" : "succesfully added!!" })
