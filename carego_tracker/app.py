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
    """A futár app ezen a végponton keresztül küldi el a helyzetét."""
    data = request.get_json()
    if not data or 'tracking_code' not in data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    tracking_code = data['tracking_code']
    latitude = data['latitude']
    longitude = data['longitude']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO LocationUpdates (order_tracking_code, latitude, longitude) VALUES (?, ?, ?)",
            (tracking_code, latitude, longitude)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Location update received"}), 201
    except sqlite3.Error as e:
        return jsonify({"status": "error", "message": f"Database error: {e}"}), 500


@app.route('/api/track/<string:tracking_code>', methods=['GET'])
def track_package(tracking_code):
    """A kliens ezen a végponton keresztül követheti a csomagot."""
    try:
        conn = get_db_connection()

        # Megrendelés adatainak lekérdezése
        order = conn.execute('SELECT * FROM Orders WHERE tracking_code = ?', (tracking_code,)).fetchone()

        if order is None:
            return jsonify({"status": "error", "message": "Tracking code not found"}), 404

        # Utolsó helyzet lekérdezése
        last_location = conn.execute(
            'SELECT latitude, longitude, timestamp FROM LocationUpdates WHERE order_tracking_code = ? ORDER BY timestamp DESC LIMIT 1',
            (tracking_code,)
        ).fetchone()

        conn.close()

        response_data = {
            "tracking_code": order['tracking_code'],
            "status": order['status'],
            "created_at": order['created_at'],
            "last_known_location": None
        }

        if last_location:
            response_data["last_known_location"] = {
                "latitude": last_location['latitude'],
                "longitude": last_location['longitude'],
                "timestamp": last_location['timestamp']
            }

        return jsonify(response_data), 200

    except sqlite3.Error as e:
        return jsonify({"status": "error", "message": f"Database error: {e}"}), 500


if __name__ == '__main__':
    # Ellenőrizzük, hogy az adatbázis létezik-e, mielőtt a szerver elindul
    if not os.path.exists(DATABASE):
        print(f"Hiba: Az adatbázis ('{DATABASE}') nem található.")
        print("Kérlek, futtasd a 'database_setup.py' szkriptet először.")
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)