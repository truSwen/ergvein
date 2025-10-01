import sqlite3
import os

def setup_database():
    """Létrehozza az adatbázist, a szükséges táblákat, és feltölti mintaadatokkal."""
    try:
        # Az adatbázis fájl helyének meghatározása a szkripthez képest
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracker.db')

        # Csatlakozás az adatbázishoz (létrehozza, ha nem létezik)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # --- Táblák Létrehozása ---

        # Orders (Megrendelések) tábla létrehozása
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_code TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Az 'Orders' tábla sikeresen létrehozva vagy már létezik.")

        # LocationUpdates (Helyzetfrissítések) tábla létrehozása
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LocationUpdates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_tracking_code TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_tracking_code) REFERENCES Orders (tracking_code)
            )
        ''')
        print("A 'LocationUpdates' tábla sikeresen létrehozva vagy már létezik.")

        # --- Mintaadatok Beszúrása (Javasolt Kiegészítés) ---
        
        # Ellenőrizzük, hogy az Orders tábla üres-e, hogy ne szúrjunk be duplikált adatokat
        cursor.execute("SELECT COUNT(id) FROM Orders")
        # A fetchone() egy tuple-t ad vissza, pl. (0,) vagy (5,), ezért kell az első elem.
        if cursor.fetchone()[0] == 0:
            print("Mintaadatok beszúrása...")
            sample_orders = [
                ('CAREGO-TEST-123', 'Felvéve'),
                ('CAREGO-TEST-456', 'Kiszállítás alatt'),
                ('CAREGO-TEST-789', 'Központi raktárban')
            ]
            cursor.executemany("INSERT INTO Orders (tracking_code, status) VALUES (?, ?)", sample_orders)
            print(f"{len(sample_orders)} mintamegrendelés hozzáadva az 'Orders' táblához.")

            # Hozzáadhatunk egy minta helyzetfrissítést is az egyik rendeléshez
            sample_location_update = ('CAREGO-TEST-456', 47.4979, 19.0402) # Budapest koordinátái
            cursor.execute(
                "INSERT INTO LocationUpdates (order_tracking_code, latitude, longitude) VALUES (?, ?, ?)",
                sample_location_update
            )
            print("Egy minta helyzetfrissítés hozzáadva a 'LocationUpdates' táblához.")
        else:
            print("Az 'Orders' tábla már tartalmaz adatokat, a mintaadatok beszúrása kihagyva.")


        # Változtatások mentése és kapcsolat bezárása
        conn.commit()
        conn.close()
        print("Adatbázis sikeresen beállítva.")
    except sqlite3.Error as e:
        print(f"Adatbázis hiba: {e}")

if __name__ == '__main__':
    setup_database()
