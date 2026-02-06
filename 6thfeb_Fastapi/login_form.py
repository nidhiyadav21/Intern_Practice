
from fastapi import FastAPI,Form,Request,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()



VALID_USERNAME = "Nidhi"
VALID_PASSWORD = "Nidhi123"

#Setup templates folder
templates = Jinja2Templates(directory="templates")


@app.get("/",response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("form.html",{"request":request})

@app.post("/login")
def login(username: str = Form(...),password: str = Form(...)):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return {"message":"Login Successful"}
    else:
        # raise HTTPException(status_code=401,detail="Incorrect username or password")
        return {"message":"Login Failed"}

