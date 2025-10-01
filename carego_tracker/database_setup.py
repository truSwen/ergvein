import sqlite3
import os

def setup_database():
    """
    Létrehozza az adatbázist, a szükséges táblákat, 
    és feltölti egyedi tesztadattal a fejlesztéshez.
    """
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

        # --- Tesztadat Beszúrása (a te logikád alapján) ---
        
        # Ellenőrizzük, hogy a teszt adat már létezik-e
        cursor.execute("SELECT * FROM Orders WHERE tracking_code = 'TEST123'")
        if cursor.fetchone():
            print("A 'TEST123' követési kódú teszt megrendelés már létezik.")
        else:
            # Teszt megrendelés beszúrása
            cursor.execute(
                "INSERT INTO Orders (tracking_code, status) VALUES (?, ?)",
                ('TEST123', 'folyamatban')
            )
            print("A 'TEST123' követési kódú teszt megrendelés sikeresen hozzáadva.")

        # Változtatások mentése és kapcsolat bezárása
        conn.commit()
        conn.close()
        print("Adatbázis sikeresen beállítva.")
    except sqlite3.Error as e:
        print(f"Adatbázis hiba: {e}")

if __name__ == '__main__':
    setup_database()
