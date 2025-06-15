## ⚙️ Tech Stack

- **Python 3.9+**
- **FastAPI** - for the web server
- **MongoDB** using `pymongo` - for storing metadata
- **Celery + Redis** - for background video processing
- **FFmpeg** - to extract video duration and generate thumbnails 

## Start FastAPI Server
uvicorn app.main:app --reload

## Sample API Requests 
Upload Video: curl -F "file=@example.mp4" http://localhost:8000/upload-video/

Response:
{
  "message": "Video uploaded successfully",
  "video_id": "666fcccbd29d2271a25d1c4a"
}
## Get Video Metadata
curl http://localhost:8000/video-metadata/666fcccbd29d2271a25d1c4a
{
  "filename": "vid.mp4",
  "upload_time": "2025-06-14T10:00:00",
  "status": "done",
  "duration": "00:02:45",
  "thumbnail_url": "http://localhost:8000/thumbnails/vid.jpg"
}

## FFmpeg Commands Used
To extract video duration: ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 vid.mp4
To generate thumbnail at 10% of duration: ffmpeg -ss 00:00:17 -i example.mp4 -frames:v 1 -q:v 2 thumbnails/img.jpg

