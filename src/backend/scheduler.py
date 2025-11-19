from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal, Broadcast
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def check_schedules():
    """
    Checks for scheduled broadcasts that need to be executed.
    This function runs every minute.
    """
    logger.info("Checking for scheduled broadcasts...")
    
    db = SessionLocal()
    try:
        now = datetime.now().astimezone()
        
        # Find broadcasts that are SCHEDULED and due (or past due)
        # Note: In a real app, you might want to handle "missed" schedules differently
        pending_broadcasts = db.query(Broadcast).filter(
            Broadcast.status == 'SCHEDULED',
            Broadcast.scheduled_at <= now
        ).all()

        for broadcast in pending_broadcasts:
            execute_broadcast(broadcast.id)
            
    except Exception as e:
        logger.error(f"Error checking schedules: {e}")
    finally:
        db.close()

def execute_broadcast(broadcast_id):
    """
    Executes a single broadcast task.
    """
    db = SessionLocal()
    try:
        broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
        if not broadcast:
            logger.error(f"Broadcast {broadcast_id} not found.")
            return

        logger.info(f"Executing broadcast {broadcast.id}: {broadcast.content}")
        
        # Update status to BROADCASTING
        broadcast.status = 'BROADCASTING'
        db.commit()
        
        # TODO: Implement actual TTS and playback logic here
        # For now, we simulate the broadcast
        
        # Update status to COMPLETED
        broadcast.status = 'COMPLETED'
        db.commit()
        logger.info(f"Broadcast {broadcast.id} completed.")

    except Exception as e:
        logger.error(f"Error executing broadcast {broadcast_id}: {e}")
        if broadcast:
            broadcast.status = 'FAILED'
            broadcast.error_log = str(e)
            db.commit()
    finally:
        db.close()

def init_scheduler(app):
    """
    Initializes and starts the scheduler.
    """
    # Add the job to run every minute
    scheduler.add_job(func=check_schedules, trigger="interval", seconds=60)
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started.")
    
    # Shut down the scheduler when exiting the app
    import atexit
    atexit.register(lambda: scheduler.shutdown())
