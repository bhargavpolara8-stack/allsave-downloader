import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-info")
def get_info(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL is missing")
        
    try:
        # YouTube અને Insta માટે બેસ્ટ સેટિંગ્સ
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # વિડિયો ડેટા કાઢવો
            info = ydl.extract_info(url, download=False)
            
            if not info:
                return {"status": "error", "message": "Could not extract info"}

            return {
                "status": "success",
                "title": info.get('title', 'No Title'),
                "thumbnail": info.get('thumbnail', ''),
                "url": info.get('url', '')
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def home():
    return {"message": "AllSave API is Running"}
