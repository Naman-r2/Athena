import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services.blog_service import create_and_store_blog

logger = logging.getLogger(__name__)

TOPICS_CYCLE = [
    "FastAPI",
    "Docker",
    "PostgreSQL",
    "Chroma embeddings",
    "Microservices",
    "REST APIs",
    "Kubernetes",
    "System Design"
]
current_topic_index = 0

def generate_daily_blog():
    global current_topic_index
    topic = TOPICS_CYCLE[current_topic_index]
    logger.info(f"Scheduler fired. Generating daily blog on topic: {topic}")
    
    db = SessionLocal()
    try:
        create_and_store_blog(db, topic)
        logger.info(f"Successfully generated daily blog on: {topic}")
    except Exception as e:
        logger.error(f"Failed to generate daily blog: {e}")
    finally:
        db.close()
        
    current_topic_index = (current_topic_index + 1) % len(TOPICS_CYCLE)

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Adding jitter to not interfere with startup immediately
    scheduler.add_job(generate_daily_blog, 'interval', hours=24, jitter=120)
    scheduler.start()
    logger.info("APScheduler started. Generating 1 blog per day.")
