import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Broadcast
from datetime import datetime
import hashlib
from scheduler import init_scheduler

# --- Flask App Initialization ---
app = Flask(__name__, static_folder='../../frontend')

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Database Session --- 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---
@app.route("/api/broadcasts", methods=["GET"])
def get_broadcasts():
    db: Session = next(get_db())
    broadcasts = db.query(Broadcast).order_by(Broadcast.scheduled_at.asc()).all()
    return jsonify([{
        "id": b.id,
        "uuid": str(b.uuid),
        "content": b.content,
        "scheduled_at": b.scheduled_at.isoformat(),
        "priority": b.priority,
        "status": b.status,
        "task_type": b.task_type,
        "created_at": b.created_at.isoformat() if b.created_at else None
    } for b in broadcasts])

@app.route("/api/broadcasts", methods=["POST"])
def create_broadcast():
    data = request.json
    if not data or 'content' not in data or 'scheduled_at' not in data:
        return jsonify({"error": "`content` and `scheduled_at` are required."}), 400

    db: Session = next(get_db())
    content_hash = hashlib.sha256(data['content'].encode('utf-8')).hexdigest()

    new_broadcast = Broadcast(
        content=data['content'],
        scheduled_at=datetime.fromisoformat(data['scheduled_at']),
        priority=data.get('priority', 0),
        task_type=data.get('task_type', 'REGULAR'),
        status='SCHEDULED',
        content_hash=content_hash
    )

    db.add(new_broadcast)
    db.commit()
    db.refresh(new_broadcast)

    return jsonify({
        "id": new_broadcast.id,
        "uuid": str(new_broadcast.uuid)
    }), 201

# --- Frontend Serving ---
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# --- Main Execution ---
if __name__ == '__main__':
    # Initialize Scheduler
    init_scheduler(app)
    
    # Note: `debug=True` is for development only.
    # Warning: With debug=True, the reloader will start two schedulers.
    # For production or testing scheduler, use use_reloader=False or handle the lock.
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)