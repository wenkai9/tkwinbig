import os
from typing import List

from db.polardb import PolarDB
from db.vecdb import VecDB
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from datetime import datetime
from utils.conf import Conf


class UserRetrival:
    def __init__(self, conf):
        user_retrival_conf = conf['user_retrival']
        polardb_conf = conf['polardb']
        vecdb_conf = conf['vecdb']
        # 用户语义向量表
        self.user_emb_table = user_retrival_conf['user_emb_table']
        # 视频tag和聚类id关系表
        self.vtag_cluster_table = user_retrival_conf['vtag_cluster_table']
        # 视频tag的向量表
        self.vtag_emb_table = user_retrival_conf['vtag_emb_table']
        # 视频tag的聚类id的向量表
        self.vtag_cluster_emb_table = user_retrival_conf['vtag_cluster_emb_table']
        # 用户视频tag聚类id的graphemb表
        self.user_vtag_cluster_graphemb_table = user_retrival_conf['user_vtag_cluster_graphemb_table']
        # 用户检索结果的文件保存聚类·路径
        self.user_retrival_result_table_prefix = user_retrival_conf['user_retrival_result_table_prefix']
        # self.oss_dir = "/mnt/oss/xxx/"
        self.oss_dir = os.getcwd()

        # 生成语义emb
        # self.sentence_emb_model = 'damo/nlp_gte_sentence-embedding_english-small'
        self.sentence_emb_model = user_retrival_conf['sentence_emb_model']

        self.pipeline_se = pipeline(Tasks.sentence_embedding, model=self.sentence_emb_model)

        # 初始化相关数据库
        self.polardb = PolarDB(polardb_conf)
        self.vecdb = VecDB(vecdb_conf)
        self.db_init()

    def db_init(self):
        self.polardb.connect()
        self.vecdb.connect()

    def set_dilivery_id(self, task_id, shop_id):
        self.task_id = task_id
        self.shop_id = shop_id
        self.user_retrival_result_table = self.user_retrival_result_table_prefix + "_" + self.shop_id
        self.user_retrival_result_dir = self.oss_dir + "/retrival_result/" + self.shop_id

    # 1.Resistance Bands获取nlp emb
    # 2.该emb检索tag_nlp_1向量表获取top5的hashtag_name的id
    # 3.在tag_nlp_id.csv找到该批5个id对应的5个hashtag_name
    # 4.根据hashtag_name在deepwalk_cluster10w.csv找到聚类后的tag id

    def generate_embeddings(self, text: List[str]):
        # 获取语义向量
        inputs = {'source_sentence': text}
        result = self.pipeline_se(input=inputs)
        return result['text_embedding']

    def p_emb(self):
        # 获取商品的语义emb
        pass

    def pemb_vtag(self, vecs):
        # 用商品语义emb获取topk的视频tag
        for vec in vecs:
            ret = self.vecdb.query(self.vtag_emb_table, vec=vec)
        return ret
    def vtag_cluster(self):
        # 获取视频tag的聚类id
        pass

    def vtag_user_retrival(self):
        # 基于视频tag的emb，用视频tag的emb检索topk的user
        pass

    def vtag_cluster_user_retrival(self, text):
        # 基于视频tag聚类id的emb，用视频tag聚类id（即视频tag聚类id的emb）检索topk的user

        # 90-0
        pembs = self.generate_embeddings(text=text)

        # todo, 商品语义向量检索topk的视频tag
        vtags = self.pemb_vtag(pembs)

        # todo,找到视频tag对应的聚类id
        vtags_cluster_ids = self.vtag_cluster()

        p_userids = {}

        # 用视频tag的聚类id检索topk的user
        for index, vtcid in enumerate(vtags_cluster_ids):
            userids = self.vecdb.query(table=self.user_vtag_cluster_graphemb_table, id=vtcid, vec=None, topk=10)
            p_userids[text[index]] = self.extract_userid(text[index], userids)

        return p_userids

    # 基于用户语义emb，用商品emb检索topk的user
    # @param texts：待检索用户包的商品列表
    # @return
    def pemb_user_retrival(self, text):
        # 物品en名字生成emb
        pembs = self.generate_embeddings(text=text)

        # 基于用户语义emb，用商品语义emb检索topk的user
        p_userids = {}
        for index, pemb in enumerate(pembs):
            userids = self.vecdb.query(table=self.user_emb_table, id=None, vec=pembs, topk=1000)
            # p_userids[texts[index]] = userids
            p_userids[text[index]] = self.extract_userid(text[index], userids)

        # for item, value in p_userids.items():
        #     # data = self.extract_userid(item, value)
        #     # 保存至polardb
        #     self.save2db(item, value)
        #     # 保存至csv文件
        #     self.write2file(item, value)

        return p_userids

    def now_datetime(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def create_table(self):
        sql = f'''
        create table if not exists `{self.user_retrival_result_table}`(
           `id` INT UNSIGNED AUTO_INCREMENT,
           `task_id` VARCHAR(64) DEFAULT NULL,
           `unique_id` VARCHAR(64) NOT NULL,
           `item` VARCHAR(64) DEFAULT NULL,
           `score`  FLOAT DEFAULT null,
           PRIMARY KEY (`id` , `unique_id`)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8
        '''
        self.polardb.create_table(sql)

    def save2db(self, item, retrival_ids):
        # 表不存在则创建
        self.create_table()
        # 检索结果保存至结果表，按商户各自保存一张打表
        self.polardb.batch_insert(table=self.user_retrival_result_table, keys=["task_id", "unique_id", "item", "score"], values=retrival_ids)

    def write2file(self, item, retrival_ids):
        # 检索结果保存至文件，按商户id+taskid保存单独文件
        self.create_dir_if_not_exists(self.user_retrival_result_dir)
        filename = self.user_retrival_result_dir + "/" + self.user_retrival_result_table + "_" + self.task_id + ".csv"
        with open(filename, 'a') as file:
            for d in retrival_ids:
                file.write("\t".join(d) + '\n')

    def create_dir_if_not_exists(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Directory '{dir_path}' created successfully")
        else:
            print(f"Directory '{dir_path}' already exists")

    def extract_userid(self, item, retrival_ids):
        data = []
        for rid in retrival_ids:
            row = []
            row.append(self.task_id)
            row.append(rid.fields.get("name", ""))
            row.append(item)
            row.append(str(rid.score))
            data.append(row)
        return data

    # def merge(self, user_retrival_results):
    #     # todo,多路向量检索召回的去重合并
    #     result = user_retrival_results[0]
    #     for urr in user_retrival_results:
    #         result = {**result, **urr}
    #     return result

    def user_retrival(self, text):
        # 对用户的多路向量检索召回
        recalls = []
        return self.merge(recalls)

        # 用户语义向量检索
        p_userids1 = ur.pemb_user_retrival(text=text)

        # 聚类videotag图向量检索
        p_userids2 = user_retrival.vtag_cluster_user_retrival(texts=[])

        # 合并召回结果
        results = user_retrival.merge([p_userids1, p_userids2])

        return p_userids1

    # 保存结果
    def save(self, p_userids):
        for item, value in p_userids.items():
            # data = self.extract_userid(item, value)
            # 保存至polardb
            self.save2db(item, value)
            # 保存至csv文件
            self.write2file(item, value)


if __name__=="__main__":
    conf = Conf().conf_parse("C://Users//DELL//Desktop//tkwinbig(1)//tkwinbig//conf//conf.yaml")
    ur = UserRetrival(conf)
    ur.set_dilivery_id(task_id="12345", shop_id="607080")
    # 用户检索
    p_userids1 = ur.user_retrival(text=["Resistance Bands", "Balding Clippers", "Solar-powered camera"])
    # 保存结果
    ur.save(p_userids1)
    print(p_userids1)




