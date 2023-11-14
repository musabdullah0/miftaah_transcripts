from enum import Enum
from typing import List, Literal
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from docx2pdf import convert
import uvicorn
from pydantic import BaseModel
from docx import Document
from datetime import datetime
import os
from jinja2 import Template, Environment, FileSystemLoader



class Course(BaseModel):
    name: str
    grade: str
    credits: float


class Period(BaseModel):
    name: str
    courses: List[Course]


class Student(BaseModel):
    name: str
    program: Literal['Advanced', 'Associate', 'Online']
    grade: str
    credits_earned: float
    gpa: float
    expected_graduation: str

def float_to_str(x: float) -> str:
    return '{:.2f}'.format(round(x, 2))


app = FastAPI()
# templates = Jinja2Templates(directory="templates")
env = Environment(loader=FileSystemLoader('templates'))



@app.get("/")
def read_item():
    return {
        "app": "miftaah transcript generator",
        "version": "0.1.0",
        "description": "generate a transcript given a students info. see /docs for api usage"
    }


@app.post("/transcript")
async def generate_transcript(s: Student):
    template = env.get_template('template.html')
    html_content = template.render(**s.model_dump())
    print(html_content[:100])

    # html_content = templates.TemplateResponse("template.html", {"request": request, "name": s.name})
    with open("input.html", "w+") as f:
        f.write(html_content)

    # Return the generated PDF as a StreamingResponse
    os.system("wkhtmltopdf  --allow /Users/musab/Development/miftaah_transcripts/images input.html result.pdf")  
    return StreamingResponse(open("result.pdf", "rb"), media_type="application/pdf", headers={"Content-Disposition": f"inline; filename=result.pdf"})



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
