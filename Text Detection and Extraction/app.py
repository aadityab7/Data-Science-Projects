from project import app
from project import socketio
import os

if __name__ == '__main__':
    #app.run(debug = True, host = "0.0.0.0", port = int(os.environ.get("PORT",8000)), ssl_context="adhoc")
    #app.run(debug = True, host = "0.0.0.0", port = int(os.environ.get("PORT",8000)))
    #socketio.run(app, debug = True)
    #socketio.run(app)
    socketio.run(app, host = "0.0.0.0", port = int(os.environ.get("PORT", 8000)), allow_unsafe_werkzeug=True)