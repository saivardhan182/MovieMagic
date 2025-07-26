import sqlite3

# ✅ Your Final Movie List
movies = [

    ("Pushpa 2", "Kavali", "Telugu", "images/pushpa.jpeg"),
    ("BRO", "Kavali", "Telugu", "images/bro.jpeg"),
    ("RRR", "Kavali", "Telugu", "images/rrr.jpeg"),
    ("Hi Nanna", "Kavali", "Telugu", "images/hi_nanna.jpeg"),
    ("Salaar", "Kavali", "Telugu", "images/salaar.jpeg"),

    ("BRO", "Nellore", "Telugu", "images/bro.jpeg"),
    ("Animal", "Nellore", "Telugu", "images/animal.jpeg"),
    ("Avengers: Endgame", "Nellore", "English", "images/avengers.jpeg"),
    ("Pushpa", "Nellore", "Telugu", "images/pushpa.jpeg"),
    ("RRR", "Nellore", "Telugu", "images/rrr.jpeg"),

    ("RRR", "Ongole", "Telugu", "images/rrr.jpeg"),
    ("Hi Nanna", "Ongole", "Telugu", "images/hi_nanna.jpeg"),
    ("Salaar", "Ongole", "Telugu", "images/salaar.jpeg"),
    ("Avengers: Endgame", "Ongole", "English", "images/avengers.jpeg"),
    ("Pushpa 2", "Ongole", "Telugu", "images/pushpa.jpeg"),

    ("Hi Nanna", "Guntur", "Telugu", "images/hi_nanna.jpeg"),
    ("RRR", "Guntur", "Telugu", "images/rrr.jpeg"),
    ("Salaar", "Guntur", "Telugu", "images/salaar.jpeg"),
    ("Avengers: Endgame", "Guntur", "English", "images/avengers.jpeg"),
    ("Pushpa 2", "Guntur", "Telugu", "images/pushpa.jpeg"),

    ("Salaar", "Kandukur", "Telugu", "images/salaar.jpeg"),
    ("Hi Nanna", "Kandukur", "Telugu", "images/hi_nanna.jpeg"),
    ("RRR", "Kandukur", "Telugu", "images/rrr.jpeg"),
    ("Avengers: Endgame", "Kandukur", "English", "images/avengers.jpeg"),
    ("Pushpa 2", "Kandukur", "Telugu", "images/pushpa.jpeg"),

    ("Avengers: Endgame", "Hyderabad", "English", "images/avengers.jpeg"),
    ("Pushpa 2", "Hyderabad", "Telugu", "images/pushpa.jpeg"),
    ("BRO", "Hyderabad", "Telugu", "images/bro.jpeg"),
    ("RRR", "Hyderabad", "Telugu", "images/rrr.jpeg"),
    ("Dasara", "Hyderabad", "Telugu", "images/dasara.jpeg"),

    ("KGF 2", "Warangal", "Telugu", "images/kgf2.jpeg"),
    ("Pushpa 2", "Warangal", "Telugu", "images/pushpa.jpeg"),
    ("RRR", "Warangal", "Telugu", "images/rrr.jpeg"),
    ("Hi Nanna", "Warangal", "Telugu", "images/hi_nanna.jpeg"),

    ("Pathaan", "Karimnagar", "Hindi", "images/pathaan.jpeg"),
    ("Batman", "Karimnagar", "English", "images/batman.jpeg"),
    ("Animal", "Karimnagar", "Hindi", "images/animal.jpeg"),

    ("Dasara", "Medak", "Telugu", "images/dasara.jpeg"),
    ("Gadar 2", "Medak", "Hindi", "images/gadar2.jpeg"),
    ("Pushpa 2", "Medak", "Hindi", "images/pushpa.jpeg"),
    ("RRR", "Medak", "Hindi", "images/rrr.jpeg"),

    ("Jawan", "Mumbai", "Hindi", "images/jawan.jpeg"),
    ("Avengers: Endgame", "Mumbai", "English", "images/avengers.jpeg"),
    ("Pushpa 2", "Mumbai", "Telugu", "images/pushpa.jpeg"),
    ("Kalki", "Mumbai", "Telugu", "images/kalki.jpeg"),
    ("Hanuman", "Mumbai", "Telugu", "images/hanuman.jpeg"),
    ("Don 3", "Mumbai", "Hindi", "images/don3.jpeg"),

    ("Gadar 2", "Pune", "Hindi", "images/gadar2.jpeg"),
    ("Jawan", "Pune", "Hindi", "images/jawan.jpeg"),
    ("Avengers: Endgame", "Pune", "English", "images/avengers.jpeg"),
    ("Pushpa 2", "Pune", "Telugu", "images/pushpa.jpeg"),

    ("Batman", "Nagpur", "English", "images/batman.jpeg"),
    ("Hanuman", "Nagpur", "Telugu", "images/hanuman.jpeg"),
    ("Don 3", "Nagpur", "Hindi", "images/don3.jpeg"),

    ("Animal", "Aurangabad", "Hindi", "images/animal.jpeg"),
    ("Jawan", "Aurangabad", "Hindi", "images/jawan.jpeg"),
    ("Avengers: Endgame", "Aurangabad", "English", "images/avengers.jpeg"),
    ("Pushpa 2", "Aurangabad", "Telugu", "images/pushpa.jpeg"),
    ("Kalki", "Aurangabad", "Telugu", "images/kalki.jpeg"),
    ("Hanuman", "Aurangabad", "Telugu", "images/hanuman.jpeg")
]

def init_db():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # Ensure movies table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            city TEXT NOT NULL,
            language TEXT NOT NULL,
            poster TEXT
        )
    ''')

    # 🚨 Delete all existing movie records
    cursor.execute("DELETE FROM movies")
    print("🧹 Cleared old movie records!")

    # 🎬 Insert new movies
    for title, city, language, poster in movies:
        cursor.execute("INSERT INTO movies (title, city, language, poster) VALUES (?, ?, ?, ?)",
                       (title, city, language, poster))
        print(f"✅ Added: {title} in {city}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
