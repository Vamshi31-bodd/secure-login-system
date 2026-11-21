import sqlite3
import getpass
from pathlib import Path
from flask_bcrypt import Bcrypt

db_path = Path("instance/users.db")

if not db_path.exists():
    print("Database not found!")
    raise SystemExit

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT username, password_hash FROM user")
users = cursor.fetchall()

bcrypt = Bcrypt()

for username, stored_hash in users:
    print(f"\nUser: {username}")
    print("Hash exists:", bool(stored_hash))
    print("Bcrypt format:", stored_hash.startswith(("$2b$", "$2a$", "$2y$")))
    print("Hash length:", len(stored_hash))

    password = getpass.getpass("Enter this user's password to verify: ")

    try:
        valid = bcrypt.check_password_hash(stored_hash, password)
        print("Password hash verification:", "PASSED" if valid else "FAILED")
    except ValueError:
        print("Password hash verification: FAILED")

conn.close()