from datetime import datetime
from turtle import title
from unicodedata import category
from urllib import request
from fastapi import FastAPI, Request, Cookie
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from starlette.middleware.sessions import SessionMiddleware 
from starlette.datastructures import URL, URLPath
import starlette.status as status
from starlette.responses import RedirectResponse,Response 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from Telegram import Telegram

app = FastAPI()  
security = HTTPBasic()
telegram = Telegram("5235854735:AAFPlFyow2J-nL1n03-EeY-mQYer56cQ10A","krishi_mandala")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key='MyApp')

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request : Request):
    return templates.TemplateResponse("index.html",{"request" : request})

@app.get("/Products", response_class=HTMLResponse)
def Products(request : Request):
    return templates.TemplateResponse("Products.html",{"request" : request})

@app.get("/aboutus", response_class=HTMLResponse)
def Products(request : Request):
    return templates.TemplateResponse("aboutus.html",{"request" : request})

@app.get("/logout/aboutus", response_class=HTMLResponse)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/aboutus", status_code=status.HTTP_302_FOUND)    

@app.get("/admin/sendmessage", response_class=HTMLResponse)
def Products(request : Request):
    return templates.TemplateResponse("/admin/send.html",{"request" : request})

@app.post("/admin/sendmessage",response_class=HTMLResponse)
def addblog(request : Request, message : str = Form(...)):
    telegram.sendmessage(message)
    return RedirectResponse("/admin/dashboard",status_code=status.HTTP_302_FOUND)

@app.get("/newsfeed", response_class=HTMLResponse)
def newsfeed(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from blog")
    blogs = cur.fetchall()
    con.close
    return templates.TemplateResponse("newsfeed.html",{"request" : request,"blogs" : blogs })

@app.get("/chart", response_class=HTMLResponse)
def chart(request : Request):
    return templates.TemplateResponse("chart.html",{"request" : request})

@app.get("/upload", response_class=HTMLResponse)
def upload(request : Request):
    return templates.TemplateResponse("upload.html",{"request" : request})

@app.get("/upload_home", response_class=HTMLResponse)
def upload_home(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from blog")
    blogs = cur.fetchall()
    con.close
    return templates.TemplateResponse("upload_home.html",{"request" : request,"blogs" : blogs })

@app.post("/upload",response_class=HTMLResponse)
def addblog(request : Request, name : str =  Form(...), title : str = Form(...), content : str = Form(...), image :str =Form(...)):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into verify_blog(name,title,content,image) values(?,?,?,?)",(name,title,content,image))
        con.commit()
    return RedirectResponse("/upload_home",status_code=status.HTTP_302_FOUND)

@app.post("/admin/upload",response_class=HTMLResponse)
def addblog(request : Request, name : str =  Form(...), title : str = Form(...), content : str = Form(...), image :str =Form(...)):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into blog(name,title,content,image) values(?,?,?,?)",(name,title,content,image))
        con.commit()
        telegram.sendmessage(content)
    return RedirectResponse("/admin/dashboard",status_code=status.HTTP_302_FOUND)

@app.get("/login", response_class=HTMLResponse)
def login(request : Request):
    return templates.TemplateResponse("login.html",{"request" : request})
URLPath(path="/login")  

@app.post("/login", response_class=HTMLResponse)
def do_login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from farmer where username =? and password=?", [username, password])
    farmer = cur.fetchone()
    if not farmer:
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid Username or Password"})
    elif farmer['role'] == '1':
        request.session.setdefault("isLogin", True)
        
        request.session.setdefault('username', farmer['username'])
        request.session.setdefault('role',farmer['role'])
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    elif farmer['role'] == '2':
        request.session.setdefault("isLogin", True)
        request.session.setdefault('uid', farmer['id'])
        request.session.setdefault('username', farmer['username'])
        request.session.setdefault('role',farmer['role'])
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    else:
        request.session.setdefault("isLogin", True)
        request.session.setdefault('username', farmer['username'])
        request.session.setdefault('role',farmer['role'])
        return RedirectResponse("/upload_home", status_code=status.HTTP_302_FOUND)

@app.get("/register", response_class=HTMLResponse)
def register(request : Request):
    return templates.TemplateResponse("register.html",{"request" : request})

@app.get("/crops", response_class=HTMLResponse)
def crops(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where category = 'crops'")
    crops = cur.fetchall()
    con.close
    return templates.TemplateResponse("crops.html",{"request" : request,"crops" : crops })

@app.get("/fruits", response_class=HTMLResponse)
def fruits(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where category = 'Fruits'")
    fruits = cur.fetchall()
    con.close
    return templates.TemplateResponse("fruits.html",{"request" : request,"fruits" : fruits })

@app.get("/vegetables", response_class=HTMLResponse)
def vegetables(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where category = 'Vegetables' ")
    vegetables = cur.fetchall()
    con.close
    return templates.TemplateResponse("vegetables.html",{"request" : request , "vegetables" : vegetables})

@app.get("/admin/orders", response_class=HTMLResponse)
def admin_orders(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT *, o.id as oid from farmer u, products p, orders o where o.uid = u.id and o.pid = p.id")
    orders = cur.fetchall()
    con.close
    return templates.TemplateResponse("/admin/orders.html", {"request": request, "orders": orders})

@app.get("/admin/orders", response_class=HTMLResponse)
def admin_orders(request: Request):
    return templates.TemplateResponse("/admin/orders.html", {"request": request})

@app.get("/admin/orders_view/{oid}", response_class=HTMLResponse)
def admin_order_view(request: Request, oid: int = 0):
    return templates.TemplateResponse("/admin/orders_view.html", {"request": request})

@app.get("/seeds", response_class=HTMLResponse)
def seeds(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where category = 'Seeds' ")
    seeds = cur.fetchall()
    con.close
    return templates.TemplateResponse("seeds.html",{"request" : request, "seeds" : seeds})

@app.get("/fertilizer", response_class=HTMLResponse)
def seeds(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where category = 'Fertilizers' ")
    fertilzer = cur.fetchall()
    con.close
    return templates.TemplateResponse("fertilizer.html",{"request" : request, "fertilizer" : fertilzer})
 
@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

@app.get("/contactus", response_class=HTMLResponse)
def contactus(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from contact")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("contactus.html",{"request" : request, "items" : items})

@app.post("/contactus",response_class=HTMLResponse)
def addcontact(request : Request, name : str =  Form(...), type : str = Form(...), report : str = Form(...) ):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into contact(name,type,report) values(?,?,?)",(name,type,report))
        con.commit()
    return RedirectResponse("/contactus",status_code=status.HTTP_302_FOUND)

@app.get("/admin/index", response_class=HTMLResponse)
def admin_index(request: Request):
    request.session.clear()
    return templates.TemplateResponse("/admin/index.html", {"request" : request})

@app.post("/admin/", response_class=HTMLResponse)
def admin_index(request: Request, username: str = Form(...), password: str = Form(...)):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from admin where username =? and password=?", [username, password])
    admin = cur.fetchone()
    if not admin:
        return templates.TemplateResponse("/admin/index.html", {"request": request, "msg": "Invalid Username or Password"})
    else:
        request.session.setdefault("isLogin", True)
        request.session.setdefault('username', admin['username'])
        request.session.setdefault('uid', admin['id'])
        request.session.setdefault('role', admin['role'])
        return RedirectResponse("/admin/dashboard", status_code=status.HTTP_302_FOUND)

@app.get("/admin/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("/admin/dashboard.html", {"request": request })

@app.get("/admin/products", response_class=HTMLResponse)
def admin_products(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products")
    products = cur.fetchall()
    con.close
    return templates.TemplateResponse("/admin/products.html", {"request": request, "products": products})

@app.get("/admin/products_create", response_class=HTMLResponse)
def products_create(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from  verify")
    products = cur.fetchall()
    con.close
    return templates.TemplateResponse("/admin/products_create.html", {"request": request, "products": products})

@app.post("/admin/products_create", response_class=HTMLResponse)
def admin_products_create(request: Request, pname:str = Form(...), price: str = Form(...), image: str = Form(...), details: str = Form(...), category:str = Form(...)):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into products(pname, price, image, details, category) values(?, ?, ?, ?, ?)",(pname, price, image, details, category))
        con.commit()
    return RedirectResponse("/admin/products",status_code=status.HTTP_302_FOUND)

@app.get("/products_create", response_class=HTMLResponse)
def products_create(request: Request):
    return templates.TemplateResponse("products_create.html", {"request": request })

@app.post("/products_create", response_class=HTMLResponse)
def products_create(request: Request, pname:str = Form(...), price: str = Form(...), category:str = Form(...)):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into verify(pname, price, category) values(?, ?, ?)",(pname, price,category))
        con.commit()
    return RedirectResponse("/Products", status_code=status.HTTP_302_FOUND ) 

@app.get("/addtocart", response_class=HTMLResponse)
async def addtocart(request: Request, pid:int = 1, qty:int = 1):
    uid = request.session.get('uid')
    with sqlite3.connect("Myapp.db", check_same_thread=False) as con:
        cur = con.cursor()
        cur.execute("INSERT into carts(pid, qty, uid) values(?,?,?)",(pid, qty, uid))
        con.commit()
    return RedirectResponse("/cart", status_code=status.HTTP_302_FOUND)

@app.get("/cart", response_class=HTMLResponse)
def cart(request: Request):
    if not request.session.get('isLogin'):
        return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
    uid = request.session.get('uid')
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT *,c.id as cid from farmer u,carts c, products p where  u.id=c.uid and c.pid=p.id and c.uid =? ", [uid])
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("/cart.html", {"request": request, "items": items})

@app.get("/admin/products_edit/{pid}", response_class=HTMLResponse)
def admin_product_edit(request: Request,pid: int = 0):
     con = sqlite3.connect("Myapp.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("select * from products  where id=?" , [pid])
     products = cur.fetchall()
     con.close
     return templates.TemplateResponse("/admin/products_edit.html", {"request": request , "products":products , "pid" : pid} )

@app.get("/admin/verify_edit/{pid}", response_class=HTMLResponse)
def admin_product_edit(request: Request, pid: int = 0):
     con = sqlite3.connect("Myapp.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("select * from verify where id=?" , [pid])
     products = cur.fetchall()
     con.close
     return templates.TemplateResponse("/admin/verify_edit.html", {"request": request , "products":products , "pid" : pid} )

@app.get("/admin/blog_edit/{bid}", response_class=HTMLResponse)
def admin_blog_edit(request: Request, bid: int = 0):
     con = sqlite3.connect("Myapp.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("select * from verify_blog where id=?" , [bid])
     bloggs = cur.fetchall()
     con.close
     return templates.TemplateResponse("/admin/blog_edit.html", {"request": request , "bloggs":bloggs , "bid" : bid} )

@app.get("/blog_edit/{bid}", response_class=HTMLResponse)
def admin_blog_edit(request: Request, bid: int = 0):
     con = sqlite3.connect("Myapp.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("select * from blog where id=?" , [bid])
     blogs = cur.fetchall()
     con.close
     return templates.TemplateResponse("blog_edit.html", {"request": request , "blogs": blogs , "bid" : bid} )

@app.get("/delete/{bid}", response_class=HTMLResponse)
def blog_edit(request: Request, bid: int = 0):
     con = sqlite3.connect("Myapp.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("delete from blog where id=?" , [bid])
     con.commit()
     con.close
     return RedirectResponse("/upload_home", status_code=status.HTTP_302_FOUND )

@app.get("/buynow/{pid}", response_class=HTMLResponse)
def buynow(request: Request, pid: int):
    if not request.session.get('isLogin'):
        return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products where id =?", [pid])
    description = cur.fetchall()
    con.close
    return templates.TemplateResponse("buynow.html", {"request": request, "pid": pid, "description": description[0]})

@app.get("/admin/products_delete/{pid}", response_class=HTMLResponse)
def admin_product_delete(request: Request, pid: int = 0):
     con = sqlite3.connect("Myapp.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("delete from products where id=?" , [pid])
     con.commit()
     con.close
     return RedirectResponse("/admin/products", status_code=status.HTTP_302_FOUND )

@app.get("/deletecart/{cid}", response_class=HTMLResponse)
def delete_cart_item(request: Request, cid: int):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("Delete from carts where id =?", [cid])
    con.commit()
    con.close
    return RedirectResponse("/cart", status_code=status.HTTP_302_FOUND)

@app.get("/admin/verify", response_class=HTMLResponse)
def admin_products(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from  verify")
    products = cur.fetchall()
    con.close
    return templates.TemplateResponse("/admin/verify.html", {"request": request, "products": products})

@app.get("/admin/verify_blog", response_class=HTMLResponse)
def admin_products(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from  verify_blog")
    bloggs = cur.fetchall()
    con.close
    return templates.TemplateResponse("/admin/verify_blog.html", {"request": request, "bloggs": bloggs})


@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

@app.get("/admin/logout", response_class=HTMLResponse)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/index", status_code=status.HTTP_302_FOUND)

@app.get("/confrim", response_class=HTMLResponse)
def confrim(request: Request):
    uid = request.session.get('uid')
    with sqlite3.connect("Myapp.db", check_same_thread=False) as con:
        cur = con.cursor()
        cur.execute("SELECT * from carts where uid = ? ",[uid])
        carts = cur.fetchall()
        for cart in carts:
            print(cart)
            now = datetime.now()
            order_time = now.strftime("%d/%m/%Y %H:%M:%S")
            cur.execute("INSERT into orders(pid, qty, uid,status,date) values(?,?,?,?,?)",
                        [cart[1], cart[2], cart[3], "ORDERED", order_time])
        cur.execute("Delete from carts where uid = ? ", [uid])
        con.commit()
    return RedirectResponse("/orders", status_code=status.HTTP_302_FOUND)

@app.get("/orders",response_class=HTMLResponse)
def orders(request : Request):
    if not request.session.get('isLogin'):
        return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
    uid = request.session.get('uid')
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT *,o.id as oid from farmer u,orders o, products p where  u.id=o.uid and o.pid=p.id and o.uid =?",[uid])
    orders = cur.fetchall()
    con.close
    return templates.TemplateResponse("/orders.html", {"request": request, "orders": orders})

@app.get("/admin/products_delete/{pid}", response_class=HTMLResponse)
def admin_product_delete(request: Request, pid: int = 0):
    return RedirectResponse("/admin/products", status_code=status.HTTP_302_FOUND)

@app.get("/farmerregister", response_class=HTMLResponse)
def farmerregister(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from farmer")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("farmerregister.html",{"request" : request, "items" : items})

@app.post("/farmerregister",response_class=HTMLResponse)
def addfarmer(request : Request, Name : str =  Form(...), Age : int = Form(...), Gender : str = Form(...), PhoneNumber : str = Form(...), AadharNumber:str =Form(...), Address : str = Form(...), District:str = Form(...),State : str = Form(...),FarmCategory : str = Form(...),nameb : str = Form(...), accno : int = Form(...), bankName : str = Form(...),ifsccode : str = Form(...) ,username  : str = Form(...), password  : str = Form(...) ):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into farmer(Name,Age,Gender,PhoneNumber,AadharNumber,Address,District,State,FarmCategory,nameb,accno,bankName,ifsccode,username,password,role,type) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(Name,Age,Gender,PhoneNumber,AadharNumber,Address,District,State,FarmCategory,nameb,accno,bankName,ifsccode,username,password,"1",'Farmer'))
        con.commit()
    return RedirectResponse("/login",status_code=status.HTTP_302_FOUND)

@app.get("/userregister", response_class=HTMLResponse)
def userregister(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from farmer")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("userregister.html",{"request" : request, "items" : items})

@app.post("/userregister",response_class=HTMLResponse)
def addfarmer(request : Request, Name : str =  Form(...), PhoneNumber : str = Form(...), Address : str = Form(...), District:str = Form(...),State : str = Form(...),Pincode : str = Form(...),username : str = Form(...), password : str = Form(...) ):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into farmer(Name,PhoneNumber,Address,District,State,Pincode,username,password,role,type) values(?,?,?,?,?,?,?,?,?,?)",(Name,PhoneNumber,Address,District,State,Pincode,username,password,"2",'User'))
        con.commit()
    return RedirectResponse("/login",status_code=status.HTTP_302_FOUND)
        
@app.get("/authorregister", response_class=HTMLResponse)
def authorregister(request : Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from farmer")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("authorregister.html",{"request" : request, "items" : items})
    
@app.post("/authorregister",response_class=HTMLResponse)
def addfarmer(request : Request,  Name : str =  Form(...), Gender : str = Form(...), PhoneNumber: str = Form(...),Address  : str = Form(...),District   : str = Form(...),State : str = Form(...), username : str = Form(...), password : str = Form(...)):
    with sqlite3.connect("Myapp.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into farmer(Name,Gender,PhoneNumber,Address,District,State,username,password,role,type) values(?,?,?,?,?,?,?,?,?,?)",(Name,Gender,PhoneNumber,Address,District,State,username,password,"3",'Blogger'))
        con.commit()
    return RedirectResponse("/login",status_code=status.HTTP_302_FOUND)

##################### GRAPH IMPLEMENTATION #########################
@app.get("/products_data")
def products_data(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from products")
    items = cur.fetchall()
    con.close
    return items

@app.get("/products_types")
def products_data(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select category,count(*) as count from products GROUP by category")
    items = cur.fetchall()
    con.close
    return items

@app.get("/farmer_types")
def farmer_data(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select type,count(*) as count from farmer GROUP by type")
    items = cur.fetchall()
    con.close
    return items

@app.get("/ragi_chart")
def products_chart(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from chart where pname= 'Ragi'")
    items = cur.fetchall()
    con.close
    return items

@app.get("/rice_chart")
def products_chart(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from chart where pname= 'Rice'")
    items = cur.fetchall()
    con.close
    return items

@app.get("/banana_chart")
def products_chart(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from chart where pname= 'Banana'")
    items = cur.fetchall()
    con.close
    return items

@app.get("/Guava_chart")
def products_chart(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from chart where pname= 'Guava'")
    items = cur.fetchall()
    con.close
    return items

@app.get("/tomato_chart")
def products_chart(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from chart where pname= 'Tomato'")
    items = cur.fetchall()
    con.close
    return items

@app.get("/onion_chart")
def products_chart(request: Request):
    con = sqlite3.connect("Myapp.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from chart where pname= 'Onion'")
    items = cur.fetchall()
    con.close
    return items

@app.get("/admin/verify_edit/{pid}", response_class=HTMLResponse)
def admin_product_edit(request: Request, pid: int = 0):
     con = sqlite3.connect("Myapp.db")
     con.row_factory = sqlite3.Row
     cur = con.cursor()
     cur.execute("select * from verify where id=?" , [pid])
     products = cur.fetchall()
     con.close
     return templates.TemplateResponse("/admin/verify_edit.html", {"request": request , "products":products , "pid" : pid} )
