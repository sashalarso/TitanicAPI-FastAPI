from fastapi import FastAPI
from pydantic import BaseModel

from supabase import create_client

supabase=create_client("https://eytukwftfiurimzbqjkj.supabase.co",
                       "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5dHVrd2Z0Zml1cmltemJxamtqIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzc0Mzg3NDMsImV4cCI6MTk5MzAxNDc0M30.gNBN6OOWzGD2UrFMsQK3RXJjwAoB7Zy99D50v4Uedvs")

def getData(limit,age):
    if not limit:
        limit=20  
     
    if age:
        return supabase.from_('passengers').select('*').match({"Age" : age}).limit(limit).execute().data
    return supabase.from_('passengers').select('*').limit(limit).execute().data

def getDataById(id):
    return supabase.from_('passengers').select('*').match({"PassengerId":id}).execute().data
  
app = FastAPI()

class Passenger(BaseModel):
    PassengerId: int
    Survived: int
    Name: str

passengers=list()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/passengers")
async def getAllPassengers(limit : int = None,age : str = None):
    return getData(limit,age)
          
@app.post("/passengers")
async def postPassengers(passenger : Passenger):
    passengers.append(passenger)
    return passenger

@app.get("/passengers/{passengers_id}")
async def getPassengersById(passengers_id : int ):
    return getDataById(passengers_id)


