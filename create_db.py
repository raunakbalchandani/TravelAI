import sqlite3

def create_db():
    conn = sqlite3.connect('travel_packages.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS packages (
                        id INTEGER PRIMARY KEY,
                        from_city TEXT,
                        to_city TEXT,
                        package_type TEXT,
                        cost INTEGER
                      )''')

    packages = [
        ('Mumbai', 'London', 'Standard', 500),
        ('Mumbai', 'London', 'Premium', 1000),
        ('Hong Kong', 'London', 'Standard', 600),
        ('Hong Kong', 'London', 'Premium', 1100)
    ]

    cursor.executemany('''INSERT INTO packages (from_city, to_city, package_type, cost)
                          VALUES (?, ?, ?, ?)''', packages)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()