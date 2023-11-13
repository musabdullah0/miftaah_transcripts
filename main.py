from typing import List
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from docx2pdf import convert
import uvicorn
from pydantic import BaseModel
from docx import Document
from datetime import datetime

class Course(BaseModel):
    name: str
    grade: str
    credits: float


class Period(BaseModel):
    name: str
    courses: List[Course]


class Student(BaseModel):
    name: str
    grade: str
    credits_earned: str
    gpa: str
    expected_graduation: str


app = FastAPI()

@app.get("/")
def read_item():
    return {
        "app": "miftaah transcript generator",
        "version": "0.1.0",
        "description": "generate a transcript given a students info. see /docs for api usage"
    }


@app.post("/transcript")
async def generate_transcript(s: Student):
    # update template file
    doc_file_name = s.name.replace(" ", "") + ".docx"
    doc = Document("Template_file.docx")
    update = {
        "{date_issued}": datetime.now().strftime("%B %d, %Y"),
        "{name}": s.name,
        "{grade}": s.grade,
        "{credits}": s.credits_earned,
        "{gpa}": s.gpa,
        "{expected_grad}": s.expected_graduation
    }
    for p in doc.paragraphs:
        for k, v in update.items():
            if k in p.text:
                print("before update: ", p.text)
                p.text = p.text.replace(k, v)
                print("after update: ", p.text)
    
    doc.save(doc_file_name)
    pdf_file_name = doc_file_name.replace("docx", "pdf")

    convert(doc_file_name, pdf_file_name, keep_active=True)

    # Return the generated PDF as a StreamingResponse
    return StreamingResponse(open(pdf_file_name, "rb"), media_type="application/pdf", headers={"Content-Disposition": f"inline; filename={pdf_file_name}"})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
