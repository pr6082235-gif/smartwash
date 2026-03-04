"""
Database connection and utility functions
"""
import pymysql
import os
from functools import wraps
from flask import session, redirect, url_for, flash, current_app


def get_db():
    """Get a database connection."""
    connection = pymysql.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', ''),
        database=os.environ.get('MYSQL_DB', 'smartwash_pro'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
    return connection


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


def log_activity(user_id, action, module, description='', ip_address=''):
    """Log user activity."""
    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO logs (user_id, action, module, description, ip_address) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (user_id, action, module, description, ip_address)
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Log error: {e}")
