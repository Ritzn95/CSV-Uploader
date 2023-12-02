# main.py (FastAPI backend)
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# SQLite Database Configuration
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)

# FastAPI Templates Configuration
templates = Jinja2Templates(directory="templates")

# File Upload and Form Handling
@app.post("/")
async def create_upload_file(request: Request, file: UploadFile = File(...), name: str = Form(...), age: int = Form(...)):
    contents = await file.read()
    
    # Process CSV and save to the database
    lines = contents.decode().split("\n")
    for line in lines:
        if line.strip():  # Skip empty lines
            csv_data = line.split(",")
            new_user = User(name=csv_data[name], age=csv_data[age])
            db = engine.connect()
            db.execute(metadata.tables["users"].insert().values(new_user))
            db.close()

    return {"filename": file.filename, "name": name, "age": age}

# Frontend Rendering
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
