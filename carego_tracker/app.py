from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Az adatbázis fájl helyének meghatározása az app.py-hoz képest
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracker.db')

def get_db_connection():
    """Létrehoz egy adatbázis-kapcsolatot és visszaadja azt."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/update_location', methods=['POST'])
def update_location():
    """
    A futár app ezen a végponton keresztül küldi el a helyzetét.
    Egyelőre csak egy sikeres választ ad vissza.
    """
    return jsonify({"status": "success", "message": "Location update received"}), 200

@app.route('/api/track/<string:tracking_code>', methods=['GET'])
def track_package(tracking_code):
    """
    A kliens ezen a végponton keresztül követheti a csomagot.
    Egyelőre csak dummy adatokat ad vissza.
    """
    dummy_data = {
        "tracking_code": tracking_code,
        "status": "folyamatban",
        "last_known_location": {
            "latitude": 47.4979,
            "longitude": 19.0402,
            "timestamp": "2025-10-01T10:00:00Z"
        }
    }
    return jsonify(dummy_data), 200

if __name__ == '__main__':
    # Ellenőrizzük, hogy az adatbázis létezik-e, mielőtt a szerver elindul
    if not os.path.exists(DATABASE):
        print(f"Hiba: Az adatbázis ('{DATABASE}') nem található.")
        print("Kérlek, futtasd a 'database_setup.py' szkriptet először.")
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)