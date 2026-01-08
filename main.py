import yt_dlp
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests

app = FastAPI()

# CORS સેટિંગ્સ જેથી તમારી વેબસાઈટ સાથે કનેક્ટ થઈ શકે
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-info")
def get_info(url: str):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "status": "success",
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "url": info.get('url'), # આ ડાયરેક્ટ ડાઉનલોડ લિંક છે
                "formats": info.get('formats')
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/download")
async def download(video_url: str):
    # આનાથી યુઝર તમારી સાઈટ પરથી જ વિડિયો ડાઉનલોડ કરી શકશે
    response = requests.get(video_url, stream=True)
    return StreamingResponse(response.iter_content(chunk_size=1024*1024), media_type="video/mp4")
