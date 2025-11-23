from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = 'zxnodessecret'

# Files
USERS_FILE = 'users.json'
VPS_FILE = 'data.json'

# --- Utility Functions ---
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_vps():
    if not os.path.exists(VPS_FILE):
        with open(VPS_FILE, 'w') as f:
            json.dump({}, f)
    with open(VPS_FILE) as f:
        return json.load(f)

def save_vps(vps_data):
    with open(VPS_FILE, 'w') as f:
        json.dump(vps_data, f, indent=4)

# --- Routes ---

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect('/')
        error = "Invalid credentials"
    return render_template('login.html', error=error)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Dashboard
@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    vps_list = load_vps()
    return render_template('dashboard.html', vps_list=vps_list)

# Profile
@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        users = load_users()
        users[session['username']]['password'] = request.form['password']
        save_users(users)
    return render_template('profile.html')

# Maintenance
@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html', message="Panel is under maintenance.")

# Error
@app.route('/error')
def error():
    return render_template('error.html', message="Something went wrong.")

# Create VPS
@app.route('/create_vps', methods=['GET','POST'])
def create_vps():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        vps_id = str(uuid.uuid4())[:8]
        vps_data = load_vps()
        vps_data[vps_id] = {
            "owner": request.form['owner'],
            "memory": request.form['memory'],
            "cpu": request.form['cpu'],
            "disk": request.form['disk'],
            "status": "stopped",
            "host": "127.0.0.1"
        }
        save_vps(vps_data)
        return render_template('vps_created.html', vps_id=vps_id, owner=request.form['owner'],
                               memory=request.form['memory'], cpu=request.form['cpu'],
                               disk=request.form['disk'], host="127.0.0.1")
    return render_template('create_vps.html')

# VPS Details
@app.route('/vps_details/<vps_id>')
def vps_details(vps_id):
    if 'username' not in session:
        return redirect('/login')
    vps_data = load_vps()
    if vps_id not in vps_data:
        return redirect(url_for('error'))
    return render_template('vps_details.html', vps_id=vps_id, info=vps_data[vps_id])

# Edit VPS
@app.route('/edit_vps/<vps_id>', methods=['GET','POST'])
def edit_vps(vps_id):
    if 'username' not in session:
        return redirect('/login')
    vps_data = load_vps()
    if vps_id not in vps_data:
        return redirect(url_for('error'))
    if request.method == 'POST':
        vps_data[vps_id]['memory'] = request.form['memory']
        vps_data[vps_id]['cpu'] = request.form['cpu']
        vps_data[vps_id]['disk'] = request.form['disk']
        save_vps(vps_data)
        return redirect(url_for('vps_details', vps_id=vps_id))
    return render_template('edit_vps.html', vps_id=vps_id, info=vps_data[vps_id])

# VPS Console (placeholder)
@app.route('/vps_console/<vps_id>')
def vps_console(vps_id):
    if 'username' not in session:
        return redirect('/login')
    return render_template('vps_console.html', vps_id=vps_id)

# File Manager (placeholder)
@app.route('/file_manager/<vps_id>')
def file_manager(vps_id):
    if 'username' not in session:
        return redirect('/login')
    return render_template('file_manager.html', vps_id=vps_id)

# Services (placeholder)
@app.route('/services/<vps_id>')
def services(vps_id):
    if 'username' not in session:
        return redirect('/login')
    return render_template('services.html', vps_id=vps_id)

# --- Run App ---
if __name__ == '__main__':
    # Create default admin if none exists
    users = load_users()
    if 'AadishYT' not in users:
        users['AadishYT'] = {"password": "Aadish", "role": "admin"}
        save_users(users)
    app.run(host='0.0.0.0', port=5000, debug=True)
