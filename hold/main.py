
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form, HTTPException
import subprocess
import uvicorn



app = FastAPI()
templates = Jinja2Templates(directory="templates")
class InstagramURL(BaseModel):
    url: str

#--------------------------------------------------------

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get-instagram-url/", response_model=dict)
async def get_instagram_url(request: Request, url: str = Form(...)):
    try:
        # Run the command and capture the output
        output = subprocess.check_output(['yt-dlp', '--get-url', url])

        # Decode the output from bytes to string
        output_str = output.decode('utf-8')

        # Render the result.html template with the response included
        return templates.TemplateResponse("result.html", {"request": request, "response": output_str})
    
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")






if __name__ == "__main__":
   
    uvicorn.run(app, host="127.0.0.1", port=8000)
