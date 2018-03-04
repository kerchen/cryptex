import hashlib
import os
import sqlite3

import encryption
import shared_cfg

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    c = conn.cursor()
    c.execute(create_table_sql)


def connect_to_db(db_filename):
    sql_create_password_table = """
            CREATE TABLE IF NOT EXISTS passwords (
            key integer UNIQUE PRIMARY KEY,
            name text,
            username text,
            password text,
            site_url text
            ); 
        """
 
    conn = create_connection(db_filename)
    if conn is not None:
        create_table(conn, sql_create_password_table)
    else:
        raise(Exception("Error! cannot create the database connection."))

    return conn

def open_encrypted_db(password,
                      encrypted_db_filename=shared_cfg.encrypted_db_filename,
                      decrypted_db_filename=shared_cfg.db_filename):
    key = hashlib.sha256(password).digest()
    if os.path.exists(encrypted_db_filename):
        encryption.decrypt(key,
                           in_filename=encrypted_db_filename,
                           out_filename=decrypted_db_filename)
        conn = connect_to_db(decrypted_db_filename)
    else:
        conn = connect_to_db(decrypted_db_filename)
