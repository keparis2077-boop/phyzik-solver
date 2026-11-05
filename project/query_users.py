import sqlite3
conn = sqlite3.connect('history.db')
users = conn.execute('SELECT id, username, email, xp, coins FROM users').fetchall()
with open('users_output.txt', 'w') as f:
    f.write(f'Users: {len(users)}\n')
    for r in users:
        f.write(str(r) + '\n')
conn.close()
print("Done")
