from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Alumni(BaseModel):
    firstName: str
    lastName: str
    yoj: int
    dept: str

db: List[Alumni] = []

@app.post("/add_student", status_code=201)
def add_student(alumni: Alumni):
    db.append(alumni)
    return {"message": "Alumni added successfully"}

@app.get("/search")
def search_student(
    name: Optional[str] = Query(None, description="Partial name search"),
    firstname: Optional[str] = Query(None, description="Exact match for first name"),
    lastname: Optional[str] = Query(None, description="Exact match for last name"),
    year: Optional[int] = Query(None, description="Year of joining"),
    dept: Optional[str] = Query(None, description="Department")
):
    results = db

    if name:
        results = [alum for alum in results if name.lower() in alum.firstName.lower() or name.lower() in alum.lastName.lower()]
    if firstname:
        results = [alum for alum in results if alum.firstName.lower() == firstname.lower()]
    if lastname:
        results = [alum for alum in results if alum.lastName.lower() == lastname.lower()]
    if year:
        results = [alum for alum in results if alum.yoj == year]
    if dept:
        results = [alum for alum in results if alum.dept.lower() == dept.lower()]

    if not results:
        raise HTTPException(status_code=404, detail="No alumni found matching the criteria")

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
