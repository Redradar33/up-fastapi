from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form, HTTPException
import uvicorn
import yt_dlp as youtube_dl

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class InstagramURL(BaseModel):
    url: str

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get-instagram-url/", response_model=dict)
async def get_instagram_url(request: Request, url: str = Form(...)):
    try:
        # Create a YouTube-DL instance
        ydl_opts = {}
        ydl = youtube_dl.YoutubeDL(ydl_opts)

        # Extract the video URL
        with ydl:
            result = ydl.extract_info(url, download=False)
            video_url = result['url']

        # Render the result.html template with the response included
        return templates.TemplateResponse("result.html", {"request": request, "response": video_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

if __name__ == "__main__":
#uvicorn.run(app, host="127.0.0.1", port=8000)
    #import uvicorn

    #uvicorn.run(app, host="0.0.0.0", port=10000)