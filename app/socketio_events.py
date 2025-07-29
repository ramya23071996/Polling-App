from . import r
from flask_socketio import emit

def register_socketio_events(socketio):
    @socketio.on("join_poll")
    def handle_join(poll_id):
        results = r.hgetall(f"poll:{poll_id}")
        emit("update_results", results, broadcast=True)

    @socketio.on("vote_cast")
    def handle_vote(data):
        poll_id = data["poll_id"]
        choice = data["choice"]
        r.hincrby(f"poll:{poll_id}", choice, 1)
        results = r.hgetall(f"poll:{poll_id}")
        emit("update_results", results, broadcast=True)