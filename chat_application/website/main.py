from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO
from db.database import DataBase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
db = DataBase()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle POST request logic here
        sender = request.form['username']
        
        # You might want to do some validation or processing with the username
        
        # Save the username in the session for later use
        session['username'] = sender
        
        # Redirect to the main chat page
        return redirect(url_for('chat'))
    else:
        return render_template('login.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        sender = request.form['name']
        content = request.form['message']

        db.save_message(sender, content)
        socketio.emit('message response', {'name': sender, 'message': content}, broadcast=True)

    return 'Message sent successfully!'

@app.route('/chat')
def chat():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('index'))
    
    return render_template('chats.html')

@socketio.on('event')
def handle_custom_event(json):
    data = dict(json)
    if "name" in data:
        sender = data["name"]
        content = data["message"]

        db.save_message(sender, content)

    socketio.emit('message response', {'name': sender, 'message': content}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)