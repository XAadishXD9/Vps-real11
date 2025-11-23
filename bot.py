from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'zxnodes_secret'

# Admin credentials
ADMIN_USERNAME = 'Aadish'
ADMIN_PASSWORD = 'Aadish'

# Placeholder VPS list
vps_list = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/panel')
        else:
            return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')

@app.route('/panel')
def panel():
    if 'admin' not in session:
        return redirect('/')
    return render_template('panel.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/create_vps', methods=['GET','POST'])
def create_vps():
    if 'admin' not in session:
        return redirect('/')
    if request.method == 'POST':
        name = request.form['name']
        memory = request.form['memory']
        vcpu = request.form['vcpu']
        disk = request.form['disk']
        iso = request.form['iso']
        vps_list.append({'name': name, 'memory': memory, 'vcpu': vcpu, 'disk': disk, 'iso': iso, 'status': 'Stopped'})
        return redirect('/manage_vps')
    return render_template('create_vps.html')

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    if 'admin' not in session:
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email','')
        return redirect('/panel')
    return render_template('add_user.html')

@app.route('/manage_vps', methods=['GET','POST'])
def manage_vps():
    if 'admin' not in session:
        return redirect('/')
    if request.method == 'POST':
        vps_name = request.form['vps_name']
        action = request.form['action']
        for vps in vps_list:
            if vps['name'] == vps_name:
                if action == 'start':
                    vps['status'] = 'Running'
                elif action == 'stop':
                    vps['status'] = 'Stopped'
                elif action == 'restart':
                    vps['status'] = 'Running'
                elif action == 'delete':
                    vps_list.remove(vps)
                break
        return redirect('/manage_vps')
    return render_template('manage_vps.html', vps_list=vps_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
