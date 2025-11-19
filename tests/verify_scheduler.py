import sys
import os
from datetime import datetime, timedelta
import time

# Add src/backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/backend'))

from database import SessionLocal, Broadcast
from scheduler import check_schedules

def verify_scheduler():
    print("Starting Scheduler Verification...")
    
    # Ensure DB is initialized
    # init_db() # Assuming DB is already initialized or we can use existing one
    
    db = SessionLocal()
    try:
        # Create a test broadcast scheduled for NOW (or slightly in the past to ensure it's picked up)
        scheduled_time = datetime.now().astimezone() - timedelta(seconds=1)
        
        test_broadcast = Broadcast(
            content="Scheduler Test Broadcast",
            scheduled_at=scheduled_time,
            status='SCHEDULED',
            task_type='TEST'
        )
        
        db.add(test_broadcast)
        db.commit()
        db.refresh(test_broadcast)
        
        print(f"Created test broadcast ID: {test_broadcast.id}, Status: {test_broadcast.status}")
        
        # Manually trigger the check (simulating the scheduler job)
        print("Triggering check_schedules()...")
        check_schedules()
        
        # Refresh and check status
        db.refresh(test_broadcast)
        print(f"Broadcast ID: {test_broadcast.id}, New Status: {test_broadcast.status}")
        
        if test_broadcast.status == 'COMPLETED':
            print("✅ Verification PASSED: Status changed to COMPLETED.")
        else:
            print(f"❌ Verification FAILED: Status is {test_broadcast.status}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_scheduler()
