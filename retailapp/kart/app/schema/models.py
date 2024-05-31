import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json

def connect(type="writer"):
    rds_host = os.environ['DATABASE_HOST']
    secrets_file = '/mnt/secrets-store/aurora-pg_dbuser1_EKSGDB1'
    secrets = {}
    if os.path.exists(secrets_file):
        with open(secrets_file, 'r') as f:
            secrets = eval(json.dumps(json.load(f)))
    db_user = secrets and secrets.get("username") or os.environ.get('DATABASE_USER')
    password = secrets and secrets.get("password") or os.environ.get('DATABASE_PASSWORD')
    rw_db_name = os.environ['DATABASE_DB_NAME']
    ro_db_name = os.environ['DATABASE_RODB_NAME']
    port = os.environ['DATABASE_PORT']
    db_name = rw_db_name if type == "writer" else ro_db_name
    return psycopg2.connect(sslmode="prefer", host=rds_host, user=db_user, password=password, dbname=db_name, connect_timeout=10000, port=port, keepalives_interval=30)

class Kart:
    def __init__(self):
        pass

    def set(self, key, value):
        with connect("writer") as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    sqlstmt = "insert into SessionStore(key, value) values(%s, %s) on conflict(key) do update set value = EXCLUDED.value"
                    cur.execute(sqlstmt, (key, json.dumps(value),))
                    dbconn.commit()
                except Exception as e:
                    print (e)
                    dbconn.rollback()
                    msg = "Error Occurred"

    def get(self, key):
        sqlstmt = "select value from SessionStore where key=%s"
        with connect("reader") as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt, (key, ))
                r = cur.fetchone()
                return dict(r).get('value') if r else []

    def delete(self, key):
        sqlstmt = "delete from SessionStore where key=%s"
        with connect("writer") as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt, (key, ))
                dbconn.commit()
