import threading
from flask import Flask, request, jsonify
from house import *

env = HouseEnvironment()
shared_state_lock = threading.Lock()

app = Flask(__name__)

@app.route('/rooms', methods=['GET'])
def api_list_rooms():
    """List all rooms in the house."""
    with shared_state_lock:
        rooms = env.house.list_rooms()

    return jsonify({"rooms": rooms}), 200

@app.route('/room/<string:room_name>/items', methods=['GET'])
def api_list_items(room_name):
    """API endpoint to list items in a room."""
    items_list = []
    statues_code = 404

    with shared_state_lock:
        room = env.house.get_room(room_name)
        if room:
            items_list = room.items
            statues_code = 200

    if statues_code == 200:
        return jsonify({"room_name": room_name, "items": items_list}), 200
    else:
        return jsonify({"error": f"Room '{room_name}' not found."}), 404

@app.route('/light', methods=['POST'])
def api_switch_light():
    """API endpoint to switch the light on/off."""
    current_light_status = "unknown"

    with shared_state_lock:
        env.house.switch_light()
        current_light_status = "on" if env.house.light else "off"

    return jsonify({"light_status": current_light_status}), 200

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    print("Flask server started.")

def run_house_environment():
    env.play(shared_state_lock=shared_state_lock)
    print("House environment started.")

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    env_thread = threading.Thread(target=run_house_environment)
    flask_thread.daemon = True

    env_thread.start()
    flask_thread.start()
    env_thread.join()

    print("House server stopped.")
