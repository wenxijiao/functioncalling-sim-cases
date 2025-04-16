from flask import Flask, request, jsonify
from house import *

app = Flask(__name__)

house_state = House([Room("living room"), Room("bedroom"), Room("kitchen")], name="My House")

@app.route('/rooms', methods=['GET'])
def list_rooms():
    """List all rooms in the house."""
    rooms = house_state.list_rooms()
    return jsonify(rooms), 200

@app.route('/room/<string:room_name>/items', methods=['GET'])
def api_list_items(room_name):
    """API endpoint to list items in a room."""
    room = house_state.get_room(room_name)
    if not room:
        return jsonify({"error": f"Room '{room_name}' not found."}), 404

    items_list = room.items
    return jsonify({"room_name": room_name, "items": items_list}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
