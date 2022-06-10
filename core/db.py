import sqlite3


class dbManager(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = False
    def connect(self):
        if self.conn == False:
            try:
                conn = sqlite3.connect(self.db_name)
                self.conn = conn
            except Exception as err:
                print('EXCEPTION ON DBMANAGER CONNECT ... {}'.format(err))
                return False
        return self.conn
    def close(self):
        if self.conn != False:
            try:
                self.conn.close()
                self.conn = False
            except Exception as err:
                print('EXCEPTION ON DBMANAGER CLOSE ... {}'.format(err))
                return False
        return True
    def cursor(self):
        if self.connect():
            try:
                return self.conn.cursor()
            except Exception as err:
                print('EXCEPTION ON DBMANAGER CURSOR ... {}'.format(err))
        return False
    def execute_query(self, query, params=()):
        cursor = self.cursor()
        if cursor:
            try:
                cursor.execute(query, params)
                return cursor
            except Exception as err:
                print('EXCEPTION ON DBMANAGER EXECUTE QUERY ... {}'.format(err))
        return False
    def select(self, query, params=()):
        temp_resp = self.execute_query(query, params=params)
        if temp_resp:
            try:
                return temp_resp.fetchall()
            except Exception as err:
                print('EXCEPTION ON DBMANAGER SELECT ... {}'.format(err))
        return False
    def commit(self):
        self.conn.commit()
    def insert(self, query, params=(), commit=True):
        temp_resp = self.execute_query(query, params=params)
        if not temp_resp:
            return None
        if commit:
            self.commit()
            return temp_resp.lastrowid
        else:
            return True
    def update(self, query, params={}):
        temp_resp = self.execute_query(query, params=params)
        if not temp_resp:
            return None
        self.conn.commit()
        return temp_resp.rowcount
    def delete(self, query, params={}):
        temp_resp = self.execute_query(query, params=params)
        if not temp_resp:
            return None
        self.conn.commit()
        return temp_resp.rowcount
    def has_table(self, table_name):
        temp_resp = self.select('SELECT name FROM sqlite_master WHERE type="table" AND name="{}"'.format(table_name))
        if not temp_resp:
            return None
        if len(temp_resp) > 0:
            return True
        return False
    def create_table(self, query):
        temp_resp = self.execute_query(query)
        if not temp_resp:
            return None
        return True