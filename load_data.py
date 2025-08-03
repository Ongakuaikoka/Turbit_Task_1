import requests
import logging
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}"
DB_NAME = os.getenv("MONGO_DB")

def get_data(endpoint):
    url = f"https://jsonplaceholder.typicode.com/{endpoint}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch {endpoint} from API", exc_info=True)
        raise

def load_to_mongo():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        db = client[DB_NAME]

        posts = get_data("posts")
        comments = get_data("comments")

        db.posts.drop()
        db.comments.drop()

        db.posts.insert_many(posts)
        db.comments.insert_many(comments)
        logger.info(f"Inserted {len(posts)} posts and {len(comments)} comments.")
    except errors.PyMongoError as e:
        logger.error("MongoDB error", exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error in data loading", exc_info=True)
        raise

if __name__ == "__main__":
    load_to_mongo()
