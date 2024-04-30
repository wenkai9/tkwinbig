import pymysql
from dev.db.db_interface import DBInterface


class PolarDB(DBInterface):
    def __init__(self):
        self._connection = None
        self._cursor = None

    def connect(self, host, port, user, password, database):
        try:
            self._connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
            db_info = self._connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            self._cursor = self._connection.cursor()
        except Exception as e:
            print("Error while connecting to MySQL", e)

    def close(self):
        self._cursor.close()
        self._connection.close()
        print("MySQL connection is closed")

    def insert(self, table, values):
        value_list = []
        # print(values)
        for data in values:
            keys = ", ".join(data.keys())
            value_list.append("(\"" + "\",\"".join(data.values()) + "\")")
        # print(value_list)

        values = ",".join(value_list)
        query = f"INSERT INTO {table} ({keys}) VALUES {values}"
        # print(query)
        self._cursor.execute(query)
        self._connection.commit()

    def select(self, table, condition=None):
        if not condition:
            query = f'SELECT * FROM {table}'
        else:
            where_clause = ' AND '.join([f"{k}='{v}'" for k,v in condition.items()])
            query = f'SELECT * FROM {table} WHERE {where_clause}'
        # print(query)
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def update(self, table, newdata, condition):
        set_clause = ', '.join([f'{column} = %s' for column in newdata])
        where_clause = ' AND '.join([f'{cond} = %s' for cond in condition])
        query = f'UPDATE {table} SET {set_clause} WHERE {where_clause}'
        params = list(newdata.values()) + list(condition.values())
        self._cursor.execute(query, params)
        self._connection.commit()

    def delete(self, table, condition):
        where_clause = ' AND '.join([f'{cond} = %s' for cond in condition])
        query = f'DELETE FROM {table} WHERE {where_clause}'
        self._cursor.execute(query, list(condition.values()))
        self._connection.commit()