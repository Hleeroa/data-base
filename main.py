import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
            DROP TABLE IF EXISTS client;
            DROP DOMAIN IF EXISTS domain_email;
            DROP EXTENSION IF EXISTS citext;
        ''')
        cur.execute("""
            CREATE EXTENSION citext;
            CREATE DOMAIN domain_email AS citext
            CHECK(VALUE ~ '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$');
            CREATE TABLE client (
                client_id SERIAL PRIMARY KEY, 
                first_name VARCHAR (20) NOT NULL, 
                last_name VARCHAR (30) NOT NULL,
                email domain_email,
                phone_number BIGINT UNIQUE
            );
        """)


def add_client(conn, first_name, last_name, email, phone_number):
    if email is None:
        email = 'NULL'
    elif phone_number is None:
        phone_number = 'NULL'
    with conn.cursor() as cur:
        cur.execute(f'''
            INSERT INTO client (first_name, last_name, email, phone_number)
            VALUES('{first_name}', '{last_name}', '{email}', {phone_number});
        ''')


def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute(f'''
            UPDATE client
            SET phone_number = '{phone_number}'
            WHERE client_id = {client_id};
        ''')


def delete_phone(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(f'''
            UPDATE client
            SET phone_number = NULL
            WHERE client_id = {client_id};
        ''')


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute(f'''
            DELETE FROM client
            WHERE client_id = {client_id};
        ''')


def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute(f'''
                SELECT * FROM client
                WHERE first_name = '{first_name}';
            ''')
        elif last_name is not None:
            cur.execute(f'''
                SELECT * FROM client
                WHERE last_name = '{last_name}';
            ''')
        elif email is not None:
            cur.execute(f'''
                SELECT * FROM client
                WHERE email = '{email}';
            ''')
        elif phone_number is not None:
            cur.execute(f'''
                SELECT * FROM client
                WHERE phone_number = {phone_number};
            ''')
        else:
            return 'Client is not found. The input information is not enough'
        print(cur.fetchall())


with psycopg2.connect(database="client_db", user="postgres", password='gotnoidea') as conn:
    create_db(conn)
    add_client(conn, 'Leo', 'Peterson', 'LeoPeterson@gmail.com', 89922182192)
    add_client(conn, 'Maria', 'Reynolds', 'MissMaria@mail.ru', 82213465782)
    find_client(conn, first_name = 'Leo')
    delete_phone(conn, 1)
    add_phone(conn, 2, 87654321910)
    find_client(conn, phone_number = 87654321910)
    delete_client(conn, 1)
    delete_client(conn, 2)
conn.close()
