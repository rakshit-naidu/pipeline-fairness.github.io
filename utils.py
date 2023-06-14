import sqlite3

def getUserRole(username):
    # Connect to the database and retrieve the user's role
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None