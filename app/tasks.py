import os
from datetime import timedelta
from ffmpeg import probe, input as ffmpeg_input
from app.database import videos_collection
from celery_worker import celery_app

@celery_app.task
def process_video(video_id: str, file_path: str):
    print("Processing video:", file_path)

    # Extract video duration
    metadata = probe(file_path)
    duration = float(metadata['format']['duration'])
    
    # Generate thumbnail at 10% duration
    thumbnail_time = duration * 0.1
    thumbnail_path = f"thumbnails/{os.path.basename(file_path)}.jpg"
    
    (
        ffmpeg_input(file_path, ss=thumbnail_time)
        .filter('scale', 320, -1)
        .output(thumbnail_path, vframes=1)
        .run(overwrite_output=True)
    )

    # Update MongoDB
    videos_collection.update_one(
        {"_id": video_id},
        {"$set": {
            "status": "done",
            "duration": f"{int(duration//60):02}:{int(duration%60):02}",
            "thumbnail_url": f"/{thumbnail_path}"
        }}
    )
