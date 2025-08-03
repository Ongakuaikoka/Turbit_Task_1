import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient, errors
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
try:
    MONGO_URI = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Trigger connection error if Mongo is unreachable
    db = client[os.getenv("MONGO_DB")]
    logger.info("Connected to MongoDB")
except errors.ServerSelectionTimeoutError as e:
    logger.error("Could not connect to MongoDB", exc_info=True)
    raise RuntimeError("Database unavailable") from e

app = FastAPI()

@app.get("/users/posts_count")
def get_user_posts_count():
    try:
        pipeline = [
            {"$group": {"_id": "$userId", "total_posts": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        result = db.posts.aggregate(pipeline)
        return [{"userId": r["_id"], "total_posts": r["total_posts"]} for r in result]
    except Exception as e:
        logger.error("Error aggregating posts per user", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/posts/{post_id}/comments")
def get_comments_for_post(post_id: int):
    try:
        comments = list(db.comments.find({"postId": post_id}, {"_id": 0}))
        if not comments:
            raise HTTPException(status_code=404, detail=f"No comments found for post {post_id}")
        return {"postId": post_id, "comments": comments}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching comments for post {post_id}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
