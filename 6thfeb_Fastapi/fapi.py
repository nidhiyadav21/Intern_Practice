import uvicorn
from fastapi import FastAPI

#Create the app object
app = FastAPI()

#Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {"message": "Hello World"}

#Route with a single parameter
@app.get('/Welcome')
def get_name(name:str):
    return {"Welcome To FastApi Tutorial": f'{name}'}

#Run the API with uvicorn

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)

#uvicorn main:app --reload