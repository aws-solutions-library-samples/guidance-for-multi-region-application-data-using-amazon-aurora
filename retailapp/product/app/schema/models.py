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

class Product:
    def __init__(self, product_name=None):
        self.product_name = product_name
        self.db = connect("reader")

    def fetch_data_new(self, sqlstmt, data={}, type="reader"):
        try:
            with self.db.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt, data)
                return cur.fetchall()
        except Exception:
            with connect(type) as dbconn:
                with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sqlstmt, data)
                    return cur.fetchall()

    def fetch_data(self, dbconn, sqlstmt, data={}, type="reader"):
        try:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt, data)
                return cur.fetchall()
        except Exception:
            with connect(type) as dbconn:
                with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sqlstmt, data)
                    return cur.fetchall()
    
    def return_items(self):
        with connect("reader") as dbconn:
            sqlstmt = "SELECT * FROM {}".format(self.product_name)
            return self.fetch_data(dbconn, sqlstmt)

    def popular_items(self, top=5, interval=180):
        with connect("reader") as dbconn:
            sqlstmt = """
                      with items as (
                      select item_id
                      from (
                       select item_id, cnt, 
                              rank() over (order by cnt desc) mrank
                       from (
                        select item_id, count(1) as cnt
                        from orders a join order_details b 
                         on a.order_id = b.order_id
                        group by item_id
                        ) t
                       ) t where mrank <= %(top)s order by cnt desc
                      )
                      SELECT id,name,price, description,img_url,'apparels' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM apparels a join items i on i.item_id = a.id 
                       left outer join reviews r on r.category=%(apparels)s and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name,price, description,img_url,'fashion' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM fashion a join items i on i.item_id = a.id 
                       left outer join reviews r on r.category=%(fashion)s and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name, price, description,img_url,'bicycles' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM bicycles a join items i on i.item_id = a.id 
                       left outer join reviews r on r.category=%(bicycles)s and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name, price, description,img_url,'jewelry' as category, count(1) review_cnt, round(avg(rating)*20) rating
                       FROM jewelry a join items i on i.item_id = a.id 
                       left outer join reviews r on r.category=%(jewelry)s and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                       """
            data = {'top': top, 'apparels': 'apparels', 'fashion': 'fashion', 'bicycles': 'bicycles', 'jewelry': 'jewelry'}
            return self.fetch_data(dbconn, sqlstmt, data)

    def show_all_items(self, id=None):
        with connect("reader") as dbconn:
            if id:
                sqlstmt = """
                SELECT id,name,price, description,img_url FROM apparels where id = %(id)s
                UNION
                SELECT id,name,price, description,img_url FROM fashion where id = %(id)s
                UNION
                SELECT id,name, price, description,img_url FROM bicycles where id = %(id)s
                UNION 
                SELECT id,name, price, description,img_url FROM jewelry where id = %(id)s
                ORDER BY name
                """
                return self.fetch_data(dbconn, sqlstmt,{'id': id})
            else:
                sqlstmt = """
                SELECT id,name,price, description,img_url FROM apparels
                UNION
                SELECT id,name,price, description,img_url FROM fashion
                UNION
                SELECT id,name, price, description,img_url FROM bicycles
                UNION 
                SELECT id,name, price, description,img_url FROM jewelry
                ORDER BY name
                """
                return self.fetch_data(dbconn, sqlstmt)

    def show_all_items_new(self, id=None):
        if id:
            sqlstmt = """
            SELECT id,name,price, description,img_url FROM apparels where id = %(id)s
            UNION
            SELECT id,name,price, description,img_url FROM fashion where id = %(id)s
            UNION
            SELECT id,name, price, description,img_url FROM bicycles where id = %(id)s
            UNION 
            SELECT id,name, price, description,img_url FROM jewelry where id = %(id)s
            ORDER BY name
            """
            return self.fetch_data_new(sqlstmt, {'id': id})
        else:
            sqlstmt = """
            SELECT id,name,price, description,img_url FROM apparels
            UNION
            SELECT id,name,price, description,img_url FROM fashion
            UNION
            SELECT id,name, price, description,img_url FROM bicycles
            UNION 
            SELECT id,name, price, description,img_url FROM jewelry
            ORDER BY name
            """
            return self.fetch_data_new(sqlstmt)

    def getProducts(self, productListString):
        if isinstance(productListString, list):
            productListString = ",".join(productListString)
        sqlstmt = """select id as productId, name, price, img_url from apparels a where id in (%(productListString)s)
                     union
                     select id as productId, name, price, img_url from fashion a where id in (%(productListString)s)
                     union
                     select id as productId, name, price, img_url from bicycles a where id in (%(productListString)s)
                     union
                     select id as productId, name, price, img_url from jewelry a where id in (%(productListString)s)
                     """
        with connect("reader") as dbconn:
            return self.fetch_data(dbconn, sqlstmt, {'productListString': productListString})

    def whereami(self):
        sqlstmt = "select inet_server_addr();"
        with connect("writer") as dbconn:
            writer = self.fetch_data(dbconn, sqlstmt, {},"writer")
        with connect("reader") as dbconn:
            reader = self.fetch_data(dbconn, sqlstmt, {},"reader")
        return [{"writer": writer, "reader": reader}]

    def addProduct(self, category, product):
        if not isinstance(product, list):
            product = ast.literal_eval(product)
        sqlstmt = """insert into %(category)s (name, description, img_url, category, inventory, price)
                     values (%(name)s, %(description)s, %(img_url)s, %(category)s, %(inventory)s, %(price)s) returning *;"""
        data = {"category": category, "name": product.get("name"), "description": product.get("description"), "img_url": product.get("img_url"),
                "inventory": product.get("inventory"), "price": product.get("price")}
        with connect("writer") as dbconn:
            return self.fetch_data(dbconn, sqlstmt, data,"writer")
  
