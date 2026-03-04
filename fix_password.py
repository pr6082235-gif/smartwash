"""
SmartWash Pro - Password Fix Script
Run this to fix login issues
"""
import bcrypt
import pymysql
import os

# =============================================
# CHANGE THESE TO MATCH YOUR SETUP
# =============================================
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'pandi2006'        # Your MySQL password (blank if XAMPP with no password)
MYSQL_DB = 'smartwash_pro'
# =============================================

LOGIN_PASSWORD = 'Admin@123'

print("=" * 50)
print("  SmartWash Pro - Password Fix Tool")
print("=" * 50)

# Step 1: Generate correct hash
print("\n[1] Generating password hash...")
hashed = bcrypt.hashpw(LOGIN_PASSWORD.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
print(f"    Hash generated: {hashed[:30]}...")

# Step 2: Connect to database
print("\n[2] Connecting to MySQL...")
try:
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("    Connected successfully!")
except Exception as e:
    print(f"\n ERROR: Cannot connect to database!")
    print(f"    Details: {e}")
    print(f"\n Fix: Check your MySQL is running and MYSQL_PASSWORD is correct in this script")
    input("\nPress Enter to exit...")
    exit()

# Step 3: Check if users table exists
print("\n[3] Checking users table...")
try:
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE 'users'")
        result = cursor.fetchone()
        if not result:
            print("    Users table NOT found! Creating database tables...")
            print("    Please run schema.sql first!")
            print("\n    Command:")
            print('    mysql -u root -p smartwash_pro < schema.sql')
            input("\nPress Enter to exit...")
            exit()
        print("    Users table found!")
        
        # Check existing users
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        print(f"    Found {len(users)} users: {[u['username'] for u in users]}")

except Exception as e:
    print(f"    Error: {e}")

# Step 4: Update passwords
print("\n[4] Updating passwords...")
try:
    with conn.cursor() as cursor:
        # Check if users exist
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        count = cursor.fetchone()['cnt']
        
        if count == 0:
            print("    No users found! Inserting default users...")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role) VALUES 
                ('sureshgopi', 'suresh@smartwashpro.com', %s, 'Suresh Gopi', 'admin'),
                ('staff1', 'staff1@smartwashpro.com', %s, 'Staff Member', 'staff')
            """, (hashed, hashed))
        else:
            # Update existing
            cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'sureshgopi'", (hashed,))
            cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'staff1'", (hashed,))
            
            # Also update all other users
            cursor.execute("UPDATE users SET password_hash = %s WHERE username NOT IN ('sureshgopi', 'staff1')", (hashed,))
        
    conn.commit()
    print("    Passwords updated successfully!")

except Exception as e:
    print(f"    Error updating: {e}")
    conn.rollback()

# Step 5: Verify
print("\n[5] Verifying fix...")
try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT username, role, is_active FROM users")
        users = cursor.fetchall()
        for u in users:
            print(f"    User: {u['username']} | Role: {u['role']} | Active: {u['is_active']}")

except Exception as e:
    print(f"    Error: {e}")

conn.close()

print("\n" + "=" * 50)
print("  FIX COMPLETE!")
print("=" * 50)
print(f"\n  Login Credentials:")
print(f"  Username : sureshgopi")
print(f"  Password : Admin@123")
print(f"\n  Staff Login:")
print(f"  Username : staff1")
print(f"  Password : Admin@123")
print("\n  Now run: python app.py")
print("  Open: http://localhost:5000")
print("=" * 50)
input("\nPress Enter to exit...")