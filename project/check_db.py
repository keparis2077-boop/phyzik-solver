import sqlite3
import sys

conn = sqlite3.connect('history.db')
conn.row_factory = sqlite3.Row

output = []

# Check tables
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
output.append("=== TABLES ===")
for t in tables:
    output.append(t['name'])

# Check users
output.append("\n=== USERS ===")
users = conn.execute("SELECT id, username, email, xp, coins FROM users").fetchall()
output.append(f"Total users: {len(users)}")
for u in users:
    output.append(f"  ID={u['id']}, username={u['username']}, email={u['email']}, xp={u['xp']}, coins={u['coins']}")

# Check history
output.append("\n=== HISTORY ===")
history_count = conn.execute("SELECT COUNT(*) as cnt FROM history").fetchone()['cnt']
output.append(f"Total records: {history_count}")

# Check history schema
columns = conn.execute("PRAGMA table_info(history)").fetchall()
output.append("History columns:")
for col in columns:
    output.append(f"  {col['name']} ({col['type']})")

conn.close()

result = "\n".join(output)
print(result)

# Also write to file
with open('db_check_output.txt', 'w', encoding='utf-8') as f:
    f.write(result)
