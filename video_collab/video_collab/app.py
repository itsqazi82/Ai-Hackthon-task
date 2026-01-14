from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
socketio = SocketIO(app)

os.makedirs("uploads", exist_ok=True)

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- FILE UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
    return "File uploaded successfully"

@app.route("/files/<filename>")
def files(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------- WHITEBOARD SOCKET ----------------
@socketio.on("draw")
def handle_draw(data):
    emit("draw", data, broadcast=True)

# ---------------- SIGNALING (WebRTC) ----------------
@socketio.on("signal")
def signaling(data):
    emit("signal", data, broadcast=True, include_self=False)

if __name__ == "__main__":
    socketio.run(app, debug=True)
