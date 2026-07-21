import sqlite3

# Σύνδεση στη βάση (αντικαταστήστε με το δικό σας αρχείο)
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Εκτέλεση του query
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Εκτύπωση των εγγραφών
for row in rows:
    print(row)

conn.close()
