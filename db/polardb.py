import pymysql
from db.db_interface import DBInterface


class PolarDB(DBInterface):
    def __init__(self, conf):
        self.host=conf['host']
        self.port=conf['port']
        self.user=conf['user']
        self.password=conf['password']
        self.database=conf['database']

    # def connect(self, host, port, user, password, database):
    #     try:
    #         self._connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    #         db_info = self._connection.get_server_info()
    #         print("Connected to MySQL Server version ", db_info)
    #         self._cursor = self._connection.cursor()
    #     except Exception as e:
    #         print("Error while connecting to MySQL", e)

    def connect(self):
        try:
            self._connection = pymysql.connect(host=self.host,
                                               port=self.port,
                                               user=self.user,
                                               password=self.password,
                                               database=self.database)
            print("Connected to MySQL Server version ", self._connection.get_server_info())
            self._cursor = self._connection.cursor()
        except Exception as e:
            print("Error while connecting to MySQL", e)

    def close(self):
        self._cursor.close()
        self._connection.close()
        print("MySQL connection is closed")

    def insert_tmp(self, table, values):
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

    # 按照keys顺序向数据库插入数据
    # @param table: str
    # @param keys: list
    # @param values: list[list]
    def insert(self, table, keys, values):
        value_list = []
        # print(values)
        for data in values:
            value_list.append("(\"" + "\",\"".join(data) + "\")")
        # print(value_list)

        vals = ",".join(value_list)
        keys = ", ".join(keys)
        query = f"INSERT INTO {table} ({keys}) VALUES {vals}"
        # print(query)
        self._cursor.execute(query)
        self._connection.commit()

    def batch_insert(self, table, keys, values, batch=100):
        # 按batch批次插入数据
        tmp = []
        for index, value in enumerate(values):
            tmp.append(value)
            if index % batch == 0:
                self.insert(table, keys, tmp)
                tmp.clear()
        if len(tmp) != 0:
            self.insert(table, keys, tmp)
            tmp.clear()

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

    def create_table(self, sql):
        try:
            self._cursor.execute(sql)
            self._connection.commit()
            print("create table success")
        except Exception as e:
            print("create table error, %s", e)

    def query(self, table, key):
        pass
    def upsert(self, table, data):
        pass