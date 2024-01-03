from typing import List, Literal
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn
from pydantic import BaseModel, computed_field
from datetime import datetime
import os
from jinja2 import Template, Environment, FileSystemLoader


class Course(BaseModel):
    name: str
    grade: str
    credits: float

    @computed_field
    @property
    def credits_str(self) -> str:
        return '{:.2f}'.format(round(self.credits, 2))


class Period(BaseModel):
    name: str
    courses: List[Course]


class Student(BaseModel):
    name: str
    program: Literal['Advanced', 'Associate', 'Online']
    grade: str
    credits_earned: float
    gpa: float
    start_date: str
    expected_graduation: str
    periods: List[Period]

    @computed_field
    @property
    def gpa_str(self) -> str:
        return '{:.2f}'.format(round(self.gpa, 2))
    
    @computed_field
    @property
    def credits_earned_str(self) -> str:
        return '{:.2f}'.format(round(self.credits_earned, 2))


app = FastAPI()
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
    today = datetime.now().strftime("%B %d, %Y")
    template = env.get_template('template.html')

    # render the HTML using the provided data
    html_content = template.render(**s.model_dump(exclude={'gpa', 'credits_earned', 'credits'}), today=today)
    with open("input.html", "w+") as f:
        f.write(html_content)

    # Run the HTML to PDF conversion
    # os.system("wkhtmltopdf  --allow /Users/musab/Development/miftaah_transcripts/images input.html result.pdf")  
    os.system("wkhtmltopdf  --allow /app/images input.html result.pdf")  
    
    # Return the PDF file as a StreamingResponse
    # headers = {"Content-Disposition": f"inline; filename=result.pdf"}
    headers = {"Content-Disposition": f"attachment; filename=result.pdf"}
    return StreamingResponse(open("result.pdf", "rb"), media_type="application/pdf", headers=headers)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
