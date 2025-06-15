import os
from datetime import datetime
from fastapi import APIRouter, UploadFile, File
from bson import ObjectId
from app.database import videos_collection
from app.tasks import process_video

router = APIRouter()

UPLOAD_DIR = "videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

@router.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Insert to MongoDB
    video_doc = {
        "filename": file.filename,
        "upload_time": datetime.utcnow().isoformat(),
        "status": "pending"
    }
    result = videos_collection.insert_one(video_doc)
    video_id = str(result.inserted_id)

    # Start Celery task
    process_video.delay(video_id, file_path)
    
    return {"id": video_id}

@router.get("/video-status/{id}")
def get_status(id: str):
    video = videos_collection.find_one({"_id": ObjectId(id)})
    return {"status": video.get("status", "unknown")}

@router.get("/video-metadata/{id}")
def get_metadata(id: str):
    video = videos_collection.find_one({"_id": ObjectId(id)})
    return video
