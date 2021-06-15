import os
import contextlib
import mysql
import mysql.connector
import config
import pymysql


class mysql_conn_class:

    def __init__(self, _app_logger) -> None:
        self.app_logger = _app_logger

    @contextlib.contextmanager
    def get_mysql_conn(self, db=""):
        
        if db=="":

                """
                Context manager for when not specifying database (eg when creating database). db kwargs not used
                """
                conn = pymysql.connect(host=config.mysql_host,
                                            user=config.mysql_user,
                                            password=config.mysql_pwd,
                                             port=config.mysql_port#tunnel.local_bind_port,
                                            )
                try: 
                    yield conn
                    print("****DB Conn Established****")
                except Exception as e:
                    print(e)
                finally:
                    conn.close()
        else:
            """
            Context manager used for when specifying database (eg add a record). db kwarg specified
            """
            conn = mysql.connector.connect(host=config.mysql_host,
                                        user=config.mysql_user,
                                        password=config.mysql_pwd,
                                        database=db)
            try:
                yield conn
            except mysql.connector.Error as e:
                self.app_logger.exception(e)
            finally:
                conn.close()
    
    def get_database_names(self):
        db_names_list = []
        try:
            with self.get_mysql_conn() as connection:
                show_db = "SHOW DATABASES"
                
                with connection.cursor() as cursor:
                    cursor.execute(show_db)
                    for db in cursor:
                        db_names_list.append(db[0])
                    if db_names_list: return (db_names_list)
                    else: return []
        except Exception as e:
            print(e)
        except Exception as e:
            self.app_logger.exception(e)

    def get_tables_in_database(self, dbname):
        tb_names_list = []
        try:
            with self.get_mysql_conn(dbname) as connection:
                show_tb = "SHOW TABLES"
                
                with connection.cursor() as cursor:
                    cursor.execute(show_tb)
                    for db in cursor:
                        tb_names_list.append(db[0])
                    if tb_names_list: return (tb_names_list)
                    else: return []
        except mysql.connector.Error as e:
            print((e))
        except Exception as e:
            self.app_logger.exception(e)

    def get_count_of_table(self, dbname, tbname):
        try:
            with self.get_mysql_conn(dbname) as connection:
                count = "SELECT COUNT(*) FROM %s" %tbname
                with connection.cursor() as cursor:
                    cursor.execute(count)
                    return cursor.fetchone()[0]
        except mysql.connector.Error as e:
            self.app_logger.exception(e)
            self.app_logger.error("Error creating new database")

    def get_count_of_table(self, dbname, tbname):
        try:
            with self.get_mysql_conn(dbname) as connection:
                count = "SELECT COUNT(*) FROM %s" %tbname
                with connection.cursor() as cursor:
                    cursor.execute(count)
                    return cursor.fetchone()[0]
        except mysql.connector.Error as e:
            self.app_logger.exception(e)
            self.app_logger.error("Error creating new database")

    def describe_table_database(self, dbname, tbname):
        """
        Returns None, simply prints Describe {table name} query on mysql db
        """
        try:
            with self.get_mysql_conn(dbname) as connection:
                describe_table_query = f"DESCRIBE {tbname}"
                with connection.cursor() as cursor:
                    cursor.execute(describe_table_query)
                    result = cursor.fetchall()
                    for row in result:
                        print(row)
        except mysql.connector.Error as e:
            self.app_logger.exception(e)
        except Exception as e:
            self.app_logger.exception(e)

    def create_database(self, dbname):
        try:
            with self.get_mysql_conn() as connection:
                create_db = f"CREATE DATABASE {dbname}"
                with connection.cursor() as cursor:
                    cursor.execute(create_db)
        except mysql.connector.Error as e:
            self.app_logger.exception(e)
            self.app_logger.error("Error creating new database")

    def create_table(self, dbname, tbquery):
        try:
            with self.get_mysql_conn(dbname) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(tbquery)
                    connection.commit()
        except mysql.connector.Error as e:
            self.app_logger.exception(e)
            self.app_logger.error("Error creating new table")

    def insert_transactions_into_database(self, dbname, transactions):
        
        with self.get_mysql_conn(dbname,) as connection:
            try:
                insert_db = "INSERT INTO transaction (id, transaction_status_id, vendor_id, transaction_type_id, amount, date, description) values (%s, %s, %s, %s, %s, %s, %s)"
                with connection.cursor() as cursor:
                    cursor.executemany(insert_db, transactions)
                    connection.commit()
            except mysql.connector.Error as e:
                print((e))
                connection.rollback()

    def insert_account_transactions_into_database(self, dbname, account_transactions):
        with self.get_mysql_conn(dbname) as connection:
            try:
                insert_db = "INSERT INTO  account_transaction (account_id, transaction_id) values (%s, %s)"
                with connection.cursor() as cursor:                  
                    cursor.executemany(insert_db, account_transactions)
                    connection.commit()
            except mysql.connector.Error as e:
                print(e)
                connection.rollback()    

    def insert_vendors_into_database(self, dbname, vendors):
        with self.get_mysql_conn(dbname) as connection:
            try:
                insert_db = "INSERT INTO  vendor (id, code) values (%s, %s)"
                with connection.cursor() as cursor:                  
                    cursor.executemany(insert_db, vendors)
                    connection.commit()
            except mysql.connector.Error as e:
                print(e)
                connection.rollback()    
    
    def find_record_by_id(self, dbname, tbname, id):
        try:
            with self.get_mysql_conn(dbname) as connection:
                select_id = f"Select * from {tbname} where id = {id}"
                with connection.cursor() as cursor:
                    cursor.execute(select_id)
                    return cursor.fetchone()
        except mysql.connector.Error as e:
            print("Error creating new database")
            print(e)


    def find_balance_by_id(self, dbname, tbname, id):
        try:
            with self.get_mysql_conn(dbname) as connection:
                select_balance = f"Select balance from {tbname} where id = {id}"
                with connection.cursor() as cursor:
                    cursor.execute(select_balance)
                    return cursor.fetchone()
        except mysql.connector.Error as e:
            print("Error creating new database")
            print(e)


    def update_account_balance_in_database(self, dbname, account_new_balance):
        with self.get_mysql_conn(dbname) as connection:
            try:
                insert_db = "Update account SET balance = %s WHERE id = %s"
                with connection.cursor() as cursor:                  
                    cursor.execute(insert_db, account_new_balance)
                    connection.commit()
            except mysql.connector.Error as e:
                print(e)
                connection.rollback()    

