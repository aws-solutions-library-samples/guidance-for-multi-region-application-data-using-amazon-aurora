import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
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

class Order:
    def __init__(self, email):
        self.email = email

    def get_orders(self, order_id=None):
        with connect("reader") as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                sqlstmt = "select d.item_id, d.qty, d.unit_price, o.order_date from order_details d join orders o on o.order_id = d.order_id and o.email = %s"
                if order_id:
                    sqlstmt = "{} where o.order_id = %s".format(sqlstmt)
                    data = (self.email, order_id, )
                else:
                    data = (self.email, )
                cur.execute(sqlstmt, data)
                return cur.fetchall()
    
    def add(self, data):
        with connect("writer") as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                sqlstmt = "select nextval('order_seq');"
                cur.execute(sqlstmt)
                order_id = cur.fetchone()['nextval']
                items = data.get('items')
                total = 0
                sqlstmt = "insert into order_details(order_id, item_id, qty, unit_price) values(%s, %s, %s, %s);"
                for x in items:
                    data = (order_id, x.get('item_id'), x.get('qty'), x.get('unit_price'), )
                    cur.execute(sqlstmt, data)
                    total += (x.get('qty') * x.get('unit_price'))
                sqlstmt = "insert into orders(order_id, order_date, order_total, email) values(%s, %s, %s, %s);"
                data = (order_id, datetime.now(), total, self.email, )
                cur.execute(sqlstmt, data)
                dbconn.commit()
                return order_id
