
import psycopg2

def get_partner_data():
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute("SELECT * FROM partners ORDER BY id ASC")
        partners = cur.fetchall()
        cur.close()
        conn.close()
        return partners
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return None

def get_partner_type(id):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute(f"SELECT type FROM company_types where id={id}")
        type = cur.fetchone()
        cur.close()
        conn.close()
        return type
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return None

def get_discount(id):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute(f"""
            select sum(purchases.product_quantity) as total from purchases where partner_id = {id};
        """)
        amount = cur.fetchone()[0]
        cur.close()
        conn.close()
        if amount is None or amount < 10000:
            return '0%'
        elif amount >= 10000 and amount <50000:
            return '5%'
        elif amount >= 50000 and amount <300000:
            return '10%'
        elif amount >= 300000:
            return '15%'
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return None

def update_partner(id, data):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute(f"""
            select sum(purchases.product_quantity) as total from purchases where partner_id = {id};
        """)
        amount = cur.fetchone()[0]
        cur.close()
        conn.close()
        if amount < 10000:
            return '0%'
        elif amount >= 10000 and amount <50000:
            return '5%'
        elif amount >= 50000 and amount <300000:
            return '10%'
        elif amount >= 300000:
            return '15%'
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return None

def get_partner_id(name):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute(f"""
            select id from partners where name='{name}';
        """)
        id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return id
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return None

def get_type_id(type):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute(f"""
            select id from company_types where type='{type}';
        """)
        id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return id
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return None

def alter_partner(id, type_id, name, director, email, phone, address, tax_number, rating):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute("""
                    UPDATE partners 
                    SET company_type = %s, name = %s, director = %s, email = %s, 
                        phone = %s, address = %s, tax_number = %s, rating = %s
                    WHERE id = %s;
                    SELECT * FROM partners WHERE id = %s;
                """, (type_id, name, director, email, phone, address, tax_number, rating, id, id))

        partners = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        print(partners)
        return
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return

def add_partner(company_type, name, director, email, phone, address, tax_number, rating):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='1234', host='localhost', port=5433)
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO partners (company_type, name, director, email, phone, address, tax_number, rating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (company_type, name, director, email, phone, address, tax_number, rating))

        conn.commit()
        cur.close()
        conn.close()
        return
    except psycopg2.Error as e:
        print(f"database error: {e}")
        return





# alter_partner(1, 1, 'База Строитель4', 'Иванова Аександа Ивановна', 'aleksandraivanova@ml.ru', '4931234567','652050, Кемеровская область, город Юрга, ул. Лесная, 15', '2222455179', 7)