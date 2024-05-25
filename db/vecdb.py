import dashvector
from db.db_interface import DBInterface


class VecDB(DBInterface):
    def __init__(self, conf):
        self.api_key = conf['api_key']
        self.endpoint = conf['endpoint']

    def connect(self, host, port, user, password, database):
        pass
    def connect(self):
        self.client = dashvector.Client(
            api_key=self.api_key,
            endpoint=self.endpoint
        )

    def insert(self, table, data):
        pass

    def select(self, table, condition=None):
        pass

    def update(self, table, newdata, condition):
        pass

    def delete(self, table, condition):
        pass

    def query(self, table, key):
        pass

    def query(self, table, id=None, vec=None, topk=10, filter=None, include_vector=False):
        # table 即为collection_name
        collection = self.client.get(table)
        rets = collection.query(id=id, vector=None, topk=topk, filter=filter, include_vector=include_vector)
        return rets

    def upsert(self, table, data, dimension, batch=1000):
        # data: docs
        # table 即为collection_name
        # 每1000条执行一次插入
        # 2.创建Collection
        self.client.create(name=table, dimension=dimension)
        collection = self.client.get(table)
        tmp_per_batch = []
        for index, doc in enumerate(data):
            tmp_per_batch.append(doc)
            if index % batch == 0:
                ret = collection.upsert(tmp_per_batch)
                tmp_per_batch.clear()
                if ret.code != 0:
                    print("index: {} ret:{}".format(index, ret))
                else:
                    print("collection insert: {} ret code:{} msg:{}".format(index, ret.code, ret.message))
            if len(tmp_per_batch) !=0:
                ret = collection.upsert(tmp_per_batch)
                tmp_per_batch.clear()
            # ret = collection.upsert(tmp_per_batch)
        return True
