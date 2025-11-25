import sqlite3
import os

# Path to the database
db_path = os.path.join('instance', 'modres.db')

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Migrating database schema...")

try:
    # Add job_url column to application table
    cursor.execute("ALTER TABLE application ADD COLUMN job_url VARCHAR(500)")
    print("✓ Added job_url column")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("✓ job_url column already exists")
    else:
        print(f"✗ Error adding job_url: {e}")

try:
    # Add notes column to application table
    cursor.execute("ALTER TABLE application ADD COLUMN notes TEXT")
    print("✓ Added notes column")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("✓ notes column already exists")
    else:
        print(f"✗ Error adding notes: {e}")

try:
    # Update status default value (can't alter default in SQLite, so just note it)
    print("✓ Status column uses existing default")
except Exception as e:
    print(f"✗ Error: {e}")

# Create user_profile table if it doesn't exist
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name VARCHAR(100),
            email VARCHAR(120),
            phone VARCHAR(20),
            linkedin_url VARCHAR(200),
            github_url VARCHAR(200),
            portfolio_url VARCHAR(200),
            work_auth_status VARCHAR(50),
            disability_status VARCHAR(50),
            veteran_status VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    """)
    print("✓ user_profile table created/verified")
except Exception as e:
    print(f"✗ Error creating user_profile: {e}")

# Create resume table if it doesn't exist
try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            json_data JSON NOT NULL,
            pdf_path VARCHAR(200),
            score INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (application_id) REFERENCES application(id)
        )
    """)
    print("✓ resume table created/verified")
except Exception as e:
    print(f"✗ Error creating resume table: {e}")

conn.commit()
conn.close()

print("\n✅ Database migration complete!")
print("Restart your Flask server now.")
