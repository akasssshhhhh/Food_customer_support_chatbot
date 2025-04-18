import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()

# Set up connection pooling
db_pool = psycopg2.pool.SimpleConnectionPool(
    1,  # minconn
    10,  # maxconn
    dbname=os.getenv("db_name"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    host=os.getenv("db_host"),
    port=os.getenv("db_port"),
)

def get_db_connection():
 
    try:
        conn = db_pool.getconn()
        if conn is None:
            raise Exception("Unable to get connection from pool.")
        return conn
    except Exception as e:
        print(f"Error getting database connection: {e}")
        raise

def execute_query(query, params=None):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        raise
    finally:
        if conn:
            db_pool.putconn(conn)

def execute_single_query(query, params=None):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchone()
        return result
    except Exception as e:
        print(f"Error executing single query: {e}")
        raise
    finally:
        if conn:
            db_pool.putconn(conn)

def execute_commit_query(query, params=None):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
    except Exception as e:
        print(f"Error executing commit query: {e}")
        raise
    finally:
        if conn:
            db_pool.putconn(conn)
