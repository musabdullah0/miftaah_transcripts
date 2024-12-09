# miftaah transcripts

a fastapi application to create transcript PDFs for miftaah students

`POST /transcript`
sample request body
```json
{
  "name": "musab",
  "program": "Advanced",
  "grade": "second",
  "credits_earned": 1,
  "gpa": 2,
  "start_date": "08/01/2019",
  "expected_graduation": "05/30/23",
  "periods": [
    {
      "name": "Fall 2021",
      "courses": [
        {
          "name": "Arabic",
          "grade": "100",
          "credits": 1
        },
        {
          "name": "Tafseer",
          "grade": "90",
          "credits": 1
        },
        {
          "name": "Seerah",
          "grade": "95",
          "credits": 1
        }
      ]
    }
  ]
}
```
