from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

complaints_db = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('lodge_complaint')
def handle_lodge(data):
    time.sleep(0.5)
    new_id = len(complaints_db) + 1
    complaint = {
        'id': new_id,
        'room': data['room'],
        'category': data['category'],
        'description': data['description'],
        'status': 'Pending'
    }
    complaints_db.append(complaint)
    emit('complaint_lodged', {'msg': f"Ticket #{new_id} Submitted Successfully", 'status': 'success'})
    emit('refresh_warden', complaints_db, broadcast=True)

@socketio.on('request_all_data')
def handle_fetch():
    emit('update_data', complaints_db)

@socketio.on('resolve_complaint')
def handle_resolve(data):
    c_id = data.get('id')
    for c in complaints_db:
        if c['id'] == c_id:
            c['status'] = 'Completed'
            break
    emit('update_data', complaints_db, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)